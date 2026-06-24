import os
import pytest
from app.data_pipeline.parsers.chrome_parser import ChromeParser
from app.data_pipeline.parsers.github_parser import GitHubParser
from app.data_pipeline.parsers.screentime_parser import ScreenTimeParser
from app.data_pipeline.parsers.spotify_parser import SpotifyParser
from app.data_pipeline.transformers.event_transformer import EventTransformer

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def test_chrome_parser():
    file_path = os.path.join(DATA_DIR, 'chrome.csv')
    parser = ChromeParser(file_path)
    data = parser.process()
    
    # 6 rows originally. 
    # Row 4 is missing visit_time
    # Row 5 is missing URL
    # Row 6 is exact duplicate of row 1
    # Should result in 3 valid rows
    assert len(data) == 3
    
    # Test transformer
    events = EventTransformer.transform_chrome(data, user_id=1, upload_id=1)
    assert len(events) == 3
    assert events[0]['source'] == 'chrome'
    assert events[0]['event_type'] == 'visit'
    assert events[0]['category'] == 'development' # github.com -> development
    assert events[1]['category'] == 'entertainment' # youtube.com -> entertainment
    assert events[2]['category'] == 'learning' # chatgpt.com -> learning
    
def test_github_parser():
    file_path = os.path.join(DATA_DIR, 'github.csv')
    parser = GitHubParser(file_path)
    data = parser.process()
    
    assert len(data) == 2
    events = EventTransformer.transform_github(data, user_id=1, upload_id=1)
    assert len(events) == 2
    assert events[0]['source'] == 'github'
    assert events[0]['category'] == 'development'

def test_screentime_parser():
    file_path = os.path.join(DATA_DIR, 'screentime.csv')
    parser = ScreenTimeParser(file_path)
    data = parser.process()
    
    assert len(data) == 3
    events = EventTransformer.transform_screentime(data, user_id=1, upload_id=1)
    assert len(events) == 3
    assert events[0]['source'] == 'screentime'
    assert events[0]['category'] == 'development' # VS Code -> development
    assert events[1]['category'] == 'music' # Spotify -> music
    assert events[2]['category'] == 'social' # Twitter -> social

def test_spotify_parser():
    file_path = os.path.join(DATA_DIR, 'spotify.csv')
    parser = SpotifyParser(file_path)
    data = parser.process()
    
    assert len(data) == 2
    events = EventTransformer.transform_spotify(data, user_id=1, upload_id=1)
    assert len(events) == 2
    assert events[0]['source'] == 'spotify'
    assert events[0]['category'] == 'music'
    assert events[0]['event_type'] == 'play'
