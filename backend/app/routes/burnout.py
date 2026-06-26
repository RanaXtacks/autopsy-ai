from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.burnout_service import BurnoutService

burnout_bp = Blueprint('burnout', __name__)

@burnout_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_assessment():
    current_user_id = int(get_jwt_identity())
    try:
        assessment = BurnoutService.generate_assessment(current_user_id)
        return jsonify({
            "message": "Burnout assessment generated successfully",
            "assessment": assessment.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@burnout_bp.route('/current', methods=['GET'])
@jwt_required()
def get_current_assessment():
    current_user_id = int(get_jwt_identity())
    assessment = BurnoutService.get_latest_assessment(current_user_id)
    if assessment:
        return jsonify(assessment.to_dict()), 200
    return jsonify({"message": "No assessment found"}), 404

@burnout_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    current_user_id = int(get_jwt_identity())
    history = BurnoutService.get_history(current_user_id)
    return jsonify({"history": [a.to_dict() for a in history]}), 200

@burnout_bp.route('/risk-factors', methods=['GET'])
@jwt_required()
def get_risk_factors():
    current_user_id = int(get_jwt_identity())
    factors = BurnoutService.get_risk_factors(current_user_id)
    return jsonify({"risk_factors": factors}), 200
