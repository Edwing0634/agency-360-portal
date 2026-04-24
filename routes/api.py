"""JSON API endpoints consumed by the frontend."""

import logging
from flask import Blueprint, jsonify, request, session
from models.database import db
from routes.auth import login_required

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/kpis")
@login_required
def kpis():
    role = session.get("role", "")
    unit = session.get("unit", "")
    data = db.get_dashboard_kpis(role, unit)
    return jsonify(data)


@api_bp.route("/rankings")
@login_required
def rankings():
    limit = int(request.args.get("limit", 10))
    data = db.get_rankings(limit=limit)
    return jsonify(data)


@api_bp.route("/consultants")
@login_required
def consultants():
    search = request.args.get("q", "")
    unit = request.args.get("unit", "")
    data = db.get_consultants(search=search, unit=unit)
    return jsonify(data)


@api_bp.route("/copilot/chat", methods=["POST"])
@login_required
def copilot_chat():
    body = request.get_json(silent=True) or {}
    user_message: str = body.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    # Placeholder — wire to Azure OpenAI or any LLM in production
    response = _mock_copilot_response(user_message, session.get("role", ""))
    return jsonify({"reply": response})


def _mock_copilot_response(message: str, role: str) -> str:
    greetings = ["hi", "hello", "hey", "hola"]
    if any(g in message.lower() for g in greetings):
        return "Hello! I'm your Agency Copilot. Ask me about KPIs, rankings, or agent performance."
    if "ranking" in message.lower():
        return "The top performer this month is Miguel Torres with 115.5% achievement. 🏆"
    if "production" in message.lower():
        return "Current monthly production stands at $3.24B COP — 92.7% of the monthly target."
    return (
        f"I understand you're asking about: '{message}'. "
        "This feature will be connected to the AI backend in the next release. "
        "For now, try asking about rankings or production."
    )
