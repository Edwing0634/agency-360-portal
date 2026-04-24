"""
Main Flask application entry point.
Run as a web server with `flask run` or as a desktop app via PyWebView with `python app.py`.
"""

import logging
import sys
import threading
import os
from flask import Flask
from config import config
from models.database import db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.api import api_bp

logging.basicConfig(
    level=logging.DEBUG if config.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    db.connect()
    return app


def _run_flask(app: Flask) -> None:
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def launch_desktop(app: Flask) -> None:
    """Launch the app inside a native window via PyWebView."""
    import webview

    flask_thread = threading.Thread(target=_run_flask, args=(app,), daemon=True)
    flask_thread.start()

    webview.create_window(
        title=config.APP_TITLE,
        url="http://127.0.0.1:5000/",
        width=config.WINDOW_WIDTH,
        height=config.WINDOW_HEIGHT,
        resizable=True,
        min_size=(1024, 600),
    )
    webview.start()


if __name__ == "__main__":
    application = create_app()
    desktop_mode = "--web" not in sys.argv and not os.getenv("FLASK_RUN_FROM_CLI")
    if desktop_mode:
        logger.info("Starting in desktop mode (PyWebView)")
        launch_desktop(application)
    else:
        logger.info("Starting in web mode")
        application.run(debug=config.DEBUG)
