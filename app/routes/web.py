from flask import Blueprint, jsonify
from app.controllers import web_controller
router = Blueprint("router-web", __name__)
    
# Create web routes here
@router.route("/")
def home():
    return web_controller.index_home()