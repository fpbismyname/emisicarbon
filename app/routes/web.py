from flask import Blueprint, jsonify
from app.controllers import web_controller
router = Blueprint("router-web", __name__)
    
# Create web routes here
# Homepage
@router.route("/")
def home():
    return web_controller.index_home()
# Account List
@router.route("/account-list")
def emisipage():
    return web_controller.account_list()
# Emisi carbon
@router.route("/emisi-carbon")
def emisi_list():
    return web_controller.emisi_page()