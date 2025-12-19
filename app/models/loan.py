from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class LoanStatus(str, Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class Loan(db.Model):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True)
    applicant_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    income = Column(Float, nullable=False)
    credit_score = Column(Integer, nullable=False)
    purpose = Column(String(255), nullable=True)
    status = Column(String(32), nullable=False, default=LoanStatus.SUBMITTED.value)
    risk_score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    applicant = relationship("User", back_populates="loans")
