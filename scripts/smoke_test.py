import os
import sys
# Ensure repo root is on sys.path when this script is executed from the scripts/ folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Safety: require explicit opt-in to use development-only secrets in this script.
# To run this smoke test locally set ALLOW_SMOKE_TEST=1 in your environment.
if os.environ.get("ALLOW_SMOKE_TEST") == "1":
    os.environ.setdefault("SECRET_KEY", "dev-secret-not-for-prod")
    os.environ.setdefault("JWT_SECRET_KEY", "dev-jwt-secret-not-for-prod")
else:
    print("Smoke test requires ALLOW_SMOKE_TEST=1 to run with dev-only secrets. Exiting.")
    raise SystemExit(1)

from app.main import create_app
from app.extensions import db
from app.services.auth_service import register_user, authenticate_user


def run():
    app = create_app()
    # Use app context to access extensions and models
    with app.app_context():
        # Create tables (safe for sqlite dev smoke test)
        db.create_all()

        # Register a test user
        email = "testuser@example.com"
        try:
            user = register_user(email=email, full_name="Test User", password="StrongPassw0rd$")
            print(f"Registered user id={user.id} email={user.email}")
        except Exception as e:
            print("Registration failed or user exists; continuing")

        # Attempt authentication
        result = authenticate_user(email=email, password="StrongPassw0rd$", ip="127.0.0.1")
        if result:
            print("Authentication succeeded; tokens present")
            print({k: (v[:10] + '...') if k.endswith('_token') else v for k, v in result['tokens'].items()})
        else:
            print("Authentication failed")


if __name__ == "__main__":
    run()
