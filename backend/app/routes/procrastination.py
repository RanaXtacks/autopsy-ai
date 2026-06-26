from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.procrastination_service import ProcrastinationService
from app.models.procrastination import ProcrastinationPattern

procrastination_bp = Blueprint('procrastination', __name__)

@procrastination_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_patterns():
    current_user_id = int(get_jwt_identity())
    try:
        patterns = ProcrastinationService.generate_patterns_for_user(current_user_id)
        return jsonify({
            "message": "Procrastination patterns detected successfully",
            "count": len(patterns),
            "patterns": [p.to_dict() for p in patterns]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@procrastination_bp.route('', methods=['GET'])
@jwt_required()
def get_patterns():
    current_user_id = int(get_jwt_identity())
    patterns = ProcrastinationService.get_patterns(current_user_id)
    return jsonify({"patterns": [p.to_dict() for p in patterns]}), 200

@procrastination_bp.route('/top', methods=['GET'])
@jwt_required()
def get_top_distractions():
    current_user_id = int(get_jwt_identity())
    patterns = ProcrastinationService.get_top_distractions(current_user_id)
    return jsonify({"patterns": [p.to_dict() for p in patterns]}), 200

@procrastination_bp.route('/timeline', methods=['GET'])
@jwt_required()
def get_timeline():
    # Placeholder for focus breakdown timeline (could combine patterns grouped by day)
    current_user_id = int(get_jwt_identity())
    patterns = ProcrastinationService.get_patterns(current_user_id)
    return jsonify({"patterns": [p.to_dict() for p in patterns]}), 200

@procrastination_bp.route('/lost-time', methods=['GET'])
@jwt_required()
def get_lost_time():
    current_user_id = int(get_jwt_identity())
    metrics = ProcrastinationService.get_time_loss_metrics(current_user_id)
    return jsonify(metrics), 200
