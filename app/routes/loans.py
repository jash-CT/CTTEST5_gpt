from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.schemas.loan_schema import LoanApplySchema, LoanResponseSchema
from app.services.loan_service import submit_loan, get_loans_for_user, approve_loan, reject_loan
from app.security.rbac import role_required
from marshmallow import ValidationError

bp = Blueprint("loans", __name__, url_prefix="/loans")


@bp.route("/apply", methods=["POST"])
@jwt_required()
def apply():
    try:
        data = LoanApplySchema().load(request.get_json())
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400

    # `identity` is the JWT subject (string user id); additional claims contain role/email
    identity = get_jwt_identity()
    user_id = int(identity)
    ip = request.remote_addr
    loan = submit_loan(applicant_id=user_id, amount=data["amount"], income=data["income"], credit_score=data["credit_score"], purpose=data.get("purpose"), ip=ip)
    return jsonify(LoanResponseSchema().dump(loan)), 201


@bp.route("/my", methods=["GET"])
@jwt_required()
def my_loans():
    identity = get_jwt_identity()
    user_id = int(identity)
    loans = get_loans_for_user(user_id)
    return jsonify(LoanResponseSchema(many=True).dump(loans)), 200


@bp.route("/<int:loan_id>/approve", methods=["PUT"])
@role_required("loan_officer", "admin")
def approve(loan_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    res = approve_loan(loan_id=loan_id, approver_id=int(identity), approver_role=claims.get("role"), ip=request.remote_addr)
    if not res:
        return jsonify({"msg": "Unable to approve"}), 400
    return jsonify(LoanResponseSchema().dump(res)), 200


@bp.route("/<int:loan_id>/reject", methods=["PUT"])
@role_required("loan_officer", "admin")
def reject(loan_id):
    identity = get_jwt_identity()
    claims = get_jwt()
    res = reject_loan(loan_id=loan_id, approver_id=int(identity), approver_role=claims.get("role"), ip=request.remote_addr)
    if not res:
        return jsonify({"msg": "Unable to reject"}), 400
    return jsonify(LoanResponseSchema().dump(res)), 200
