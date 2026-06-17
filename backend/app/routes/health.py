from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    health_status = {
        'status': 'healthy',
        'database': 'unknown'
    }

    try:
        db.session.execute(text('SELECT 1'))
        health_status['database'] = 'healthy'
    except Exception as e:
        health_status['database'] = 'unhealthy'
        health_status['status'] = 'unhealthy'
        health_status['error'] = str(e)

    return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 503
