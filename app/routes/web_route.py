from flask import Blueprint, jsonify
from app.controllers import web_controller
router = Blueprint("router-web", __name__)
    
# Create web routes here

# Homepage
@router.route("/", methods=['GET'])
def home():
    return web_controller.index_home()

@router.route("/login", methods =['GET'])
def login():
    return web_controller.loginPage()