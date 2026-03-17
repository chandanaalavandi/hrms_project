Basic HRMS (Human Resource Management System)
A comprehensive HRMS application built with Flask that demonstrates employee management, attendance tracking, departmental reporting, and interactive dashboards with modern UI.

📋 Features
👥 Employee Management
-- Add new employees with complete details (name, email, address, designation, department, date of joining)

-- View all employees in a sortable table

-- Filter employees by department, designation, or search term

-- Delete employees with confirmation

-- View detailed employee profiles

⏱️ Attendance Tracking
-- Mark attendance with in-time and out-time

-- Automatic working hours calculation

-- View attendance history for each employee

-- Today's attendance statistics on dashboard

-- Status badges (Present, Pending, Completed)

📊 Reports & Analytics
-- Department-wise employee count with bar charts

-- Distribution visualization with doughnut charts

-- Export reports as CSV

-- Export reports as JSON

-- Percentage breakdown in table view

-- Live dashboard statistics

🎨 Modern UI Features
-- Responsive sidebar navigation

-- Gradient backgrounds and modern color scheme

-- Interactive charts using Chart.js

-- Font Awesome icons throughout

-- Mobile-responsive design

-- Loading states and animations

-- Card-based layout with hover effects

🛠️ Tech Stack
-- Backend: Flask 2.3.3 (Python)

-- Database: SQLite with SQLAlchemy ORM 3.1.1

-- Frontend: HTML5, CSS3, JavaScript (ES6)

-- Charts: Chart.js 3.9.1

-- Icons: Font Awesome 6.0.0

-- Fonts: Google Fonts (Inter)

📁 Project Structure
text
hrms_project/
├── app.py                 # Main application with all routes and API endpoints
├── models.py              # Database models (Employee, Attendance)
├── extensions.py          # SQLAlchemy initialization
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── hrms.db                # SQLite database (auto-generated)
├── static/
│   └── style.css          # Comprehensive CSS styling (600+ lines)
└── templates/
    ├── index.html         # Dashboard with live statistics
    ├── employees.html     # Employee list with add form and filters
    ├── employee_detail.html # Employee profile with attendance history
    ├── mark_attendance.html # Dedicated attendance marking form
    └── report.html        # Department reports with charts and export


🚀 Installation and Setup
-- Prerequisites
Python 3.8 or higher

pip (Python package manager)

Virtual environment (recommended)

-- Step-by-Step Installation
Clone or extract the project

-- bash
cd hrms_project
Create a virtual environment

-- bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies

-- bash
pip install -r requirements.txt
Run the application

-- bash
python app.py
Access the application
Open your browser and navigate to: http://localhost:5000

📡 API Endpoints
-Employee Management
-Method	Endpoint	Description	Request Body
-POST	/api/employees	Add new employee	{name, email, address, designation, department, date_of_joining}
-GET	/api/employees	Get all employees	-
-GET	/api/employees/filter	Filter employees	Query params: department, designation, search
-DELETE	/api/employees/<id>	Delete employee	-
-Attendance Management
-Method	Endpoint	Description	Request Body
-POST	/api/attendance	Mark attendance	{employee_id, date, in_time, out_time}
-GET	/api/attendance/<id>	Get employee attendance	-
-GET	/api/attendance/today	Get today's attendance stats	-
-- Reports & Dashboard
Method	Endpoint	Description
-GET	/api/report/department/	Get department-wise employee counts
-GET	/api/report/export/csv	Download report as CSV
-GET	/api/stats/dashboard	Get dashboard statistics
🎯 Web Routes
Route	Description
/	Home dashboard with live statistics
/employees	Employee list with add form
/employee/<id>	Employee details with attendance history
/mark-attendance/<id>	Dedicated attendance marking form
/report	Department reports with charts
💻 Usage Examples
Adding an Employee via API
bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main St",
    "designation": "Software Engineer",
    "department": "Engineering",
    "date_of_joining": "2024-01-15"
  }'
Marking Attendance via API
-- bash
curl -X POST http://localhost:5000/api/attendance \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "date": "2024-01-15",
    "in_time": "09:00:00",
    "out_time": "18:00:00"
  }'
  
📊 Time & Space Complexities
Operation	Time Complexity	Space Complexity
Add Employee	O(1)	O(1)
Get All Employees	O(n)	O(n)
Filter Employees	O(n)	O(n)
Mark Attendance	O(1)	O(1)
Get Employee Attendance	O(m)	O(m)
Department Report	O(n)	O(d)
where n = number of employees, m = number of attendance records, d = number of departments

🔧 Troubleshooting
Common Issues and Solutions
Database errors

bash
# Delete the existing database and restart
rm hrms.db
python app.py
Port already in use

bash
# Change the port in app.py
app.run(debug=True, port=5001)
Module not found errors

bash
# Ensure all dependencies are installed
pip install -r requirements.txt
📝 Notes
The application runs in debug mode by default (not for production)

Database is automatically created on first run

All API endpoints return JSON responses

The UI is fully responsive and works on mobile devices

Charts automatically update when data changes

🤝 Contributing
This project was created for an internship assignment. For any questions or suggestions, please contact the author.

📄 License
This project is for educational purposes as part of an internship assignment.

🎉 Acknowledgments
Flask documentation

SQLAlchemy ORM documentation

Chart.js library

Font Awesome icons