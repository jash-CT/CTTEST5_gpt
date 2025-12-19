from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.security.rbac import role_required
from app.models.audit_log import AuditLog

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/audit-logs", methods=["GET"])
@role_required("admin")
def audit_logs():
    # Simple pagination
    page = int(request.args.get("page", 1))
    per_page = min(int(request.args.get("per_page", 50)), 200)
    q = AuditLog.query.order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = [
        {
            "id": a.id,
            "timestamp": a.timestamp.isoformat(),
            "user_id": a.user_id,
            "role": a.role,
            "action": a.action,
            "ip": a.ip,
            "details": a.details,
        }
        for a in q.items
    ]
    return jsonify({"items": items, "total": q.total, "pages": q.pages}), 200
