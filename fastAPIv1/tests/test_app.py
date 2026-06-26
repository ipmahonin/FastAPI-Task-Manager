#код из tests/test_app.py
from fastapi.testclient import TestClient
from main import app
import uuid
import pytest

client=TestClient(app)

@pytest.fixture
def creat_user():
    email = f"{uuid.uuid4()}@test.com"
    return client.post(
        '/users/register',
        json={
            'email':email,
            'password':'123456'
        }),email 

@pytest.fixture
def creata_loggin_user(creat_user):
    data,email = creat_user
    return client.post(
        '/users/login',
        data={
            'username':email,
            'password':'123456'
        })

@pytest.fixture
def creat_task(creata_loggin_user):
    data=creata_loggin_user
    data=data.json()
    return client.post(
        '/tasks',
        json={
            'title': 'title',
            'description': 'description'
        },
        headers={"Authorization": f"Bearer {data['access_token']}"})

@pytest.fixture
def creat_token_id(creata_loggin_user,creat_task):
    log = creata_loggin_user
    task = creat_task
    log=log.json()
    access_token=log['access_token']
    task=task.json()
    task_id=task['id']
    return access_token,task_id

def test_register(creat_user):
    data,email = creat_user
    assert data.status_code == 201
    data = data.json()
    assert "id" in data
    assert "email" in data

    data=client.post(
        '/users/register',
        json={
            'email':email,
            'password':'123456'
        })
    assert data.status_code == 400
    data = data.json()
    assert data["detail"] == 'User already exists'

def test_loggin(creata_loggin_user):
    data=client.post(
        '/users/login',
        data={
            'username':'test@test.com',
            'password':'test_password'
        })
        
    assert data.status_code == 401
    data = data.json()
    assert data["detail"] == 'Invalid credentials'

    data = creata_loggin_user
    assert data.status_code == 200
    data = data.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert 'token_type' in data

def test_refresh(creata_loggin_user):
    data = creata_loggin_user
    data=data.json()
    token_ref=data['refresh_token']

    result = client.post(
        '/users/refresh',
        json={"refresh_token": "string"})
    assert result.status_code == 401
    result = result.json()
    assert result["detail"] == 'Invalid token'

    result = client.post(
        '/users/refresh',
        json={"refresh_token": token_ref})
    assert result.status_code == 200
    result = result.json()
    assert 'access_token' in result
    assert 'token_type' in result


def test_post_task(creat_task):
    query=client.post(
        '/tasks',
        json={
            'title': 'title',
            'description': 'description'
        },
        headers={"Authorization": "Bearer 123"})
    assert query.status_code == 401
    query = query.json()
    assert query["detail"] == 'Invalid token'

    query = creat_task
    assert query.status_code == 201
    query = query.json()
    assert 'id' in query
    assert 'title' in query
    assert 'description' in query


def test_get_task_user(creat_token_id):
    access_token,task_id = creat_token_id
    query = client.get(
        '/tasks',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 200
    query = query.json()
    assert 'id' in query[0]
    assert 'title' in query[0]
    assert 'description' in query[0]


def test_get_task_id(creat_token_id):
    access_token,task_id = creat_token_id

    query = client.get(
        f'/tasks/{999}',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 404
    query = query.json()
    assert query["detail"] == 'Not found'

    query = client.get(
        f'/tasks/{1}',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 403
    query = query.json()
    assert query["detail"] == 'No access'

    query = client.get(
        f'/tasks/{task_id}',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 200
    query = query.json()
    assert 'id' in query
    assert 'title' in query
    assert 'description' in query

def test_update_task(creat_token_id):
    access_token,task_id = creat_token_id
    query = client.put(
        f'/tasks/{999}',
        json={
            'title': 'title',
            'description': 'description'},
            headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 404
    query = query.json()
    assert query["detail"] == 'Not found'

    query = client.put(
        f'/tasks/{1}',
        json={
            'title': 'title',
            'description': 'description'},
            headers={"Authorization": f"Bearer {access_token}"}
            )

    assert query.status_code == 403
    query = query.json()
    assert query["detail"] == 'No access'

    query = client.put(
        f'/tasks/{task_id}',
        json={
            'title': 'title',
            'description': 'description'},
            headers={"Authorization": f"Bearer {access_token}"}
            )
    
    assert query.status_code == 200
    query = query.json()
    assert 'id' in query
    assert 'title' in query
    assert 'description' in query

def test_patch_task(creat_token_id):
    access_token,task_id = creat_token_id
    query = client.patch(
        f'/tasks/{999}/status',
        json={"status": "in_progress"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 404
    query = query.json()
    assert query["detail"] == 'Not found'

    query = client.patch(
        f'/tasks/{1}/status',
        json={"status": "in_progress"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 403
    query = query.json()
    assert query["detail"] == 'No access'


    query = client.patch(
        f'/tasks/{task_id}/status',
        json={"status": "in_progress"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 200
    query = query.json()
    assert 'id' in query
    assert 'status' in query
    
def test_delete_task(creat_token_id):
    access_token,task_id = creat_token_id

    query = client.delete(
        f'/tasks/{999}',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 404
    query = query.json()
    assert query["detail"] == 'Not found'

    query = client.delete(
        f'/tasks/{1}',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 403
    query = query.json()
    assert query["detail"] == 'No access'

    query = client.delete(
        f'/tasks/{task_id}',
         headers={"Authorization": f"Bearer {access_token}"}
    )
    assert query.status_code == 204
