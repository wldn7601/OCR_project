# routes/health.py
from flask import Blueprint
health_bp = Blueprint("health", __name__)

@bp.route("/health")
def health():
    return {"status": "ok"}, 200