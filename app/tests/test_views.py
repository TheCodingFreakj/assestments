from flask import json
import pytest
from main.model.models import Employee
from main.model.models import db
from flask import Flask
import pytest
from main.model.models import db
from config import TestingConfig
from sqlalchemy.exc import IntegrityError
from main.service.view import employees_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object(TestingConfig)
    db.init_app(app)  # Initialize SQLAlchemy with the app instance
    app.register_blueprint(employees_bp)
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()



def test_create_employee_success(client):
    response = client.post('/create_employee', json={
        'name': 'Pallavi Priyadarshini',
        'age': 30,
        'dept': 'Engineering'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Employee created successfully'


def test_create_employee_missing_fields(client):
    response = client.post('/create_employee', json={
        'name': 'Pallavi Priyadarshini',
        'age': 30
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields: name, age, or dept'

def test_create_employee_invalid_age(client):
    response = client.post('/create_employee', json={
        'name': 'Pallavi Priyadarshini',
        'age': -5,
        'dept': 'Engineering'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Age should be a positive integer'

def test_create_employee_integrity_error(client, mocker):
    # Mock the IntegrityError exception
    mocker.patch('app.db.session.commit', side_effect=IntegrityError("Database integrity error", None, None))
    
    response = client.post('/create_employee', json={
        'name': 'Pallavi Priyadarshini',
        'age': 30,
        'dept': 'Engineering'
    })
    assert response.status_code == 500
    assert 'Database integrity error' in response.json['error']

def test_create_employee_unexpected_error(client, mocker):
    # Mock a generic Exception
    mocker.patch('app.db.session.commit', side_effect=Exception("Failed to create employee"))
    
    response = client.post('/create_employee', json={
        'name': 'Pallavi Priyadarshini',
        'age': 30,
        'dept': 'Engineering'
    })
    assert response.status_code == 500
    assert 'Failed to create employee' in response.json['error']


def test_update_employee_success(client):
    # Create a dummy employee for testing
    employee = Employee(name='Pallavi Priyadarshini', age=30, dept='Engineering')
    db.session.add(employee)
    db.session.commit()

    # Update the employee's information
    response = client.put(f'/employee/{employee.id}', json={
        'name': 'Pallavi Priyadarshini',
        'age': 32,
        'dept': 'IT'
    })

    assert response.status_code == 200
    assert response.json['message'] == 'Employee updated successfully'

def test_update_employee_not_found(client):
    # Attempt to update a non-existent employee
    response = client.put('/employee/999', json={
        'name': 'Pallavi Priyadarshini',
        'age': 32,
        'dept': 'IT'
    })

    assert response.status_code == 404
    assert response.json['message'] == 'Employee not found'

def test_update_employee_missing_key(client):

    employee = Employee(name='Pallavi Priyadarshini', age=30, dept='Engineering')
    db.session.add(employee)
    db.session.commit()
    # Attempt to update employee with missing JSON key
    response = client.put('/employee/1', json={
        'age': 32,
        'dept': 'IT'
    })

    assert response.status_code == 400
    error_response = response.get_json()
    assert 'error' in error_response
    assert 'Missing key in JSON data' in error_response['error']
   


   

def test_update_employee_integrity_error(client, mocker):
    # Create a dummy employee for testing
    employee = Employee(name='John Doe', age=30, dept='Engineering')
    db.session.add(employee)
    db.session.commit()

    # Mock the IntegrityError exception when db.session.commit() is called
    mocker.patch('app.db.session.commit', side_effect=IntegrityError('Database integrity error', params={}, orig=None))

    # Attempt to update the employee, which should trigger IntegrityError
    response = client.put(f'/employee/{employee.id}', json={
        'name': 'Pallavi Priyadarshini',
        'age': 32,
        'dept': 'IT'
    })

    # Assert the response status code
    assert response.status_code == 500

    # Assert the error message in the JSON response
    error_response = response.get_json()
    assert 'error' in error_response
    assert 'Database integrity error' in error_response['error']

def test_delete_employee_success(client):
    # Create a dummy employee for testing
    employee = Employee(name='Pallavi Priyadarshini', age=30, dept='Engineering')
    db.session.add(employee)
    db.session.commit()

    # Delete the employee
    response = client.delete(f'/employee/{employee.id}')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the success message in the JSON response
    assert response.json['message'] == 'Employee deleted successfully'

def test_delete_employee_not_found(client):


    # Attempt to delete a non-existent employee
    response = client.delete('/employee/999')

    # Assert the response status code
    assert response.status_code == 404

    # Assert the message in the JSON response
    assert response.json['message'] == 'Employee not found'

