import os
import logging
from app import db
from app.models.core import Upload
from app.models.events import BehaviorEvent

from ..parsers.chrome_parser import ChromeParser
from ..parsers.github_parser import GitHubParser
from ..parsers.screentime_parser import ScreenTimeParser
from ..parsers.spotify_parser import SpotifyParser
from ..transformers.event_transformer import EventTransformer

logger = logging.getLogger(__name__)

class IngestionService:
    """
    Orchestrates the data pipeline for an uploaded file.
    """
    
    PARSERS = {
        'chrome': ChromeParser,
        'github': GitHubParser,
        'screentime': ScreenTimeParser,
        'spotify': SpotifyParser
    }
    
    TRANSFORMERS = {
        'chrome': EventTransformer.transform_chrome,
        'github': EventTransformer.transform_github,
        'screentime': EventTransformer.transform_screentime,
        'spotify': EventTransformer.transform_spotify
    }
    
    @staticmethod
    def process_upload(upload_id: int, user_id: int, source: str, upload_folder: str) -> dict:
        """
        Process the given upload_id synchronously.
        Updates Upload status accordingly.
        """
        upload = Upload.query.filter_by(id=upload_id, user_id=user_id).first()
        if not upload:
            return {'success': False, 'message': 'Upload not found or forbidden access'}
            
        if upload.status == 'completed':
            return {'success': False, 'message': 'Upload already processed'}
            
        if source not in IngestionService.PARSERS:
            return {'success': False, 'message': f'Unsupported source: {source}'}
            
        try:
            # Update status to processing
            upload.status = 'processing'
            db.session.commit()
            
            # File path
            file_path = os.path.join(upload_folder, upload.stored_filename)
            if not os.path.exists(file_path):
                raise FileNotFoundError('Physical file is missing from storage')
                
            # Parse
            parser_class = IngestionService.PARSERS[source]
            parser = parser_class(file_path)
            valid_rows = parser.process()
            
            if not valid_rows:
                raise ValueError('File contained no valid data rows matching the schema')
                
            # Transform
            transform_fn = IngestionService.TRANSFORMERS[source]
            transformed_events = transform_fn(valid_rows, user_id, upload_id)
            
            # Bulk Insert
            behavior_events = [BehaviorEvent(**event) for event in transformed_events]
            db.session.bulk_save_objects(behavior_events)
            
            # Update status
            upload.status = 'completed'
            db.session.commit()
            
            logger.info(f"Successfully processed upload {upload_id}. Inserted {len(behavior_events)} events.")
            return {
                'success': True, 
                'message': 'Successfully processed',
                'records_processed': len(behavior_events)
            }
            
        except Exception as e:
            db.session.rollback()
            upload.status = 'failed'
            db.session.commit()
            logger.error(f"Failed to process upload {upload_id}: {str(e)}")
            return {'success': False, 'message': f'Processing failed: {str(e)}'}
