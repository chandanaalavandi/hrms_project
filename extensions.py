"""
Extensions module for HRMS application.
Initializes SQLAlchemy without binding to app.
"""

from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance without binding to app
db = SQLAlchemy()

# Note: Login functionality removed for basic HRMS
# If you need login later, install flask-login and uncomment:
# from flask_login import LoginManager
# login_manager = LoginManager()