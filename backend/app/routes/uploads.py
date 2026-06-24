import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.upload_service import UploadService

logger = logging.getLogger(__name__)

uploads_bp = Blueprint('uploads', __name__)
upload_service = UploadService()


@uploads_bp.route('', methods=['POST'])
@jwt_required()
def create_upload():
    try:
        current_user_id = int(get_jwt_identity())
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
            
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        upload = upload_service.create_upload(
            user_id=current_user_id,
            file=file,
            source='api'
        )

        logger.info(f'Created upload: {upload.id} for user {current_user_id}')
        return jsonify(upload.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error creating upload: {str(e)}')
        return jsonify({'error': 'Internal server error processing file'}), 500


@uploads_bp.route('', methods=['GET'])
@jwt_required()
def get_uploads():
    try:
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # Force scoping to current_user_id for security
        result = upload_service.get_uploads_by_user_id(current_user_id, page, per_page)

        return jsonify({
            'items': [upload.to_dict() for upload in result['items']],
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'pages': result['pages']
        })
    except Exception as e:
        logger.error(f'Error getting uploads: {str(e)}')
        return jsonify({'error': 'Internal server error retrieving uploads'}), 500


@uploads_bp.route('/<int:upload_id>', methods=['GET'])
@jwt_required()
def get_upload(upload_id):
    try:
        current_user_id = int(get_jwt_identity())
        upload = upload_service.get_upload_by_id(upload_id)
        
        if not upload:
            return jsonify({'error': 'Upload not found'}), 404
            
        # Security Ownership Check
        if upload.user_id != current_user_id:
            logger.warning(f'User {current_user_id} attempted to access unowned upload {upload_id}')
            return jsonify({'error': 'Forbidden access'}), 403
            
        return jsonify(upload.to_dict())
    except Exception as e:
        logger.error(f'Error getting upload: {str(e)}')
        return jsonify({'error': 'Internal server error retrieving upload'}), 500


@uploads_bp.route('/<int:upload_id>', methods=['DELETE'])
@jwt_required()
def delete_upload(upload_id):
    try:
        current_user_id = int(get_jwt_identity())
        success = upload_service.delete_upload(upload_id, current_user_id)
        if not success:
            return jsonify({'error': 'Upload not found or forbidden access'}), 404
            
        return jsonify({'success': True, 'message': 'Upload deleted successfully'})
    except Exception as e:
        logger.error(f'Error deleting upload: {str(e)}')
        return jsonify({'error': 'Internal server error deleting upload'}), 500
