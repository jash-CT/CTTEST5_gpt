import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")

from app.main import create_app
from app.extensions import db


def make_auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}


def test_customer_cannot_approve():
    app = create_app()
    with app.app_context():
        db.create_all()
        client = app.test_client()

        # Register and login customer
        client.post("/auth/register", json={"email": "c1@example.com", "full_name": "C1", "password": "CustPass123$"})
        login = client.post("/auth/login", json={"email": "c1@example.com", "password": "CustPass123$"})
        assert login.status_code == 200
        token = login.get_json().get("access_token")

        # Create a loan as the customer
        resp = client.post("/loans/apply", json={"amount": 1000.0, "income": 5000.0, "credit_score": 650}, headers=make_auth_header(token))
        assert resp.status_code == 201
        loan_id = resp.get_json().get("id")

        # Customer attempts to approve their own loan
        resp = client.put(f"/loans/{loan_id}/approve", headers=make_auth_header(token))
        assert resp.status_code == 403 or resp.status_code == 401
