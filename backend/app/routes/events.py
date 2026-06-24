import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.events import BehaviorEvent
from app import db

logger = logging.getLogger(__name__)
events_bp = Blueprint('events', __name__)

@events_bp.route('', methods=['GET'])
@jwt_required()
def get_events():
    try:
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # Optional filters
        source = request.args.get('source')
        category = request.args.get('category')
        
        query = BehaviorEvent.query.filter_by(user_id=current_user_id)
        
        if source:
            query = query.filter_by(source=source)
        if category:
            query = query.filter_by(category=category)
            
        # Order by timestamp descending
        query = query.order_by(BehaviorEvent.timestamp.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'items': [event.to_dict() for event in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        })
        
    except Exception as e:
        logger.error(f'Error retrieving events: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500
