import os
import sys
import json
from app.extensions import db

# Ensure repo root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")

from app.main import create_app
from app.security.password import hash_password
from app.models.user import User


def make_auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_end_to_end_workflow():
    app = create_app()
    with app.app_context():
        db.create_all()
        client = app.test_client()

        # Register a customer via endpoint
        reg = client.post("/auth/register", json={
            "email": "cust@example.com",
            "full_name": "Customer",
            "password": "CustPass123$"
        })
        assert reg.status_code == 201

        # Login customer
        login = client.post("/auth/login", json={"email": "cust@example.com", "password": "CustPass123$"})
        assert login.status_code == 200
        data = login.get_json()
        access = data.get("access_token")
        assert access

        # Customer applies for a loan
        resp = client.post("/loans/apply", json={"amount": 5000.0, "income": 60000.0, "credit_score": 720}, headers=make_auth_header(access))
        assert resp.status_code == 201
        loan = resp.get_json()
        loan_id = loan.get("id")
        assert loan_id is not None

        # Ensure customer can list own loans
        resp = client.get("/loans/my", headers=make_auth_header(access))
        assert resp.status_code == 200
        items = resp.get_json()
        assert isinstance(items, list)

        # Create a loan officer user directly in DB
        lo_password = "OfficerPass123$"
        lo = User(email="lo@example.com", full_name="Officer", password_hash=hash_password(lo_password), role="loan_officer")
        db.session.add(lo)
        db.session.commit()

        # Login loan officer
        login = client.post("/auth/login", json={"email": "lo@example.com", "password": lo_password})
        assert login.status_code == 200
        lo_token = login.get_json().get("access_token")

        # Loan officer approves the loan
        resp = client.put(f"/loans/{loan_id}/approve", headers=make_auth_header(lo_token))
        assert resp.status_code == 200
        approved = resp.get_json()
        assert approved.get("status") == "APPROVED"

        # Create admin user
        admin_pwd = "AdminPass123$"
        admin = User(email="admin@example.com", full_name="Admin", password_hash=hash_password(admin_pwd), role="admin")
        db.session.add(admin)
        db.session.commit()

        # Login admin and fetch audit logs
        login = client.post("/auth/login", json={"email": "admin@example.com", "password": admin_pwd})
        assert login.status_code == 200
        admin_token = login.get_json().get("access_token")

        resp = client.get("/admin/audit-logs", headers=make_auth_header(admin_token))
        assert resp.status_code == 200
        body = resp.get_json()
        assert "items" in body
