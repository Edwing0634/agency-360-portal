# Architecture — Agency 360 Portal

## Overview

```
┌─────────────────────────────────────────────────────┐
│                    End User                         │
│          (Desktop App via PyWebView)                │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP (localhost:5000)
┌───────────────────────▼─────────────────────────────┐
│              Flask Application Layer                │
│  ┌──────────┐  ┌───────────────┐  ┌─────────────┐  │
│  │  auth.py │  │ dashboard.py  │  │   api.py    │  │
│  │  /login  │  │ /dashboard    │  │ /api/kpis   │  │
│  │  /logout │  │ /rankings     │  │ /api/rank   │  │
│  └────┬─────┘  │ /consultants  │  │ /api/chat   │  │
│       │        └───────┬───────┘  └──────┬──────┘  │
│       └────────────────┼─────────────────┘         │
│                        │                            │
│  ┌─────────────────────▼──────────────────────────┐ │
│  │            Database Layer (models/)             │ │
│  │  database.py — pyodbc + demo data fallback     │ │
│  └─────────────────────┬──────────────────────────┘ │
└────────────────────────┼────────────────────────────┘
                         │
              ┌──────────▼──────────┐
              │   SQL Server DB     │
              │  (agency360_db)     │
              │  tables: agents,    │
              │  production_monthly │
              └─────────────────────┘
```

## Role Access Matrix

| Feature         | Admin | Senior | GA  | GU  |
|----------------|-------|--------|-----|-----|
| Full dashboard | ✅    | ❌     | ❌  | ❌  |
| Unit dashboard | ✅    | ✅     | ✅  | ✅  |
| All rankings   | ✅    | ✅     | ❌  | ❌  |
| Unit rankings  | ✅    | ✅     | ✅  | ✅  |
| Consultants    | ✅    | ✅     | ✅  | ✅  |
| AI Copilot     | ✅    | ✅     | ✅  | ✅  |

## Demo Mode

When `DB_SERVER` is not configured, the app runs in **demo mode** using
hardcoded sample data. All routes and features work without a database.
