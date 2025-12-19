from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.extensions import db


class RoleEnum(str, Enum):
    CUSTOMER = "customer"
    LOAN_OFFICER = "loan_officer"
    ADMIN = "admin"


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default=RoleEnum.CUSTOMER.value)
    is_active = Column(Boolean, default=True, nullable=False)
    failed_logins = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    loans = relationship("Loan", back_populates="applicant")

    def is_admin(self) -> bool:
        return self.role == RoleEnum.ADMIN.value

    def is_loan_officer(self) -> bool:
        return self.role == RoleEnum.LOAN_OFFICER.value

    def is_customer(self) -> bool:
        return self.role == RoleEnum.CUSTOMER.value
