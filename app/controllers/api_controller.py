from app.extensions import *
from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.Users import Users
from app.database.models.Sources import Sources

controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes

# Controller for Users
def users(type):
    
    # Register Process
    if type == "register":
        data = request.get_json()
        if not data or not data['email'] or not data['username'] or not data['password']:
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
            
    # Login Process
    if type == "login":
        data = request.get_json()
        if not data or not data['email'] or not data['password']:
            return jsonify({"status" : 400, "message" : "Invalid Request, please fill the email and password"})
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

# SOURCES CONTROLLER
def sources(source_id):
   methods = request.method
   sourceID = source_id
   
    # Get all the source data
   if methods == "GET" and sourceID is None:
       try:
            source = Sources.query.all()
            sources = [source.to_dict() for source in source]
            return jsonify({
                "status" : 200,
                "message" : "Get all sources",
                "sources" : sources
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
           
    # Get one of source data
   if methods == "GET" and sourceID is not None:
       try:
            oneSource = Sources.query.get(sourceID)
            if not oneSource:
                return jsonify({"status": 404, "message": "Source not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One source data found !",
                "source" : oneSource.to_dict()
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
       
    # Add one source data
   if methods == "POST" and sourceID is None:
       data = request.get_json()
       if not data or not data['source_name'] or not data['description']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addSource = Sources(source_name=data['source_name'], description=data['description'])
            db.session.add(addSource)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add data source successfully",
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
           
    # Update one of source data
   if methods == "PUT" and sourceID is not None:
       data = request.get_json()
       if not data or not data['source_name'] or not data['description']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}), 400
       try:
            source = Sources.query.get(sourceID)
            if not source:
                return jsonify({"status": 404, "message": "Source not found !"}),404
            source.source_name = data['source_name']
            source.description = data['description']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update data source successfully",
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and sourceID is not None:
       try:
            source = Sources.query.get(sourceID)
            if not source:
                return jsonify({"status": 404, "message": "Source not found !"}),404
            db.session.delete(source)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Delete data source successfully",
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500