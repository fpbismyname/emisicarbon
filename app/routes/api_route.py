from app.extensions import *
from app.controllers import api_controller
from flask import Blueprint, jsonify
router = Blueprint("router-api", __name__)
    
# Create api routes here
# Base URL endpoint
URL = "/emisi-carbon/api/v1"

# Route for register API
@router.route(f"{URL}/register", methods=['POST'])
def register():
    return api_controller.users(type="register")

# Route for login API
@router.route(f"{URL}/login", methods=['POST'])
def login():
    return api_controller.users(type="login")

# Route for CRUD sources
@router.route(f"{URL}/sources", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@router.route(f"{URL}/sources/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def sources(id):
    return api_controller.sources(source_id = id)

# Route for CRUD Emisions
@router.route(f"{URL}/emissions", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@router.route(f"{URL}/emissions/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def emissions(id):
    return api_controller.emissions(emission_id= id)

# Route for CRUD Emisions
@router.route(f"{URL}/carbon-factors", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@router.route(f"{URL}/carbon-factors/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def carbon_factor(id):
    return api_controller.carbon_factors(carbonFact_id= id)

# Route for CRUD Emisions
@router.route(f"{URL}/goals", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@router.route(f"{URL}/goals/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def goals(id):
    return api_controller.goals(goals_id = id)