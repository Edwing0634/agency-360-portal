"""Authentication routes — login, logout, session management."""

import logging
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.database import db
from config import config

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


def _validate_domain(email: str) -> bool:
    return email.lower().endswith(f"@{config.COMPANY_DOMAIN}")


@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET"])
def login_page():
    if session.get("agent_id"):
        return redirect(url_for("dashboard.index"))
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    email: str = request.form.get("email", "").strip().lower()
    password: str = request.form.get("password", "")

    if not email or not password:
        flash("Email and password are required.", "error")
        return render_template("login.html")

    if not _validate_domain(email):
        flash(f"Access restricted to @{config.COMPANY_DOMAIN} accounts.", "error")
        logger.warning("Login attempt with unauthorized domain: %s", email)
        return render_template("login.html")

    agent = db.get_agent_by_email(email)
    if not agent:
        flash("Invalid credentials. Please try again.", "error")
        logger.warning("Failed login attempt for: %s", email)
        return render_template("login.html")

    # Demo mode accepts any non-empty password; production would hash-check
    if not db.demo_mode and not _check_password(password, agent.get("password_hash", "")):
        flash("Invalid credentials. Please try again.", "error")
        return render_template("login.html")

    session["agent_id"] = agent["agent_id"]
    session["full_name"] = agent["full_name"]
    session["email"] = agent["email"]
    session["role"] = agent["role"]
    session["unit"] = agent.get("unit", "")
    logger.info("Login successful: %s (%s)", email, agent["role"])
    return redirect(url_for("dashboard.index"))


@auth_bp.route("/logout")
def logout():
    agent_email = session.get("email", "unknown")
    session.clear()
    logger.info("Logout: %s", agent_email)
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login_page"))


def _check_password(plain: str, hashed: str) -> bool:
    """Placeholder — replace with werkzeug.security.check_password_hash in production."""
    import hashlib
    return hashlib.sha256(plain.encode()).hexdigest() == hashed


def login_required(f):
    """Decorator that redirects unauthenticated requests to login."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("agent_id"):
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)

    return decorated


def role_required(*roles: str):
    """Decorator that restricts a route to specific roles."""
    from functools import wraps

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get("role") not in roles:
                flash("You do not have permission to access this page.", "error")
                return redirect(url_for("dashboard.index"))
            return f(*args, **kwargs)
        return decorated
    return decorator
