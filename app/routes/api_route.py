from app.extensions import *
from app.controllers import api_controller
from flask import Blueprint, jsonify
api = Blueprint("router-api", __name__)
    
# Create api routes here
# Base URL endpoint
URL = "/emisi-carbon/api/v1"

# Route for register API
@api.route(f"{URL}/register", methods=['POST'])
def register():
    return api_controller.users(type="register")

# Route for login API
@api.route(f"{URL}/login", methods=['POST'])
def login():
    return api_controller.users(type="login")

# Route for CRUD Activities
@api.route(f"{URL}/activities", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/activities/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def activities(id):
    return api_controller.activities(activity_id= id)

# Route for CRUD sources
@api.route(f"{URL}/sources", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/sources/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def sources(id):
    return api_controller.sources(source_id = id)

# Route for CRUD Emisions
@api.route(f"{URL}/emissions", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/emissions/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def emissions(id):
    return api_controller.emissions(emission_id= id)

# Route for CRUD Carbon Factors
@api.route(f"{URL}/carbon-factors", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/carbon-factors/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def carbon_factor(id):
    return api_controller.carbon_factors(carbonFact_id= id)

# Route for CRUD Goals
@api.route(f"{URL}/goals", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/goals/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def goals(id):
    return api_controller.goals(goals_id = id)

# Route for CRUD Offsets
@api.route(f"{URL}/offsets", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/offsets/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def offsets(id):
    return api_controller.offsets(offsets_id = id)

# Route for CRUD Reports
@api.route(f"{URL}/reports", defaults={'id' : None }, methods=[ 'GET', 'POST'])
@api.route(f"{URL}/reports/<int:id>", methods=['GET','PUT','DELETE'])
@jwt_required()
def reports(id):
    return api_controller.reports(reports_id = id)