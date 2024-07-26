import pytest
import json
from app import app, mysql

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MYSQL_DB'] = 'inventoria_db'
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_signup(client):
    # Test successful registration
    response = client.post('/api/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'User registered successfully'

    # Test missing fields
    response = client.post('/api/register', json={'username': 'testuser2','password': 'testpassword'})
    data = response.get_json()
    assert response.status_code == 400
    assert data['error'] == 'Missing required fields'

def test_login(client):
    # Assuming the user 'testuser' already exists
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Login successful'
    assert 'user' in data

    # Test invalid login
    response = client.post('/api/login', json={
        'username': 'nonexistent',
        'password': 'wrongpassword'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['error'] == 'Invalid username or password'

def test_dashboard(client):
    response = client.get('/api/dashboard')
    data = response.get_json()
    assert response.status_code == 200
    assert 'totalProducts' in data
    assert 'outOfStock' in data
    assert 'lowStock' in data
    assert 'products' in data

def test_add_product(client):
    response = client.post('/api/products', json={
        'name': 'Test Product',
        'stock': 20,
        'price': 10.5
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Product added successfully'

def test_update_product(client):
    # Assuming there is a product with id 1
    response = client.put('/api/products/1', json={
        'name': 'Updated Product',
        'stock': 30,
        'price': 15.0
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Product updated successfully'

def test_delete_product(client):
    response = client.delete('/api/products/1')
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Product deleted successfully'