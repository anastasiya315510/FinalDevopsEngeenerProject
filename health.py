"""
This module handles the health and readiness checks for the Flask application.
It defines a Blueprint with endpoints for liveness and readiness probes.
"""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/healthz")
def healthz():
    """
    Liveness endpoint to indicate the application is running.

    Returns:
        tuple: JSON response with status and HTTP 200
    """
    return jsonify(status="ok"), 200

@health_bp.route("/ready")
def ready():
    """
    Readiness endpoint to indicate the application is ready to serve requests.
    Add additional checks here for DB or cache readiness if needed.

    Returns:
        tuple: JSON response with status and HTTP 200
    """
    return jsonify(status="ready"), 200
