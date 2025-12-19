from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Rate limiter will be initialized with app in factory
limiter = Limiter(key_func=get_remote_address, default_limits=[])

# Talisman will be used to set secure headers (CSP and others can be set per app needs)
talisman = Talisman()
