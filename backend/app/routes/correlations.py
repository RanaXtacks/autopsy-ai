from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.correlation_service import CorrelationService

correlations_bp = Blueprint('correlations', __name__)

@correlations_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_correlations():
    current_user_id = int(get_jwt_identity())
    try:
        correlations = CorrelationService.generate_correlations_for_user(current_user_id)
        return jsonify({
            "message": "Correlations detected successfully",
            "count": len(correlations),
            "correlations": [c.to_dict() for c in correlations]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@correlations_bp.route('', methods=['GET'])
@jwt_required()
def get_correlations():
    current_user_id = int(get_jwt_identity())
    correlations = CorrelationService.get_correlations(current_user_id)
    return jsonify({"correlations": [c.to_dict() for c in correlations]}), 200

@correlations_bp.route('/top', methods=['GET'])
@jwt_required()
def get_top_correlations():
    current_user_id = int(get_jwt_identity())
    correlations = CorrelationService.get_top_correlations(current_user_id)
    return jsonify({"correlations": [c.to_dict() for c in correlations]}), 200

@correlations_bp.route('/negative', methods=['GET'])
@jwt_required()
def get_negative_correlations():
    current_user_id = int(get_jwt_identity())
    correlations = CorrelationService.get_negative_correlations(current_user_id)
    return jsonify({"correlations": [c.to_dict() for c in correlations]}), 200

@correlations_bp.route('/positive', methods=['GET'])
@jwt_required()
def get_positive_correlations():
    current_user_id = int(get_jwt_identity())
    correlations = CorrelationService.get_positive_correlations(current_user_id)
    return jsonify({"correlations": [c.to_dict() for c in correlations]}), 200
