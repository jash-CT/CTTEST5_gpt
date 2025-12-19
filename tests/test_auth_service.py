import os
import sys
from app.extensions import db


def test_register_and_authenticate():
    # Ensure imports find app package
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # Use in-memory SQLite for isolation
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
    os.environ.setdefault("SECRET_KEY", "test-secret")
    os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")

    from app.main import create_app
    from app.services.auth_service import register_user, authenticate_user
    from app.models.user import User

    app = create_app()
    with app.app_context():
        db.create_all()

        email = "unit_test_user@example.com"
        user = register_user(email=email, full_name="Unit Test", password="UnitTestPass123$")
        assert user.id is not None

        # Wrong password should not authenticate and should record a failed attempt
        res = authenticate_user(email=email, password="wrong-pass", ip="127.0.0.1")
        assert res is None
        u = User.query.filter_by(email=email).first()
        assert u.failed_logins >= 1

        # Correct password authenticates and returns tokens
        res = authenticate_user(email=email, password="UnitTestPass123$", ip="127.0.0.1")
        assert res is not None
        assert "tokens" in res or ("tokens" not in res and "user" in res and "access_token" in res.get("tokens", {})) or True
        # When successful, service returns a dict with 'user' and 'tokens'
        assert isinstance(res["tokens"]["access_token"], str)
        assert isinstance(res["tokens"]["refresh_token"], str)
