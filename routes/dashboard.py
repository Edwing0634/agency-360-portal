"""Dashboard and main content routes."""

import logging
from flask import Blueprint, render_template, session, request, jsonify
from models.database import db
from routes.auth import login_required

logger = logging.getLogger(__name__)
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    role = session.get("role", "")
    unit = session.get("unit", "")
    kpis = db.get_dashboard_kpis(role, unit)
    rankings = db.get_rankings(limit=5)
    template = "dashboard_admin.html" if role == "Admin" else "dashboard_ga.html"
    return render_template(template, kpis=kpis, rankings=rankings, role=role)


@dashboard_bp.route("/rankings")
@login_required
def rankings():
    top = db.get_rankings(limit=10)
    return render_template("rankings.html", rankings=top)


@dashboard_bp.route("/consultants")
@login_required
def consultants():
    search = request.args.get("q", "")
    unit = request.args.get("unit", "")
    agents = db.get_consultants(search=search, unit=unit)
    units = list({a["unit"] for a in db.get_consultants()})
    return render_template("consultants.html", agents=agents, units=sorted(units),
                           search=search, selected_unit=unit)


@dashboard_bp.route("/copilot")
@login_required
def copilot():
    return render_template("copilot.html")
