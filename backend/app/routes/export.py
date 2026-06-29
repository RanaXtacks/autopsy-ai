from flask import Blueprint, jsonify, Response
import json

export_bp = Blueprint('export', __name__, url_prefix='/api/export')

@export_bp.route('/data', methods=['GET'])
def export_user_data():
    """
    Exports all user data as a structured JSON file.
    """
    # In a real application, this would query the DB for the user's records.
    # We are mocking the payload for the MVP.
    mock_dataset = {
        "user_profile": {
            "username": "AutopsyUser",
            "joined_at": "2023-01-15T12:00:00Z"
        },
        "habits": [
            {"id": 1, "name": "Late Night Coding", "score": 85},
            {"id": 2, "name": "Deep Work Block", "score": 92}
        ],
        "productivity_scores": [
            {"date": "2023-10-01", "score": 78},
            {"date": "2023-10-02", "score": 88}
        ]
    }
    
    response = Response(
        json.dumps(mock_dataset, indent=2),
        mimetype='application/json',
        headers={"Content-disposition": "attachment; filename=autopsy_ai_export.json"}
    )
    return response
