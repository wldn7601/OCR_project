# routes/health_routes.py
from flask import Blueprint
health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health():
    return {"status": "ok"}, 200