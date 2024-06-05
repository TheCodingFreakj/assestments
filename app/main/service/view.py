from flask import Blueprint, jsonify, request
from psycopg2 import IntegrityError
from .logger import setup_logger
from ..model.models import db
from ..model.models import Employee

# Set up logger
logger = setup_logger()
employees_bp = Blueprint('employees', __name__)



@employees_bp.route('/employees/getall', methods=['GET'])
def getall():
    try:
        page = request.args.get('page', 1, type=int)
        employees = Employee.query.paginate(page=page, per_page=2)

        logger.info({"employees paginated----->": employees})
        # Prepare JSON response with employee details
        employee_list = []
        for employee in employees:
            employee_data = {
                'id': employee.id,
                'name': employee.name,
                'age': employee.age,
                'dept': employee.dept
            }
            employee_list.append(employee_data)
        
        return jsonify(employee_list)
    
    except Exception as e:
        logger.error({"error happended here----->": str(e)})
        return jsonify({'error': f'Failed to retrieve employees: {str(e)}'}), 500
    


@employees_bp.route('/employees/age_greater_than_23', methods=['GET'])
def get_employees_age_greater_than_23():
    try:
        # Query employees with age greater than 23
        employees = Employee.query.filter(Employee.age > 23).all()
        logger.info({"employees filtered----->": employees})
        # Prepare JSON response with employee details
        employee_list = []
        for employee in employees:
            employee_data = {
                'id': employee.id,
                'name': employee.name,
                'age': employee.age,
                'dept': employee.dept
            }
            employee_list.append(employee_data)
        
        return jsonify(employee_list)
    
    except Exception as e:
        logger.error({"error happended here----->": str(e)})
        return jsonify({'error': f'Failed to retrieve employees: {str(e)}'}), 500
   


@employees_bp.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        employee = Employee.query.get(id)
        logger.info({"employee----->": employee})
        # Check if employee exists
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # Return employee details
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'age': employee.age,
            'dept': employee.dept
        })
    
    except Exception as e:
        logger.error({"error happended here----->": str(e)})
        return jsonify({'error': f'Failed to retrieve employee: {str(e)}'}), 500


@employees_bp.route('/create_employee', methods=['POST'])
def create_employee():
    try:
        data = request.json
        # Validate required fields
        if 'name' not in data or 'age' not in data or 'dept' not in data:
            error_message = 'Missing required fields: name, age, or dept'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        
        # Additional data validation (e.g., age is a number, etc.)
        # Example: age should be a positive integer
        if not isinstance(data['age'], int) or data['age'] <= 0:
            error_message = 'Age should be a positive integer'
            logger.error(error_message)
            return jsonify({'error': error_message}), 400
        

        logger.info('Employee creation initiated')
        employee = Employee(name=data['name'], age=data['age'], dept=data['dept'])
        db.session.add(employee)
        db.session.commit()
        logger.info(f'Employee created successfully')
        return jsonify({'message': 'Employee created successfully'}), 201
    
    except IntegrityError as e:
        db.session.rollback()
        error_message = f'Database integrity error: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 500
    
    except KeyError as e:
        db.session.rollback()
        error_message = f'Missing key in JSON data: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 400
    
    except Exception as e:
        db.session.rollback()
        error_message = f'Failed to create employee: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 500
    
@employees_bp.route('/employee/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404
        
        logger.info(f'Employee updates initiated')
        data = request.json
        employee.name=data['name']
        employee.age=data['age']
        employee.dept=data['dept']
        db.session.commit()
        logger.info(f'Employee updated successfully')
        return jsonify({'message': 'Employee updated successfully'})
    except KeyError as e:
        db.session.rollback()
        error_message = f'Missing key in JSON data: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 400
    
    except ValueError as e:
        db.session.rollback()
        error_message = f'Invalid value: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 400
    
    except IntegrityError as e:
        db.session.rollback()
        error_message = f'Database integrity error: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 500
    
    except Exception as e:
        db.session.rollback()
        error_message = f'Failed to update employee: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 500

@employees_bp.route('/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get(id)
        logger.info({"employee":employee})
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404
        
        logger.info(f'Employee deletes initiated')
        db.session.delete(employee)
        db.session.commit()
        logger.info(f'Employee deleted successfully')
        return jsonify({'message': 'Employee deleted successfully'})
    except KeyError as e:
        db.session.rollback()
        error_message = f'Missing key in JSON data: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 400
    
    except ValueError as e:
        db.session.rollback()
        error_message = f'Invalid value: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 400
    
    except IntegrityError as e:
        db.session.rollback()
        error_message = f'Database integrity error: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 500
    
    except Exception as e:
        db.session.rollback()
        error_message = f'Failed to delete employee: {str(e)}'
        logger.error(error_message)
        return jsonify({'error': error_message}), 500