'''
Стартовый файл
'''
import logging

from flask import Flask, request

from app.repos.employee import EmployeeRepository
from app.db import SessionLocal, create_db_and_tables

app = Flask(__name__)

LOG = logging.getLogger('werkzeug')
create_db_and_tables()


@app.route('/', methods=['POST'])
def create_employee():
    session = SessionLocal()
    employee_repo = EmployeeRepository(session)

    employee_repo.create(
        name=request.json['name'],
        age=request.json['age'],
        email=request.json['email'],
    )
    return {'message': "Employee created"}, 201

@app.route('/all', methods=['GET'])
def all_employees():
    session = SessionLocal()
    employee_repo = EmployeeRepository(session)
    employees = employee_repo.get_all()
    employees_list = list()
    for employee in employees:
        employees_list.append({
            'id': employee.id,
            'name': employee.name,
            'age': employee.age,
            'email': employee.email,
        })
    session.close()
    return employees_list

@app.route('/<employee_id>', methods=['GET', 'DELETE'])
def employee_by_id(employee_id):
    if request.method == 'GET':
        session = SessionLocal()
        employee_repo = EmployeeRepository(session)
        employee = employee_repo.get_or_404(employee_id)
        session.close()
        if employee is None:
            return {'message': 'Employee not found'}, 404
        return {
            'id': employee.id,
            'name': employee.name,
            'age': employee.age,
            'email': employee.email,
        }, 200
    if request.method == 'DELETE':
        session = SessionLocal()
        employee_repo = EmployeeRepository(session)
        employee = employee_repo.get_or_404(employee_id)
        if employee is None:
            return {'message': 'Employee not found'}, 404
        else:
            employee_repo.delete(employee_id)
            return {'message': 'Employee deleted'}, 204
    else:
        return {'message': 'Method not allowed'}, 405

@app.route('/<employee_id>', methods=['PATCH'])
def edit_employee(employee_id):
    session = SessionLocal()
    employee_repo = EmployeeRepository(session)
    employee = employee_repo.get_or_404(employee_id)
    if employee is None:
        return {'message': 'Employee not found'}, 404

    data = request.get_json()

    edited_data = dict()

    if 'name' in data:
        edited_data['name'] = data['name']
    if 'age' in data:
        edited_data['age'] = data['age']
    if 'email' in data:
        edited_data['email'] = data['email']

    result = employee_repo.update(employee_id, **edited_data)
    return {'message': 'Employee updated'}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
