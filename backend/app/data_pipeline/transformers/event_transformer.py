from datetime import datetime
from urllib.parse import urlparse

class EventTransformer:
    """
    Transforms raw dictionaries from parsers/validators into dicts matching 
    the BehaviorEvent database schema.
    """
    
    @staticmethod
    def get_category_from_url(url: str) -> str:
        try:
            domain = urlparse(url).netloc.lower()
            if not domain:
                # Fallback if URL doesn't have scheme
                domain = urlparse('http://' + url).netloc.lower()
                
            if any(x in domain for x in ['youtube.com', 'netflix.com', 'twitch.tv']):
                return 'entertainment'
            elif any(x in domain for x in ['github.com', 'stackoverflow.com', 'leetcode.com']):
                return 'development'
            elif any(x in domain for x in ['chatgpt.com', 'wikipedia.org', 'coursera.org']):
                return 'learning'
            elif any(x in domain for x in ['spotify.com', 'apple.music']):
                return 'music'
            elif any(x in domain for x in ['twitter.com', 'facebook.com', 'instagram.com', 'reddit.com']):
                return 'social'
            return 'uncategorized'
        except:
            return 'uncategorized'
            
    @staticmethod
    def transform_chrome(data: list, user_id: int, upload_id: int) -> list:
        events = []
        for row in data:
            # marshmallow already converts visit_time to datetime
            dt = row['visit_time'] 
            url = row['URL']
            title = row.get('Title', '')
            
            events.append({
                'user_id': user_id,
                'upload_id': upload_id,
                'timestamp': dt,
                'source': 'chrome',
                'event_type': 'visit',
                'category': EventTransformer.get_category_from_url(url),
                'value': url,
                'metadata_obj': {'title': title}
            })
        return events
        
    @staticmethod
    def transform_github(data: list, user_id: int, upload_id: int) -> list:
        events = []
        for row in data:
            events.append({
                'user_id': user_id,
                'upload_id': upload_id,
                'timestamp': row['Timestamp'],
                'source': 'github',
                'event_type': row['Action'],
                'category': 'development',
                'value': row['Repository'],
                'metadata_obj': {}
            })
        return events
        
    @staticmethod
    def transform_screentime(data: list, user_id: int, upload_id: int) -> list:
        events = []
        for row in data:
            app = row['app_name']
            
            category = 'uncategorized'
            app_lower = app.lower()
            if 'youtube' in app_lower or 'netflix' in app_lower: category = 'entertainment'
            elif 'spotify' in app_lower: category = 'music'
            elif 'code' in app_lower or 'terminal' in app_lower: category = 'development'
            elif 'instagram' in app_lower or 'twitter' in app_lower: category = 'social'
            
            events.append({
                'user_id': user_id,
                'upload_id': upload_id,
                'timestamp': row['Date'],
                'source': 'screentime',
                'event_type': 'app_usage',
                'category': category,
                'value': app,
                'metadata_obj': {'duration_seconds': row['Duration']}
            })
        return events
        
    @staticmethod
    def transform_spotify(data: list, user_id: int, upload_id: int) -> list:
        events = []
        for row in data:
            events.append({
                'user_id': user_id,
                'upload_id': upload_id,
                'timestamp': row['Timestamp'],
                'source': 'spotify',
                'event_type': 'play',
                'category': 'music',
                'value': row['Track'],
                'metadata_obj': {'artist': row['Artist']}
            })
        return events
