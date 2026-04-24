"""Database connection and query layer using pyodbc."""

import logging
import pyodbc
from typing import Any, Optional
from config import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Demo data — used when DB_SERVER is not configured (offline / dev mode)
# ---------------------------------------------------------------------------
DEMO_AGENTS = [
    {"agent_id": 1, "full_name": "Laura Martínez", "email": "laura@agency360.com",
     "role": "GA", "unit": "Norte", "active": True, "production": 185_400_000},
    {"agent_id": 2, "full_name": "Carlos Restrepo", "email": "carlos@agency360.com",
     "role": "GU", "unit": "Centro", "active": True, "production": 142_300_000},
    {"agent_id": 3, "full_name": "Sofía Valencia", "email": "sofia@agency360.com",
     "role": "Senior", "unit": "Sur", "active": True, "production": 98_700_000},
    {"agent_id": 4, "full_name": "Miguel Torres", "email": "miguel@agency360.com",
     "role": "GA", "unit": "Occidente", "active": True, "production": 231_000_000},
    {"agent_id": 5, "full_name": "Admin User", "email": "admin@agency360.com",
     "role": "Admin", "unit": "HQ", "active": True, "production": 0},
]

DEMO_KPIS = {
    "total_agents": 130,
    "active_agents": 118,
    "monthly_production": 3_245_800_000,
    "monthly_target": 3_500_000_000,
    "achievement_pct": 92.7,
    "collections_pct": 88.4,
    "new_clients": 47,
}

DEMO_RANKINGS = [
    {"rank": 1, "agent_name": "Miguel Torres", "unit": "Occidente",
     "production": 231_000_000, "target": 200_000_000, "achievement": 115.5},
    {"rank": 2, "agent_name": "Laura Martínez", "unit": "Norte",
     "production": 185_400_000, "target": 180_000_000, "achievement": 103.0},
    {"rank": 3, "agent_name": "Carlos Restrepo", "unit": "Centro",
     "production": 142_300_000, "target": 150_000_000, "achievement": 94.9},
    {"rank": 4, "agent_name": "Sofía Valencia", "unit": "Sur",
     "production": 98_700_000, "target": 120_000_000, "achievement": 82.3},
    {"rank": 5, "agent_name": "Andrés Gómez", "unit": "Norte",
     "production": 87_500_000, "target": 100_000_000, "achievement": 87.5},
]


class Database:
    """Manages SQL Server connections and exposes query helpers."""

    def __init__(self) -> None:
        self._conn: Optional[pyodbc.Connection] = None
        self.demo_mode: bool = not bool(config.DB_SERVER and config.DB_SERVER != "localhost")

    def connect(self) -> bool:
        if self.demo_mode:
            logger.info("Running in DEMO mode — no DB connection required")
            return True
        try:
            self._conn = pyodbc.connect(config.connection_string, timeout=5)
            logger.info("Database connected successfully")
            return True
        except pyodbc.Error as exc:
            logger.error("DB connection failed: %s", exc)
            self.demo_mode = True
            return False

    def _execute(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        if not self._conn:
            self.connect()
        cursor = self._conn.cursor()
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    # ------------------------------------------------------------------
    # Auth
    # ------------------------------------------------------------------
    def get_agent_by_email(self, email: str) -> Optional[dict[str, Any]]:
        if self.demo_mode:
            return next((a for a in DEMO_AGENTS if a["email"] == email), None)
        rows = self._execute(
            "SELECT agent_id, full_name, email, role, unit, active "
            "FROM agents WHERE email = ? AND active = 1",
            (email,),
        )
        return rows[0] if rows else None

    # ------------------------------------------------------------------
    # KPIs
    # ------------------------------------------------------------------
    def get_dashboard_kpis(self, role: str, unit: Optional[str] = None) -> dict[str, Any]:
        if self.demo_mode:
            return DEMO_KPIS
        filter_clause = "WHERE 1=1"
        params: tuple = ()
        if role in ("GU", "GA") and unit:
            filter_clause += " AND a.unit = ?"
            params = (unit,)
        rows = self._execute(
            f"""
            SELECT
                COUNT(DISTINCT a.agent_id)                      TotalAgents,
                SUM(p.production_amount)                        MonthlyProduction,
                SUM(p.target_amount)                            MonthlyTarget,
                CAST(SUM(p.production_amount) * 100.0
                     / NULLIF(SUM(p.target_amount), 0) AS DECIMAL(5,1)) AchievementPct
            FROM agents a
            JOIN production_monthly p ON a.agent_id = p.agent_id
            {filter_clause}
            AND p.period_month = MONTH(GETDATE())
            AND p.period_year  = YEAR(GETDATE())
            """,
            params,
        )
        return rows[0] if rows else DEMO_KPIS

    # ------------------------------------------------------------------
    # Rankings
    # ------------------------------------------------------------------
    def get_rankings(self, limit: int = 10) -> list[dict[str, Any]]:
        if self.demo_mode:
            return DEMO_RANKINGS[:limit]
        return self._execute(
            """
            SELECT TOP (?)
                ROW_NUMBER() OVER (ORDER BY p.production_amount DESC) Rank,
                a.full_name                                            AgentName,
                a.unit                                                 Unit,
                p.production_amount                                    Production,
                p.target_amount                                        Target,
                CAST(p.production_amount * 100.0
                     / NULLIF(p.target_amount, 0) AS DECIMAL(5,1))    Achievement
            FROM agents a
            JOIN production_monthly p ON a.agent_id = p.agent_id
            WHERE p.period_month = MONTH(GETDATE())
              AND p.period_year  = YEAR(GETDATE())
              AND a.active = 1
            ORDER BY p.production_amount DESC
            """,
            (limit,),
        )

    # ------------------------------------------------------------------
    # Consultants directory
    # ------------------------------------------------------------------
    def get_consultants(self, search: str = "", unit: str = "") -> list[dict[str, Any]]:
        if self.demo_mode:
            result = DEMO_AGENTS[:]
            if search:
                result = [a for a in result if search.lower() in a["full_name"].lower()]
            if unit:
                result = [a for a in result if a["unit"] == unit]
            return result
        params_list: list[Any] = []
        where = "WHERE a.active = 1"
        if search:
            where += " AND a.full_name LIKE ?"
            params_list.append(f"%{search}%")
        if unit:
            where += " AND a.unit = ?"
            params_list.append(unit)
        return self._execute(
            f"""
            SELECT
                a.agent_id   AgentID,
                a.full_name  FullName,
                a.email      Email,
                a.role       Role,
                a.unit       Unit,
                a.phone      Phone,
                a.start_date StartDate
            FROM agents a
            {where}
            ORDER BY a.full_name
            """,
            tuple(params_list),
        )

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            logger.info("Database connection closed")


db = Database()
