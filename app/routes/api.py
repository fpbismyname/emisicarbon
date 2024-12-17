from flask import Blueprint, jsonify
from app.controllers import api_controller
router = Blueprint("router-api", __name__)
    
# Create api routes here
# Base URL
URL = "/emisi-carbon/api/v1"

# Account List
@router.route(f"{URL}/account")
def home():
    return api_controller.account_get_data()

@router.route(f"{URL}/emisi")
def emisi():
    return api_controller.emisi_get_data()