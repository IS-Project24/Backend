from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(255), unique=True)
    vehicleid = db.Column(db.String(255), unique=True)
    userType = db.Column(db.String(255))
    contactNumber = db.Column(db.String(255))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))
    password = db.Column(db.String(255))
