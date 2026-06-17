from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
from app.logger import setup_logging

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    if config_name is None:
        config_name = 'default'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    setup_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from app.routes.auth import auth_bp
    from app.routes.analytics import analytics_bp
    from app.routes.health import health_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(analytics_bp, url_prefix='/api/analytics')

    @app.errorhandler(400)
    def bad_request(error):
        app.logger.error(f'Bad Request: {error}')
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        app.logger.error(f'Unauthorized: {error}')
        return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

    @app.errorhandler(404)
    def not_found(error):
        app.logger.error(f'Not Found: {error}')
        return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f'Internal Server Error: {error}')
        return jsonify({'error': 'Internal Server Error', 'message': 'Something went wrong on our end'}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled Exception: {error}', exc_info=True)
        return jsonify({'error': 'Internal Server Error', 'message': 'Something went wrong'}), 500

    return app
