from app.extensions import *
from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.Users import Users

controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes

# Controller for Users
def users(type):
    if type == "register":
        data = request.get_json()
        if not data or "username" not in data or "password" not in data or "email" not in data :
            return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
        checkDuplication = Users.query.filter_by(email=data['email']).first()
        if checkDuplication:
            return jsonify({"status" : 409, "message" : "Account already exists"}), 409
        try:
            newUsers = Users(username=data['username'], email=data['email'])
            newUsers.set_password(data['password'])
            db.session.add(newUsers)  
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
    elif type == "login":
        data = request.get_json()
        if not data or "email" not in data or "password" not in data :
            return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
        currentUsers = Users.query.filter_by(email=data['email']).first()
        if not currentUsers : return jsonify({"status": 404, "message": "Invalid Credentials !"}), 404
        currentUser = currentUsers.to_dict()
        try:
            if not Users.check_password(currentUser['password_hash'], data['password']) : return jsonify({"status":404, "message" : "Invalid Credentials !"}), 404
            bearer_token = flask_jwt.create_access_token(identity=f"{currentUser['username']}-{currentUser['user_id']}")
            return jsonify({
                "status" : 200,
                "role" : currentUser['role'],
                "message": "Login Success",
                "bearer_token" : bearer_token
            }), 200 
        except IntegrityError:
            return jsonify({"status": 500, "message": "Internal Server Error"}), 500

def sources(source_id):
   methods = request.method
   if methods == "GET" and source_id is None:
       return jsonify({
           "GET ALL" : "ALL"
       })
   elif methods == "GET" and source_id is not None:
       return jsonify({
           "GET ONE" : "ONE"
       })
   elif methods == "POST" and source_id is None:
       return jsonify({
           "POST ONE" : "ONE"
       })
   elif methods == "PUT" and source_id is not None:
       return jsonify({
           "PUT ONE" : "ONE"
       })
   elif methods == "DELETE" and source_id is not None:
       return jsonify({
           "DELETE ONE" : "ONE"
       })