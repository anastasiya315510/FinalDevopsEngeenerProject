from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)

@health_bp.route("/healthz")
def healthz():
    # Liveness check
    return jsonify(status="ok"), 200

@health_bp.route("/ready")
def ready():
    # Readiness check (can add DB/cache checks here later)
    return jsonify(status="ready"), 200
