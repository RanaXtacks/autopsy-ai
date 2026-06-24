import os
import uuid
import logging
from typing import Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app
from app.repositories import UploadRepository
from app.models import Upload
from app import db

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'csv'}

class UploadService:
    def __init__(self):
        self.upload_repo = UploadRepository()
        
    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
    def create_upload(self, user_id: int, file: FileStorage, source: str = 'web') -> Upload:
        if not file or not file.filename:
            raise ValueError("No file provided")
            
        if not self.allowed_file(file.filename):
            raise ValueError("Invalid file extension. Only CSV files are allowed.")
            
        # Secure original filename
        original_filename = secure_filename(file.filename)
        if not original_filename:
            original_filename = "unnamed.csv"
            
        # Generate unique storage filename
        stored_filename = f"{uuid.uuid4().hex}_{original_filename}"
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, stored_filename)
        
        # Save file to disk
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            os.remove(file_path)
            raise ValueError("File is empty")
            
        # Check against MAX_CONTENT_LENGTH
        if file_size > current_app.config['MAX_CONTENT_LENGTH']:
            os.remove(file_path)
            raise ValueError("File exceeds maximum allowed size (10MB)")
            
        # Create DB record
        upload = Upload(
            user_id=user_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            mime_type=file.mimetype or 'text/csv',
            file_size=file_size,
            status='uploaded',
            upload_source=source
        )
        
        self.upload_repo.create(upload)
        
        logger.info(f'Upload created for user {user_id}: {original_filename} -> {stored_filename}')
        return upload
        
    def get_all_uploads(self, page: int = 1, per_page: int = 20):
        return self.upload_repo.get_all(page, per_page)
        
    def get_uploads_by_user_id(self, user_id: int, page: int = 1, per_page: int = 20):
        return self.upload_repo.get_by_user_id(user_id, page, per_page)
        
    def get_upload_by_id(self, upload_id: int) -> Optional[Upload]:
        return self.upload_repo.get_by_id(upload_id)
        
    def update_upload_status(self, upload_id: int, status: str) -> Optional[Upload]:
        upload = self.upload_repo.get_by_id(upload_id)
        if not upload:
            return None
        upload.status = status
        db.session.commit()
        logger.info(f'Upload {upload_id} status updated to {status}')
        return upload

    def delete_upload(self, upload_id: int, user_id: int) -> bool:
        upload = self.upload_repo.get_by_id(upload_id)
        if not upload or upload.user_id != user_id:
            return False
            
        # Delete from disk
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, upload.stored_filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            
        # Delete from DB
        db.session.delete(upload)
        db.session.commit()
        logger.info(f'Upload {upload_id} deleted by user {user_id}')
        return True
