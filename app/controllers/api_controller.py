from app.extensions import *
from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.Users import Users
from app.database.models.Sources import Sources

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
   
    # Get all the source data
   if methods == "GET" and source_id is None:
       try:
            source = Sources.query.all()
            return jsonify({
                "status" : 200,
                "message" : "Get all sources",
                "sources" : ""
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
           
    # Add one source data
   elif methods == "POST" and source_id is None:
       data = request.get_json()
       if not data or "source_name" not in data or "description" not in data:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"})
       try:
            addSource = Sources(source_name=data['source_name'], description=data['description'])
            db.session.add(addSource)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Get all sources",
                "sources" : ""
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
           
    # Get one of source data
   elif methods == "GET" and source_id is not None:
       source = Sources.query.get_or_404(source_id)
       return jsonify({
           "status" : 200,
           "message" : "Get one source",
           "source" : ""
       }), 200
       
    # Update one of source data
   elif methods == "PUT" and source_id is not None:
       return jsonify({
           "status" : 200,
           "message" : "Post source successfully",
       }), 200
       
    # Delete one of source data
   elif methods == "DELETE" and source_id is not None:
       return jsonify({
           "status" : 200,
           "message" : "Delete source successfully",
       }), 200