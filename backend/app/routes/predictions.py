from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.prediction_service import PredictionService

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_predictions():
    current_user_id = int(get_jwt_identity())
    try:
        preds = PredictionService.generate_predictions(current_user_id)
        return jsonify({
            "message": "Focus predictions generated successfully",
            "predictions": [p.to_dict() for p in preds]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@predictions_bp.route('/tomorrow', methods=['GET'])
@jwt_required()
def get_tomorrow_predictions():
    current_user_id = int(get_jwt_identity())
    preds = PredictionService.get_tomorrow_predictions(current_user_id)
    return jsonify({"predictions": [p.to_dict() for p in preds]}), 200

@predictions_bp.route('/chronotype', methods=['GET'])
@jwt_required()
def get_chronotype():
    current_user_id = int(get_jwt_identity())
    chronotype = PredictionService.get_chronotype(current_user_id)
    return jsonify({"chronotype": chronotype}), 200
