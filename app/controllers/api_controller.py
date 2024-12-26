from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.users import users

controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes
# Controller for register an users
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data :
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
    user = data['username']
    pwd = data['password']
    checkDuplication = users.query.filter_by(username=user).first()
    if checkDuplication:
        return jsonify({"status" : 409, "message" : "Username already exist"}), 409
    try:
        newusers = users(username=user)
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
    user = data['username']
    pwd = data['password']
    if not data or "username" not in data or "password" not in data :
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
    currentusers = users.query.filter_by(username=user).first()
    if not currentusers : return jsonify({"status": 404, "message": "Invalid Credentials !"}), 404
    currentusersPassword = currentusers.password_hash
    try:
        if not users.check_password(currentusersPassword, pwd) : return jsonify({"status":404, "message" : "Invalid Credentials !"}), 404
        bearer_token = flask_jwt.create_access_token(identity=currentusers.username)
        return jsonify({
            "status" : 200,
            "message": "Login Success",
            "access_token" : bearer_token
        }), 200
    except IntegrityError:
        return jsonify({"status": 500, "message": "Internal Server Error"}), 500