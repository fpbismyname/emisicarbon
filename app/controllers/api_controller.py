from app import db
from flask import Blueprint, jsonify, request
from app.models.Account import Account

controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes
# Controller for register an account
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data :
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
    user = data['username']
    pwd = data['password']
    checkDuplication = Account.query.filter_by(username=user).first()
    if checkDuplication:
        return jsonify({"status" : 409, "message" : "Username already exist"}), 409
    try:
        newAccount = Account(username=user)
        newAccount.set_password(pwd)
        db.session.add(newAccount)  
        db.session.commit() 
        return jsonify({
            "status" : 200,
            "message": "Register Success"
            }), 200
    except ZeroDivisionError as err:
        return jsonify({
                "status" : 500,
                "message": "Internal Server Error !"
                }), 500
        
# Controller for login an account
def login():
    data = request.json
    user = data['username']
    pwd = data['password']
    if not data or "username" not in data or "password" not in data :
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
    currentAccount = Account.query.filter_by(username=user).first()
    if not currentAccount : return jsonify({"status": 404, "message": "Invalid Credentials !"}), 404
    currentAccountPassword = currentAccount.password
    try:
        if not Account.check_password(currentAccountPassword, pwd) : return jsonify({"status":404, "message" : "Invalid Credentials !"}), 404
        return jsonify({
            "status" : 200,
            "message": "Login Success",
            "token" : currentAccount.password
        }), 200
    except ZeroDivisionError as err:
        return jsonify({"status": 500, "message": "Internal Server Error"}), 500