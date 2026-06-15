from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.data_processor import process_user_data

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_data():
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    
    # In a real app, we would save the file and process it
    # For now, we'll just simulate processing
    results = process_user_data(file)
    
    return jsonify(results), 200

@analytics_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    # Placeholder for getting stored analytics summary
    return jsonify({"summary": "Behavioral patterns analysis complete."}), 200
