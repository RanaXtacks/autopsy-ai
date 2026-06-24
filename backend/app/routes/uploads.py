import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.upload_service import UploadService

logger = logging.getLogger(__name__)

uploads_bp = Blueprint('uploads', __name__)
upload_service = UploadService()


@uploads_bp.route('', methods=['POST'])
@jwt_required()
def create_upload():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['user_id', 'file_name', 'file_type', 'file_size']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        upload = upload_service.create_upload(
            user_id=data['user_id'],
            file_name=data['file_name'],
            file_type=data['file_type'],
            file_size=data['file_size']
        )

        logger.info(f'Created upload: {upload.id}')
        return jsonify(upload.to_dict()), 201
    except Exception as e:
        logger.error(f'Error creating upload: {str(e)}')
        return jsonify({'error': str(e)}), 500


@uploads_bp.route('', methods=['GET'])
@jwt_required()
def get_uploads():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        user_id = request.args.get('user_id', type=int)

        if user_id:
            result = upload_service.get_uploads_by_user_id(user_id, page, per_page)
        else:
            result = upload_service.get_all_uploads(page, per_page)

        return jsonify({
            'items': [upload.to_dict() for upload in result['items']],
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'pages': result['pages']
        })
    except Exception as e:
        logger.error(f'Error getting uploads: {str(e)}')
        return jsonify({'error': str(e)}), 500


@uploads_bp.route('/<int:upload_id>', methods=['GET'])
@jwt_required()
def get_upload(upload_id):
    try:
        upload = upload_service.get_upload_by_id(upload_id)
        if not upload:
            return jsonify({'error': 'Upload not found'}), 404
        return jsonify(upload.to_dict())
    except Exception as e:
        logger.error(f'Error getting upload: {str(e)}')
        return jsonify({'error': str(e)}), 500
