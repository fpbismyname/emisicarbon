from flask import Blueprint, jsonify
from app.controllers import api_controller
router = Blueprint("router-api", __name__)
    
# Create api routes here
# Base URL
URL = "/emisi-carbon/api/v1"
# Route for register API
@router.route(f"{URL}/register", methods=['POST'])
def register():
    return api_controller.register()
# Route for login API
@router.route(f"{URL}/login", methods=['POST'])
def login():
    return api_controller.login()