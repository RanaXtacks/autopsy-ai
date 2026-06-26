import pytest
from app import create_app, db
from app.models.core import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User(username='test_user', email='test@test.com')
            user.set_password('password')
            db.session.add(user)
            db.session.commit()
            yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def token(client):
    with client.application.app_context():
        user = User.query.first()
        return create_access_token(identity=str(user.id))

def test_generate_predictions(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    res = client.post('/api/predictions/generate', headers=headers)
    assert res.status_code == 200
    assert 'predictions' in res.json
    assert len(res.json['predictions']) > 0

def test_get_chronotype(client, token):
    headers = {'Authorization': f'Bearer {token}'}
    # Need to generate first
    client.post('/api/predictions/generate', headers=headers)
    
    res = client.get('/api/predictions/chronotype', headers=headers)
    assert res.status_code == 200
    assert 'chronotype' in res.json
