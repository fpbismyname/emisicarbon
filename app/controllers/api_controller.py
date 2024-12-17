import json
from flask import Blueprint, jsonify
from app.models.model import Account, Emisi
controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes

# Account
def account_get_data():
    datas = Account.query.all()
    data = [data.to_dict() for data in datas]
    return jsonify({
        "status" : 200,
        "message": "Request Succeed",
        "data" : data
    })
    
# Emisi
def emisi_get_data():
    datas = Emisi.query.all()
    data = [data.to_dict() for data in datas]
    return jsonify({
        "status" : 200,
        "message": "Request Succeed",
        "data" : data
    })