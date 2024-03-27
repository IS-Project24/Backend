from flask import request, jsonify
from app import app, bcrypt, db
from app.models.user import User
from app.models.vehicle import Vehicle
import jwt

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    userid = data.get('userid')
    vehicleid = data.get('vehicleid')
    password = data.get('password')
    if not userid or not vehicleid or not password:
        return jsonify({'message': 'Incomplete details provided.'}), 400
    
    user = User.query.filter_by(userid=userid, vehicleid=vehicleid).first()

    if not user:
        return jsonify({'message': 'User does not exist.'}), 404

    if bcrypt.check_password_hash(user.password, password):
        data = {'user': {'id': user.id}}
        auth_token = jwt.encode(data, app.secret_key, algorithm='HS256')
        return jsonify({'message': 'Login successful', 'authToken': auth_token}), 200
    else:
        return jsonify({'message': 'Incorrect password.'}), 401

@app.route("/signup", methods=['POST'])
def signup():
    data = request.json
    userid = data.get('userid')
    vehicleid = data.get('vehicleid')
    userType = data.get('userType')
    contactNumber = data.get('contactNumber')
    email = data.get('email')
    address = data.get('address')
    password = data.get('password')

    if not userid or not vehicleid or not userType or not contactNumber or not email or not address or not password:
        return jsonify({'message': 'Incomplete details provided.'}), 400

    existing_user = User.query.filter((User.userid == userid)).first()
    if existing_user:
        return jsonify({'message': 'User already exists with this userid.'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(
        userid=userid, 
        vehicleid=vehicleid, 
        userType=userType, 
        contactNumber=contactNumber, 
        email=email, 
        address=address, 
        password=hashed_password
    )

    # Create a default vehicle entry for the new user
    new_vehicle = Vehicle(
        vehicle_id=vehicleid,
        user=new_user,  # Associate the vehicle with the new user
        last_battery_percentage=90,  # Default battery percentage
        last_health_status=90  # Default health status
    )

    db.session.add(new_user)
    db.session.add(new_vehicle)
    db.session.commit()

    data = {'user': {'id': new_user.id}}
    auth_token = jwt.encode(data, app.secret_key, algorithm='HS256')

    return jsonify({'message': 'User created successfully.', 'authToken': auth_token}), 201
