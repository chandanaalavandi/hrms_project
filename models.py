"""
Database models for HRMS application.
Defines Employee and Attendance models with relationships.
"""

from extensions import db
from datetime import datetime

class Employee(db.Model):
    """
    Employee model representing employee information.
    
    Attributes:
        id (int): Primary key
        name (str): Employee's full name
        email (str): Employee's email address (unique)
        address (str): Employee's residential address
        designation (str): Job title/position
        department (str): Department name
        date_of_joining (date): When employee joined
        created_at (datetime): Record creation timestamp
        attendances (relationship): Related attendance records
    """
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with Attendance (one-to-many)
    attendances = db.relationship('Attendance', backref='employee', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """
        Convert employee object to dictionary.
        
        Returns:
            dict: Employee data in dictionary format
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'designation': self.designation,
            'department': self.department,
            'date_of_joining': self.date_of_joining.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        """String representation of Employee object."""
        return f'<Employee {self.name}>'


class Attendance(db.Model):
    """
    Attendance model tracking employee attendance.
    
    Attributes:
        id (int): Primary key
        employee_id (int): Foreign key to Employee
        date (date): Attendance date
        in_time (datetime): Check-in time
        out_time (datetime): Check-out time
        created_at (datetime): Record creation timestamp
    """
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    in_time = db.Column(db.DateTime, nullable=False)
    out_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure unique attendance per employee per day
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='unique_employee_attendance'),)
    
    def to_dict(self):
        """
        Convert attendance object to dictionary.
        
        Returns:
            dict: Attendance data in dictionary format
        """
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'in_time': self.in_time.strftime('%Y-%m-%d %H:%M:%S'),
            'out_time': self.out_time.strftime('%Y-%m-%d %H:%M:%S') if self.out_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def calculate_working_hours(self):
        """
        Calculate total working hours.
        
        Returns:
            float: Total working hours
        """
        if self.out_time:
            delta = self.out_time - self.in_time
            return round(delta.total_seconds() / 3600, 2)
        return 0.0
    
    def __repr__(self):
        """String representation of Attendance object."""
        return f'<Attendance Emp:{self.employee_id} Date:{self.date}>'