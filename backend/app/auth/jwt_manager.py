from flask import jsonify
from app import db
from app.models import TokenBlocklist
from flask_jwt_extended import JWTManager

def configure_jwt(jwt: JWTManager):
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        """
        Callback function to check if a JWT exists in the database blocklist
        """
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "The token has been revoked",
            "error": "token_revoked"
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "The token has expired",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "success": False,
            "message": "Signature verification failed",
            "error": "invalid_token"
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "success": False,
            "message": "Request does not contain an access token",
            "error": "authorization_required"
        }), 401
