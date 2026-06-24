from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    # Placeholder for getting stored analytics summary
    return jsonify({"summary": "Behavioral patterns analysis complete."}), 200
