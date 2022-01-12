"""
Pytest test file 
"""

import pytest, json
from main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    #os.close(db_fd)
    #os.unlink(db_path)

def test_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert 'users' in json_data
    assert len(json_data['users']) > 0
   