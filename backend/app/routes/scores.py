from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.scoring_service import ScoringService
from datetime import date, datetime

scores_bp = Blueprint('scores', __name__)

@scores_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_scores():
    try:
        current_user_id = int(get_jwt_identity())
        target_date_str = request.json.get('date', None) if request.is_json else None
        
        if target_date_str:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        else:
            target_date = date.today()
            
        score = ScoringService.generate_scores_for_date(current_user_id, target_date)
        return jsonify({"message": f"Scores generated for {target_date}", "score": score.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scores_bp.route('/today', methods=['GET'])
@jwt_required()
def get_today_scores():
    try:
        current_user_id = int(get_jwt_identity())
        data = ScoringService.get_today_scores(current_user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scores_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    try:
        current_user_id = int(get_jwt_identity())
        days = request.args.get('days', 30, type=int)
        data = ScoringService.get_history(current_user_id, days)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scores_bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    try:
        current_user_id = int(get_jwt_identity())
        data = ScoringService.get_trends(current_user_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scores_bp.route('/comparison', methods=['GET'])
@jwt_required()
def get_comparison():
    # Helper endpoint for dashboard
    try:
        current_user_id = int(get_jwt_identity())
        trends = ScoringService.get_trends(current_user_id)
        return jsonify(trends), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
