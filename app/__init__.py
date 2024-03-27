from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os
from sqlalchemy import inspect

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config')
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

from app.routes import *

# Define a function to create all database tables if they don't exist
def create_tables():
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()

        # Check if the 'users' table exists
        if 'users' not in existing_tables:
            User.__table__.create(bind=db.engine) 
            print("User Table created successfully!")
        else:
            print("User Table already exist, skipping creation.")

        if 'vehicles' not in existing_tables:
            Vehicle.__table__.create(bind=db.engine)
            print("Vehicle Table created successfully!")
        else:
            print("Vehicle Table already exist, skipping creation.")

        