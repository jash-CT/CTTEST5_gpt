from app.extensions import db
from app.models.loan import Loan, LoanStatus
from app.models.audit_log import AuditLog
from app.services.risk_engine import compute_risk_score
from datetime import datetime, timezone


def submit_loan(applicant_id: int, amount: float, income: float, credit_score: int, purpose: str, ip: str) -> Loan:
    loan = Loan(applicant_id=applicant_id, amount=amount, income=income, credit_score=credit_score, purpose=purpose)
    # compute initial risk
    loan.risk_score = compute_risk_score(credit_score, income, amount)
    loan.status = LoanStatus.SUBMITTED.value
    db.session.add(loan)
    db.session.add(AuditLog(user_id=applicant_id, role="customer", action="loan_submitted", ip=ip, details=f"loan_id_temp"))
    db.session.commit()
    return loan


def get_loans_for_user(user_id: int):
    return Loan.query.filter_by(applicant_id=user_id).order_by(Loan.created_at.desc()).all()


def approve_loan(loan_id: int, approver_id: int, approver_role: str, ip: str):
    loan = db.session.get(Loan, loan_id)
    if loan is None:
        return None
    if loan.status not in (LoanStatus.SUBMITTED.value, LoanStatus.UNDER_REVIEW.value):
        return None
    loan.status = LoanStatus.APPROVED.value
    loan.updated_at = datetime.now(timezone.utc)
    db.session.add(loan)
    db.session.add(AuditLog(user_id=approver_id, role=approver_role, action="loan_approved", ip=ip, details=f"loan_id={loan_id}"))
    db.session.commit()
    return loan


def reject_loan(loan_id: int, approver_id: int, approver_role: str, ip: str):
    loan = db.session.get(Loan, loan_id)
    if loan is None:
        return None
    if loan.status not in (LoanStatus.SUBMITTED.value, LoanStatus.UNDER_REVIEW.value):
        return None
    loan.status = LoanStatus.REJECTED.value
    loan.updated_at = datetime.now(timezone.utc)
    db.session.add(loan)
    db.session.add(AuditLog(user_id=approver_id, role=approver_role, action="loan_rejected", ip=ip, details=f"loan_id={loan_id}"))
    db.session.commit()
    return loan
