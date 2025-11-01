import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from dashboard import dashboard_blueprint
from utils import timestamp_to_str
from health import health_bp
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

def create_app():
    """Create and configure the Flask application."""
    # Single Flask instance
    app = Flask(__name__)

    # -------------------------
    # Logging
    # -------------------------
    if not os.path.exists("logs"):
        os.makedirs("logs")

    error_handler = RotatingFileHandler("logs/error.log", maxBytes=1_000_000, backupCount=3)
    error_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_handler)

    usage_handler = RotatingFileHandler("logs/access.log", maxBytes=1_000_000, backupCount=3)
    usage_logger = logging.getLogger("usage")
    usage_logger.setLevel(logging.INFO)
    usage_logger.addHandler(usage_handler)

    @app.before_request
    def log_request_info():
        """Log each incoming request."""
        usage_logger.info("%s - %s %s", request.remote_addr, request.method, request.url)

    # -------------------------
    # Register blueprints
    # -------------------------
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(health_bp)

    # -------------------------
    # Custom Jinja filter
    # -------------------------
    app.jinja_env.filters["timestamp_to_str"] = timestamp_to_str

    # -------------------------
    # Prometheus metrics
    # -------------------------
    # Wrap the app AFTER all blueprints are registered
    metrics = PrometheusMetrics(app, path="/metrics")
    metrics.info("app_info", "Application info", version="dev")

    # Custom counter
    REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])

    @app.before_request
    def count_requests():
        """Increment custom request counter."""
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

    return app

if __name__ == "__main__":
    app = create_app()
    # Run app
    app.run(host="0.0.0.0", port=8000)
