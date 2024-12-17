from flask import Blueprint, jsonify
from app.controllers import api_controller
router = Blueprint("router-api", __name__)
    
# Create api routes here
@router.route("/emisi-carbon/api/v1")
def home():
    return api_controller.get_data()