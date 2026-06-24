import io
import os
import pytest
from app import db
from app.models.core import Upload
from app.models.events import BehaviorEvent

@pytest.fixture
def auth_token(client):
    client.post('/api/auth/register', json={
        'username': 'eventuser',
        'email': 'event@example.com',
        'password': 'password123'
    })
    resp = client.post('/api/auth/login', json={
        'email': 'event@example.com',
        'password': 'password123'
    })
    return resp.get_json()['access_token']

@pytest.fixture
def test_upload(client, auth_token):
    csv_content = b"URL,Title,Visit Time\nhttps://github.com,GitHub,2026-06-24 10:00:00"
    data = {'file': (io.BytesIO(csv_content), 'test.csv')}
    resp = client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={'Authorization': f'Bearer {auth_token}'})
    return resp.get_json()['id']

def test_process_upload_endpoint(client, auth_token, test_upload):
    resp = client.post(f'/api/uploads/{test_upload}/process', json={'source': 'chrome'}, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    
    data = resp.get_json()
    assert resp.status_code == 200
    assert data['success'] is True
    assert data['records_processed'] == 1
    
    # Check status
    status_resp = client.get(f'/api/uploads/{test_upload}/status', headers={'Authorization': f'Bearer {auth_token}'})
    assert status_resp.get_json()['status'] == 'completed'
    
    # Get events
    events_resp = client.get('/api/events', headers={'Authorization': f'Bearer {auth_token}'})
    events_data = events_resp.get_json()
    assert events_data['total'] == 1
    assert events_data['items'][0]['source'] == 'chrome'
    assert events_data['items'][0]['category'] == 'development'

def test_process_invalid_source(client, auth_token, test_upload):
    resp = client.post(f'/api/uploads/{test_upload}/process', json={'source': 'invalid_source'}, headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert resp.status_code == 400
    assert 'Unsupported source' in resp.get_json()['error']

def test_get_events_with_filters(client, auth_token, test_upload):
    # Process first
    client.post(f'/api/uploads/{test_upload}/process', json={'source': 'chrome'}, headers={'Authorization': f'Bearer {auth_token}'})
    
    # Filter by source
    resp1 = client.get('/api/events?source=chrome', headers={'Authorization': f'Bearer {auth_token}'})
    assert resp1.get_json()['total'] == 1
    
    # Filter by non-existent source
    resp2 = client.get('/api/events?source=spotify', headers={'Authorization': f'Bearer {auth_token}'})
    assert resp2.get_json()['total'] == 0
    
    # Filter by category
    resp3 = client.get('/api/events?category=development', headers={'Authorization': f'Bearer {auth_token}'})
    assert resp3.get_json()['total'] == 1
