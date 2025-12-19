from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    role = Column(String(32), nullable=True)
    action = Column(String(128), nullable=False)
    ip = Column(String(45), nullable=True)
    details = Column(Text, nullable=True)

    user = relationship("User")

    # Immutable: do not provide update operations in services; only inserts allowed
