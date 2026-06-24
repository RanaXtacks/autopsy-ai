import io
import pytest
from app import create_app, db

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

@pytest.fixture
def auth_token(client):
    client.post('/api/auth/register', json={
        'username': 'uploaduser',
        'email': 'uploader@example.com',
        'password': 'password123'
    })
    resp = client.post('/api/auth/login', json={
        'email': 'uploader@example.com',
        'password': 'password123'
    })
    return resp.get_json()['access_token']

@pytest.fixture
def other_user_token(client):
    client.post('/api/auth/register', json={
        'username': 'otheruser',
        'email': 'other@example.com',
        'password': 'password123'
    })
    resp = client.post('/api/auth/login', json={
        'email': 'other@example.com',
        'password': 'password123'
    })
    return resp.get_json()['access_token']


class TestUploads:
    def test_upload_success(self, client, auth_token):
        data = {
            'file': (io.BytesIO(b"id,name\n1,test"), 'test.csv')
        }
        response = client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['original_filename'] == 'test.csv'
        assert json_data['status'] == 'uploaded'

    def test_upload_invalid_extension(self, client, auth_token):
        data = {
            'file': (io.BytesIO(b"fake data"), 'test.txt')
        }
        response = client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_upload_empty_file(self, client, auth_token):
        data = {
            'file': (io.BytesIO(b""), 'empty.csv')
        }
        response = client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        assert response.status_code == 400

    def test_get_uploads_ownership(self, client, auth_token, other_user_token):
        # Upload file as auth_token user
        data = {
            'file': (io.BytesIO(b"id,name\n1,test"), 'my_data.csv')
        }
        client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={
            'Authorization': f'Bearer {auth_token}'
        })

        # Fetch as other user
        resp = client.get('/api/uploads', headers={'Authorization': f'Bearer {other_user_token}'})
        assert resp.status_code == 200
        assert len(resp.get_json()['items']) == 0

        # Fetch as auth user
        resp2 = client.get('/api/uploads', headers={'Authorization': f'Bearer {auth_token}'})
        assert resp2.status_code == 200
        assert len(resp2.get_json()['items']) == 1

    def test_get_single_upload_ownership(self, client, auth_token, other_user_token):
        # Upload file as auth_token user
        data = {
            'file': (io.BytesIO(b"id,name\n1,test"), 'my_data.csv')
        }
        upload_resp = client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        upload_id = upload_resp.get_json()['id']

        # Attempt to access as other user (should be forbidden)
        resp = client.get(f'/api/uploads/{upload_id}', headers={'Authorization': f'Bearer {other_user_token}'})
        assert resp.status_code == 403

    def test_delete_upload(self, client, auth_token):
        # Upload
        data = {
            'file': (io.BytesIO(b"id,name\n1,test"), 'delete_me.csv')
        }
        upload_resp = client.post('/api/uploads', data=data, content_type='multipart/form-data', headers={
            'Authorization': f'Bearer {auth_token}'
        })
        upload_id = upload_resp.get_json()['id']

        # Delete
        del_resp = client.delete(f'/api/uploads/{upload_id}', headers={'Authorization': f'Bearer {auth_token}'})
        assert del_resp.status_code == 200

        # Verify deletion
        get_resp = client.get(f'/api/uploads/{upload_id}', headers={'Authorization': f'Bearer {auth_token}'})
        assert get_resp.status_code == 404
