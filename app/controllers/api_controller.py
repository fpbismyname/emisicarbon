from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.users import users

controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes
# Controller for register an users
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data or "email" not in data :
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
    user = data['username']
    pwd = data['password']
    email = data['email']
    checkDuplication = users.query.filter_by(email=email).first()
    if checkDuplication:
        return jsonify({"status" : 409, "message" : "Account already exists"}), 409
    try:
        newusers = users(username=user, email=email)
        newusers.set_password(pwd)
        db.session.add(newusers)  
        db.session.commit() 
        return jsonify({
            "status" : 200,
            "message": "Register Success"
            }), 200
    except IntegrityError:
        return jsonify({
                "status" : 500,
                "message": "Internal Server Error !",
                }), 500
        
# Controller for login an users
def login():
    data = request.json
    email = data['email']
    pwd = data['password']
    if not data or "email" not in data or "password" not in data :
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
    currentusers = users.query.filter_by(email=email).first()
    if not currentusers : return jsonify({"status": 404, "message": "Invalid Credentials !"}), 404
    currentuser= currentusers.to_dict()
    try:
        if not users.check_password(currentuser['password_hash'], pwd) : return jsonify({"status":404, "message" : "Invalid Credentials !"}), 404
        bearer_token = flask_jwt.create_access_token(identity=currentusers.username)
        return jsonify({
            "status" : 200,
            "role" : currentuser['role'].name,
            "message": "Login Success",
            "bearer_token" : bearer_token
        }), 200
    except IntegrityError:
        return jsonify({"status": 500, "message": "Internal Server Error"}), 500