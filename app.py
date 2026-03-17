"""
Main application module for HRMS.
This module initializes the Flask app and defines all routes.
"""

from flask import Flask, render_template, request, jsonify, Response
from datetime import datetime, date
from sqlalchemy import func
import csv
from io import StringIO
import os

# Import db from extensions
from extensions import db
# Import models
from models import Employee, Attendance

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)


# ==================== HOME ROUTE ====================

@app.route('/')
def home():
    """
    Home page route.
    Returns:
        Rendered home page with welcome message
    """
    return render_template('index.html', 
                         message="Welcome to HRMS - Human Resource Management System")


# ==================== API ENDPOINTS - EMPLOYEE MANAGEMENT ====================

@app.route('/api/employees', methods=['POST'])
def add_employee():
    """
    API endpoint to add a new employee.
    
    Expected JSON payload:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "address": "123 Main St",
        "designation": "Software Engineer",
        "department": "Engineering",
        "date_of_joining": "2024-01-15"
    }
    
    Returns:
        JSON: Success message with employee data or error message
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'address', 'designation', 'department', 'date_of_joining']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if employee with same email exists
        if Employee.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Employee with this email already exists'}), 400
        
        # Create new employee
        employee = Employee(
            name=data['name'],
            email=data['email'],
            address=data['address'],
            designation=data['designation'],
            department=data['department'],
            date_of_joining=datetime.strptime(data['date_of_joining'], '%Y-%m-%d').date()
        )
        
        db.session.add(employee)
        db.session.commit()
        
        return jsonify({
            'message': 'Employee added successfully',
            'employee': employee.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees', methods=['GET'])
def get_all_employees():
    """
    API endpoint to retrieve all employees.
    
    Returns:
        JSON: List of all employees
    """
    try:
        employees = Employee.query.all()
        return jsonify({
            'employees': [emp.to_dict() for emp in employees],
            'total': len(employees)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees/filter', methods=['GET'])
def filter_employees():
    """
    API endpoint to filter employees by department, designation, or search term.
    
    Query Parameters:
        department (str): Filter by department
        designation (str): Filter by designation
        search (str): Search in name or email
    
    Returns:
        JSON: Filtered list of employees
    """
    try:
        query = Employee.query
        
        # Apply filters
        department = request.args.get('department')
        if department:
            query = query.filter(Employee.department.ilike(f'%{department}%'))
        
        designation = request.args.get('designation')
        if designation:
            query = query.filter(Employee.designation.ilike(f'%{designation}%'))
        
        search = request.args.get('search')
        if search:
            query = query.filter(
                (Employee.name.ilike(f'%{search}%')) | 
                (Employee.email.ilike(f'%{search}%'))
            )
        
        employees = query.all()
        
        return jsonify({
            'employees': [emp.to_dict() for emp in employees],
            'total': len(employees),
            'filters': {
                'department': department,
                'designation': designation,
                'search': search
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """
    API endpoint to delete an employee.
    
    Args:
        employee_id (int): ID of the employee to delete
    
    Returns:
        JSON: Success message or error
    """
    try:
        # Use db.session.get() instead of Query.get() for SQLAlchemy 2.0
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({'message': 'Employee deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== API ENDPOINTS - ATTENDANCE MANAGEMENT ====================

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    """
    API endpoint to mark attendance for an employee.
    
    Expected JSON payload:
    {
        "employee_id": 1,
        "date": "2024-01-15",
        "in_time": "09:00:00",
        "out_time": "18:00:00"  # optional
    }
    
    Returns:
        JSON: Success message with attendance data or error message
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'employee_id' not in data:
            return jsonify({'error': 'Missing employee_id'}), 400
        
        if 'date' not in data:
            return jsonify({'error': 'Missing date'}), 400
        
        if 'in_time' not in data:
            return jsonify({'error': 'Missing in_time'}), 400
        
        # Use db.session.get() instead of Query.get() for SQLAlchemy 2.0
        employee = db.session.get(Employee, data['employee_id'])
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # Parse date and time
        attendance_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        in_time = datetime.strptime(f"{data['date']} {data['in_time']}", '%Y-%m-%d %H:%M:%S')
        
        # Check if attendance already marked for this date
        existing = Attendance.query.filter_by(
            employee_id=data['employee_id'], 
            date=attendance_date
        ).first()
        
        if existing:
            return jsonify({'error': 'Attendance already marked for this date'}), 400
        
        # Parse out_time if provided
        out_time = None
        if 'out_time' in data and data['out_time']:
            out_time = datetime.strptime(f"{data['date']} {data['out_time']}", '%Y-%m-%d %H:%M:%S')
        
        # Create attendance record
        attendance = Attendance(
            employee_id=data['employee_id'],
            date=attendance_date,
            in_time=in_time,
            out_time=out_time
        )
        
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'message': 'Attendance marked successfully',
            'attendance': attendance.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/attendance/<int:employee_id>', methods=['GET'])
def get_employee_attendance(employee_id):
    """
    API endpoint to get attendance details for a specific employee.
    
    Args:
        employee_id (int): ID of the employee
        
    Returns:
        JSON: List of attendance records for the employee
    """
    try:
        # Use db.session.get() instead of Query.get() for SQLAlchemy 2.0
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # Get attendance records
        attendances = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc()).all()
        
        return jsonify({
            'employee': employee.to_dict(),
            'attendances': [att.to_dict() for att in attendances],
            'total_attendances': len(attendances)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/attendance/today', methods=['GET'])
def attendance_today():
    """
    API endpoint to get today's attendance count.
    
    Returns:
        JSON: Today's attendance statistics
    """
    try:
        today_date = date.today()
        
        # Get today's attendance records
        today_attendance = Attendance.query.filter_by(date=today_date).count()
        
        # Get total employees
        total_employees = Employee.query.count()
        
        # Get present employees
        present_today = Attendance.query.filter(
            Attendance.date == today_date,
            Attendance.in_time.isnot(None)
        ).count()
        
        return jsonify({
            'date': today_date.strftime('%Y-%m-%d'),
            'total_employees': total_employees,
            'present_today': present_today,
            'attendance_percentage': round((present_today / total_employees * 100) if total_employees > 0 else 0, 2)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== API ENDPOINTS - REPORTS ====================

@app.route('/api/report/department/', methods=['GET'])
def api_department_report():
    """
    API endpoint to get department-wise employee counts.
    
    Returns:
        JSON: Dictionary with department names as keys and employee counts as values
    """
    try:
        department_counts = db.session.query(
            Employee.department, 
            func.count(Employee.id)
        ).group_by(Employee.department).all()
        
        report = {dept: count for dept, count in department_counts}
        
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/export/csv')
def export_report_csv():
    """
    Export department report as CSV.
    
    Returns:
        CSV file download
    """
    try:
        department_counts = db.session.query(
            Employee.department, 
            func.count(Employee.id)
        ).group_by(Employee.department).all()
        
        # Create CSV in memory
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['Department', 'Employee Count'])
        for dept, count in department_counts:
            cw.writerow([dept, count])
        
        # Add total row
        total = sum(count for _, count in department_counts)
        cw.writerow(['TOTAL', total])
        
        output = si.getvalue()
        
        return Response(
            output,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=department_report.csv'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== API ENDPOINTS - DASHBOARD ====================

@app.route('/api/stats/dashboard')
def dashboard_stats():
    """
    API endpoint to get dashboard statistics.
    
    Returns:
        JSON: Dashboard statistics
    """
    try:
        total_employees = Employee.query.count()
        total_departments = db.session.query(Employee.department).distinct().count()
        
        today_date = date.today()
        attendance_today = Attendance.query.filter_by(date=today_date).count()
        
        # Get recent employees
        recent_employees = Employee.query.order_by(Employee.created_at.desc()).limit(5).all()
        
        return jsonify({
            'total_employees': total_employees,
            'total_departments': total_departments,
            'attendance_today': attendance_today,
            'recent_employees': [emp.to_dict() for emp in recent_employees]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== WEB ROUTES - EMPLOYEE PAGES ====================

@app.route('/employees')
def list_employees():
    """
    Route to display all employees.
    
    Returns:
        Rendered template with list of employees
    """
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)


@app.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    """
    Route to display employee details with attendance.
    
    Args:
        employee_id (int): ID of the employee
        
    Returns:
        Rendered template with employee details and attendance
    """
    # Use db.session.get() instead of Query.get_or_404() for SQLAlchemy 2.0
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return "Employee not found", 404
    
    attendances = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc()).all()
    return render_template('employee_detail.html', employee=employee, attendances=attendances)


@app.route('/mark-attendance/<int:employee_id>')
def mark_attendance_form(employee_id):
    """
    Route to display attendance marking form.
    
    Args:
        employee_id (int): ID of the employee
        
    Returns:
        Rendered template with attendance form
    """
    # Use db.session.get() instead of Query.get_or_404() for SQLAlchemy 2.0
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return "Employee not found", 404
    
    today = date.today().strftime('%Y-%m-%d')
    return render_template('mark_attendance.html', employee=employee, today=today)


# ==================== WEB ROUTES - REPORTS ====================

@app.route('/report')
def department_report():
    """
    Route to show department-wise employee count report.
    
    Returns:
        Rendered template with department report
    """
    # Get department counts
    department_counts = db.session.query(
        Employee.department, 
        func.count(Employee.id)
    ).group_by(Employee.department).all()
    
    # Convert to list of dictionaries
    report_data = [
        {'department': dept, 'count': count} 
        for dept, count in department_counts
    ]
    
    return render_template('report.html', report_data=report_data)


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)