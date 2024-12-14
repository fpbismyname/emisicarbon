from flask import Blueprint, jsonify
controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes
def get_data():
    return jsonify({
        "status" : 200,
        "message": "Welcome to the API"
    })