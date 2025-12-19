import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")

from app.main import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
    client = app.test_client()
    # register and login
    reg = client.post('/auth/register', json={"email":"cust@example.com","full_name":"Customer","password":"CustPass123$"})
    print('register status', reg.status_code, reg.get_json() if reg.data else None)
    r = client.post('/auth/login', json={"email":"cust@example.com","password":"CustPass123$"})
    print('login status', r.status_code, r.get_json())
    token = r.get_json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    resp = client.post('/loans/apply', json={"amount":5000.0,"income":60000.0,"credit_score":720}, headers=headers)
    print('apply status', resp.status_code)
    try:
        print('body', resp.get_json())
    except Exception:
        print('body raw', resp.data)
