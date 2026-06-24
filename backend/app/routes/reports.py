import logging
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)

reports_bp = Blueprint('reports', __name__)
report_service = ReportService()


@reports_bp.route('', methods=['POST'])
@jwt_required()
def create_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['user_id', 'report_type', 'report_data']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        report = report_service.create_report(
            user_id=data['user_id'],
            report_type=data['report_type'],
            report_data=data['report_data']
        )

        logger.info(f'Created report: {report.id}')
        return jsonify(report.to_dict()), 201
    except Exception as e:
        logger.error(f'Error creating report: {str(e)}')
        return jsonify({'error': str(e)}), 500


@reports_bp.route('', methods=['GET'])
@jwt_required()
def get_reports():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        user_id = request.args.get('user_id', type=int)

        if user_id:
            result = report_service.get_reports_by_user_id(user_id, page, per_page)
        else:
            result = report_service.get_all_reports(page, per_page)

        return jsonify({
            'items': [report.to_dict() for report in result['items']],
            'total': result['total'],
            'page': result['page'],
            'per_page': result['per_page'],
            'pages': result['pages']
        })
    except Exception as e:
        logger.error(f'Error getting reports: {str(e)}')
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/<int:report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    try:
        report = report_service.get_report_by_id(report_id)
        if not report:
            return jsonify({'error': 'Report not found'}), 404
        return jsonify(report.to_dict())
    except Exception as e:
        logger.error(f'Error getting report: {str(e)}')
        return jsonify({'error': str(e)}), 500
