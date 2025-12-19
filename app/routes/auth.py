from flask import Blueprint, request, jsonify, current_app
from app.schemas.user_schema import RegisterSchema, LoginSchema
from app.services.auth_service import register_user, authenticate_user
from app.extensions import limiter
from marshmallow import ValidationError

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
@limiter.limit(lambda: current_app.config.get("RATE_LIMIT_AUTH"))
def register():
    try:
        data = RegisterSchema().load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    try:
        user = register_user(email=data["email"], full_name=data["full_name"], password=data["password"])
    except Exception:
        # Do not leak DB details; return generic message
        return jsonify({"msg": "Registration failed"}), 400

    return jsonify({"id": user.id, "email": user.email}), 201


@bp.route("/login", methods=["POST"])
@limiter.limit(lambda: current_app.config.get("RATE_LIMIT_AUTH"))
def login():
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    ip = request.remote_addr
    result = authenticate_user(email=data["email"], password=data["password"], ip=ip)
    if not result:
        return jsonify({"msg": "Bad credentials or account locked"}), 401

    user = result["user"]
    tokens = result["tokens"]
    return jsonify({"user": {"id": user.id, "email": user.email, "role": user.role}, **tokens}), 200
