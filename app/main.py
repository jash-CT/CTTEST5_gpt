from flask import Flask, jsonify
from app.config import get_config
from app.extensions import db, migrate, jwt, limiter, talisman
from app.utils.logger import setup_logging
from app.routes.auth import bp as auth_bp
from app.routes.loans import bp as loans_bp
from app.routes.admin import bp as admin_bp
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app)

    # logging
    setup_logging(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(loans_bp)
    app.register_blueprint(admin_bp)

    # centralized error handling for JSON
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception("Unhandled exception")
        return jsonify({"msg": "Internal Server Error"}), 500

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app


if __name__ == "__main__":
    app = create_app()
    # DO NOT run with debug in production. Use WSGI server.
    app.run(host="0.0.0.0", port=5000)
