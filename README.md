# 🚀 Basic HRMS (Human Resource Management System)

A **comprehensive HRMS web application** built using **Flask** that manages employee data, attendance tracking, and departmental reporting with a modern UI dashboard.

---

## 📌 Features

### 👥 Employee Management

* Add employees with complete details
* View employees in a sortable table
* Filter by department, designation, or search
* Delete employees with confirmation
* View detailed employee profiles

---

### ⏱️ Attendance Tracking

* Mark attendance (In-Time / Out-Time)
* Automatic working hours calculation
* View attendance history
* Dashboard with today's stats
* Status badges (Present, Pending, Completed)

---

### 📊 Reports & Analytics

* Department-wise employee count (Bar Chart)
* Distribution visualization (Doughnut Chart)
* Export reports (CSV & JSON)
* Percentage breakdown tables
* Live dashboard statistics

---

### 🎨 Modern UI

* Responsive sidebar navigation
* Gradient UI & modern color scheme
* Interactive charts (Chart.js)
* Font Awesome icons
* Mobile-friendly design
* Animations & loading states

---

## 🛠️ Tech Stack

| Layer    | Technology              |
| -------- | ----------------------- |
| Backend  | Flask (Python)          |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | HTML, CSS, JavaScript   |
| Charts   | Chart.js                |
| Icons    | Font Awesome            |

---

## 📁 Project Structure

```bash
hrms_project/
│
├── app.py
├── models.py
├── extensions.py
├── requirements.txt
├── README.md
├── hrms.db
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── employees.html
    ├── employee_detail.html
    ├── mark_attendance.html
    └── report.html
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/chandanaalavandi/hrms_project.git
cd hrms_project
```

### 2️⃣ Create virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application

```bash
python app.py
```

### 🌐 Access the app

```
http://localhost:5000
```

---

## 📡 API Endpoints

### 👤 Employee APIs

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | /api/employees        | Add employee      |
| GET    | /api/employees        | Get all employees |
| GET    | /api/employees/filter | Filter employees  |
| DELETE | /api/employees/<id>   | Delete employee   |

---

### ⏱️ Attendance APIs

| Method | Endpoint              | Description         |
| ------ | --------------------- | ------------------- |
| POST   | /api/attendance       | Mark attendance     |
| GET    | /api/attendance/<id>  | Employee attendance |
| GET    | /api/attendance/today | Today's stats       |

---

### 📊 Reports APIs

| Method | Endpoint               | Description       |
| ------ | ---------------------- | ----------------- |
| GET    | /api/report/department | Department report |
| GET    | /api/report/export/csv | Export CSV        |
| GET    | /api/stats/dashboard   | Dashboard stats   |

---

## 🌐 Web Routes

| Route            | Description         |
| ---------------- | ------------------- |
| /                | Dashboard           |
| /employees       | Employee management |
| /employee/<id>   | Employee details    |
| /mark-attendance | Attendance form     |
| /report          | Reports & analytics |

---

## 💻 Usage Examples

### ➕ Add Employee

```bash
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
```

---

### ⏱️ Mark Attendance

```bash
curl -X POST http://localhost:5000/api/attendance \
-H "Content-Type: application/json" \
-d '{
  "employee_id": 1,
  "date": "2024-01-15",
  "in_time": "09:00:00",
  "out_time": "18:00:00"
}'
```

---

## 📊 Time & Space Complexity

| Operation         | Time | Space |
| ----------------- | ---- | ----- |
| Add Employee      | O(1) | O(1)  |
| Get Employees     | O(n) | O(n)  |
| Filter Employees  | O(n) | O(n)  |
| Mark Attendance   | O(1) | O(1)  |
| Attendance Fetch  | O(m) | O(m)  |
| Department Report | O(n) | O(d)  |

---

## 🔧 Troubleshooting

### ❌ Database Issues

```bash
rm hrms.db
python app.py
```

### ❌ Port Already in Use

```python
app.run(debug=True, port=5001)
```

### ❌ Module Not Found

```bash
pip install -r requirements.txt
```

---

## 📝 Notes

* Runs in debug mode (development only)
* Database auto-creates on first run
* Fully responsive UI
* REST APIs return JSON
* Charts update dynamically

---

## 🤝 Contribution

This project was built as part of an internship assignment.

---

## 👩‍💻 Author

**Chandana Kotresh Alavandi**

---

## ⭐ Final Note

This project is designed with **real-world HR workflows**, scalable backend structure, and RESTful API design — making it suitable for production-level extensions.
