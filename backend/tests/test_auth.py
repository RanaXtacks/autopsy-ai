import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestAuthEndpoints:
    def test_register_success(self, client):
        response = client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['user']['username'] == 'testuser'

    def test_login_success(self, client):
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'testuser'

    def test_refresh_token(self, client):
        # Register & Login
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        login_resp = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        refresh_token = login_resp.get_json()['refresh_token']
        
        # Refresh access token
        refresh_resp = client.post('/api/auth/refresh', headers={
            'Authorization': f'Bearer {refresh_token}'
        })
        assert refresh_resp.status_code == 200
        data = refresh_resp.get_json()
        assert data['success'] is True
        assert 'access_token' in data

    def test_get_current_user_me(self, client):
        # Register & Login
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        login_resp = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        access_token = login_resp.get_json()['access_token']
        
        # Get Me
        me_resp = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {access_token}'
        })
        assert me_resp.status_code == 200
        data = me_resp.get_json()
        assert data['username'] == 'testuser'

    def test_logout_and_blocklist(self, client):
        # Register & Login
        client.post('/api/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        login_resp = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        access_token = login_resp.get_json()['access_token']
        
        # Verify can access protected route
        me_resp = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {access_token}'
        })
        assert me_resp.status_code == 200
        
        # Logout
        logout_resp = client.post('/api/auth/logout', headers={
            'Authorization': f'Bearer {access_token}'
        })
        assert logout_resp.status_code == 200
        assert logout_resp.get_json()['success'] is True
        
        # Verify access token is now invalid (revoked)
        me_resp_after = client.get('/api/auth/me', headers={
            'Authorization': f'Bearer {access_token}'
        })
        assert me_resp_after.status_code == 401
        assert me_resp_after.get_json()['error'] == 'token_revoked'
