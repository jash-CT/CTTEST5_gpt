from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import IntegrityError
from flask import current_app
from app.extensions import db
from app.models.user import User, RoleEnum
from app.security.password import hash_password, verify_password
from app.models.audit_log import AuditLog
from app.security.jwt_utils import create_tokens

LOCKOUT_THRESHOLD = 5
LOCKOUT_PERIOD = timedelta(minutes=15)


def register_user(email: str, full_name: str, password: str) -> User:
    pw = hash_password(password)
    user = User(email=email.lower(), full_name=full_name, password_hash=pw, role=RoleEnum.CUSTOMER.value)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
    return user


def authenticate_user(email: str, password: str, ip: str):
    user = User.query.filter_by(email=email.lower()).first()
    if user is None:
        # Log failed attempt without revealing whether account exists
        log = AuditLog(user_id=None, role=None, action="login_failed", ip=ip, details=f"email={email}")
        db.session.add(log)
        db.session.commit()
        return None

    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        return None

    if not verify_password(user.password_hash, password):
        user.failed_logins += 1
        if user.failed_logins >= LOCKOUT_THRESHOLD:
            user.locked_until = datetime.now(timezone.utc) + LOCKOUT_PERIOD
        db.session.add(user)
        db.session.add(AuditLog(user_id=user.id, role=user.role, action="login_failed", ip=ip))
        db.session.commit()
        return None

    # successful auth
    user.failed_logins = 0
    user.locked_until = None
    db.session.add(user)
    db.session.add(AuditLog(user_id=user.id, role=user.role, action="login_success", ip=ip))
    db.session.commit()

    identity = {"user_id": user.id, "role": user.role, "email": user.email}
    tokens = create_tokens(identity)
    return {"user": user, "tokens": tokens}
