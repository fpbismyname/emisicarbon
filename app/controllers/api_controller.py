import json
from dateutil.parser import parse
from app.extensions import *
from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.Users import Users
from app.database.models.Sources import Sources
from app.database.models.Emissions import Emissions
from app.database.models.Activities import Activities
from app.database.models.Carbon_factors import CarbonFactors
from app.database.models.Goals import Goals
from app.database.models.Offsets import Offsets
from app.database.models.Reports import Reports

controller = Blueprint("controller-api", __name__)

# Create Method for controll the routes

# Controller for Users
def users(type):
    
    # Register Process
    if type == "register":
        data = request.get_json()
        if not data or not data['email'] or not data['username'] or not data['password']:
            return jsonify({"status" : 400, "message" : "Invalid Request, please fill the username and password"})
        checkDuplication = Users.query.filter_by(email=data['email']).first()
        if checkDuplication:
            return jsonify({"status" : 409, "message" : "Account already exists"}), 409
        try:
            newUsers = Users(username=data['username'], email=data['email'])
            newUsers.set_password(data['password'])
            db.session.add(newUsers)  
            db.session.commit() 
            return jsonify({
                "status" : 200,
                "message": "Register Success"
                }), 200
        except IntegrityError:
            return jsonify({
                    "status" : 500,
                    "message": "Internal Server Error !",
            }), 500
            
    # Login Process
    if type == "login":
        data = request.get_json()
        if not data or not data['email'] or not data['password']:
            return jsonify({"status" : 400, "message" : "Invalid Request, please fill the email and password"})
        currentUsers = Users.query.filter_by(email=data['email']).first()
        if not currentUsers : return jsonify({"status": 404, "message": "Invalid Credentials !"}), 404
        currentUser = currentUsers.to_dict()
        try:
            if not Users.check_password(currentUser['password_hash'], data['password']) : return jsonify({"status":404, "message" : "Invalid Credentials !"}), 404
            identity_user = {
                'user_id': currentUser['user_id'],
                'username': currentUser['username'],
                'role' : currentUser['role']
            }
            bearer_token = flask_jwt.create_access_token(identity=str(identity_user))
            return jsonify({
                "status" : 200,
                "role" : currentUser['role'],
                "message": "Login Success",
                "bearer_token" : bearer_token
            }), 200 
        except IntegrityError:
            return jsonify({"status": 500, "message": "Internal Server Error"}), 500

# Sources Controller
def sources(source_id):
   methods = request.method
   sourceID = source_id
   
    # Get all the source data
   if methods == "GET" and sourceID is None:
       try:
            source = Sources.query.all()
            sources = [source.to_dict() for source in source]
            return jsonify({
                "status" : 200,
                "message" : "Get all sources",
                "sources" : sources
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
           
    # Get one of source data
   if methods == "GET" and sourceID is not None:
       try:
            oneSource = Sources.query.get(sourceID)
            if not oneSource:
                return jsonify({"status": 404, "message": "Source not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One source data found !",
                "source" : oneSource.to_dict()
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
       
    # Add one source data
   if methods == "POST" and sourceID is None:
       data = request.get_json()
       if not data or not data['source_name'] or not data['description']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addSource = Sources(source_name=data['source_name'], description=data['description'])
            db.session.add(addSource)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add data source successfully",
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
           
    # Update one of source data
   if methods == "PUT" and sourceID is not None:
       data = request.get_json()
       if not data or not data['source_name'] or not data['description']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}), 400
       try:
            source = Sources.query.get(sourceID)
            if not source:
                return jsonify({"status": 404, "message": "Source not found !"}),404
            source.source_name = data['source_name']
            source.description = data['description']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update data source successfully",
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and sourceID is not None:
       try:
            source = Sources.query.get(sourceID)
            if not source:
                return jsonify({"status": 404, "message": "Source not found !"}),404
            db.session.delete(source)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Delete data source successfully",
            }), 200
       except IntegrityError:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
            }), 500

# Emisions Controller
def emissions(emission_id):
   methods = request.method
   emissionID = emission_id
   
    # Get all the source data
   if methods == "GET" and emissionID is None:
       try:
            emission = Emissions.query.all()
            emissions = [emission.to_dict() for emission in emission]
            return jsonify({
                "status" : 200,
                "message" : "Get all emissions",
                "emissions" : emissions
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Get one of source data
   if methods == "GET" and emissionID is not None:
       try:
            oneEmission = Emissions.query.get(emissionID)
            if not oneEmission:
                return jsonify({"status": 404, "message": "Emission data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One emission data found !",
                "emissions" : oneEmission.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and emissionID is None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['source_id'] or not data['amount'] or not data['emission_date'] or not data['report_date']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addEmissions = Emissions(
                user_id=data['user_id'],
                source_id=data['source_id'],
                amount=data['amount'],
                emission_date=data['emission_date'],
                report_date=data['report_date']
            )
            db.session.add(addEmissions)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add data emission successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and emissionID is not None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['source_id'] or not data['amount'] or not data['emission_date'] or not data['report_date']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            emission = Emissions.query.get(emissionID)
            if not emission:
                return jsonify({"status": 404, "message": "Emission not found !"}),404
            emission.user_id = data['user_id']
            emission.source_id= data['source_id']
            emission.amount= data['amount']
            emission.emission_date= data['emission_date']
            emission.report_date= data['report_date']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update data emission successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and emissionID is not None:
       try:
            emission = Emissions.query.get(emissionID)
            if not emission:
                return jsonify({"status": 404, "message": "Emission data not found !"}),404
            db.session.delete(emission)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Delete emission data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                "err" : str(err)
            }), 500
           
# Carbon Factor Controller
def carbon_factors(carbonFact_id):
   methods = request.method
   carbonFactorID = carbonFact_id
   
    # Get all the source data
   if methods == "GET" and carbonFactorID is None:
       try:
            carbonFact = CarbonFactors.query.all()
            carbonFacts = [carbonFact.to_dict() for carbonFact in carbonFact]
            return jsonify({
                "status" : 200,
                "message" : "Get all carbon factors",
                "carbon_factors" : carbonFacts,
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Get one of source data
   if methods == "GET" and carbonFactorID is not None:
       try:
            oneCarbonFact = CarbonFactors.query.get(carbonFactorID)
            if not oneCarbonFact:
                return jsonify({"status": 404, "message": "Emission data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One emission data found !",
                "carbon_factors" : oneCarbonFact.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and carbonFactorID is None:
       data = request.get_json()
       if not data or not data['source_id'] or not data['description'] or not data['conversion_factor'] or not data['unit']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addCarbonFact = CarbonFactors(
                source_id=data['source_id'],
                description=data['description'],
                conversion_factor=data['conversion_factor'],
                unit=data['unit']
            )
            db.session.add(addCarbonFact)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add carbon factor data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and carbonFactorID is not None:
       data = request.get_json()
       if not data or not data['source_id'] or not data['description'] or not data['conversion_factor'] or not data['unit']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            carbonFact = CarbonFactors.query.get(carbonFactorID)
            if not carbonFact:
                return jsonify({"status": 404, "message": "Carbon factor not found !"}),404
            carbonFact.source_id= data['source_id']
            carbonFact.amount= data['description']
            carbonFact.emission_date= data['conversion_factor']
            carbonFact.report_date= data['unit']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update carbon factor data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and carbonFactorID is not None:
       try:
            carbonFact = CarbonFactors.query.get(carbonFactorID)
            if not carbonFact:
                return jsonify({"status": 404, "message": "Carbon factor not found !"}),404
            db.session.delete(carbonFact)
            db.session.commit() 
            return jsonify({
                "status" : 200,
                "message" : "Delete carbon factor data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
# Goals Controller
def goals(goals_id):
   methods = request.method
   goalID = goals_id
   
    # Get all the source data
   if methods == "GET" and goalID is None:
       try:
            goals = Goals.query.all()
            goal = [goals.to_dict() for goals in goals]
            return jsonify({
                "status" : 200,
                "message" : "Get all goals",
                "goals" : goal,
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Get one of source data
   if methods == "GET" and goalID is not None:
       try:
            oneGoal = Goals.query.get(goalID)
            if not oneGoal:
                return jsonify({"status": 404, "message": "Goal data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One goal data found !",
                "source" : oneGoal.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and goalID is None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['target_emission'] or not data['deadline']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addGoal = Goals(
                user_id=data['user_id'],
                target_emission=data['target_emission'],
                deadline=data['deadline']
            )
            db.session.add(addGoal)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add goal data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and goalID is not None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['target_emission'] or not data['deadline']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            goal = Goals.query.get(goalID)
            if not goal:
                return jsonify({"status": 404, "message": "Goal data not found !"}),404
            goal.user_id= data['user_id']
            goal.target_emission= data['target_emission']
            goal.deadline= data['deadline']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update goal data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and goalID is not None:
       try:
            goal = Goals.query.get(goalID)
            if not goal:
                return jsonify({"status": 404, "message": "Carbon factor not found !"}),404
            db.session.delete(goal)
            db.session.commit() 
            return jsonify({
                "status" : 200,
                "message" : "Delete goal data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                "err" : str(err)
            }), 500
           
# Offsets Controller
def offsets(offsets_id):
   methods = request.method
   offsetID = offsets_id
   
    # Get all the source data
   if methods == "GET" and offsetID is None:
       try:
            offsets = Offsets.query.all()
            offset = [offsets.to_dict() for offsets in offsets]
            return jsonify({
                "status" : 200,
                "message" : "Get all offsets",
                "offsets" : offset
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Get one of source data
   if methods == "GET" and offsetID is not None:
       try:
            oneOffset = Offsets.query.get(offsetID)
            if not oneOffset:
                return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One goal data found !",
                "source" : oneOffset.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and offsetID is None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['project_name'] or not data['offset_amount'] or not data['offset_date']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addOffset = Offsets(
                user_id=data['user_id'],
                project_name=data['project_name'],
                offset_amount=data['offset_amount'],
                offset_date=data['offset_date']
            )
            db.session.add(addOffset)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add offset data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and offsetID is not None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['project_name'] or not data['offset_amount'] or not data['offset_date']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            offset = Offsets.query.get(offsetID)
            if not offset:
                return jsonify({"status": 404, "message": "Offset data not found !"}),404
            offset.user_id= data['user_id']
            offset.project_name= data['project_name']
            offset.offset_amount=data['offset_amount']
            offset.offset_date=data['offset_date']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update offset data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and offsetID is not None:
       try:
            offset = Offsets.query.get(offsetID)
            if not offset:
                return jsonify({"status": 404, "message": "Carbon factor not found !"}),404
            db.session.delete(offset)
            db.session.commit() 
            return jsonify({
                "status" : 200,
                "message" : "Delete offset data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
# Reports Controller
def reports(reports_id):
   methods = request.method
   reportID = reports_id
   
    # Get all the source data
   if methods == "GET" and reportID is None:
       try:
            reports = Reports.query.all()
            report = [reports.to_dict() for reports in reports]
            return jsonify({
                "status" : 200,
                "message" : "Get all offsets",
                "reports" : report
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Get one of source data
   if methods == "GET" and reportID is not None:
       try:
            oneReport = Reports.query.get(reportID)
            if not oneReport:
                return jsonify({"status": 404, "message": "Report data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One goal data found !",
                "source" : oneReport.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and reportID is None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['start_date'] or not data['end_date'] or not data['total_emission']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            addReport = Reports(
                user_id=data['user_id'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                total_emission=data['total_emission']
            )
            db.session.add(addReport)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add Report data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and reportID is not None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['start_date'] or not data['end_date'] or not data['total_emission']:
           return jsonify({"status" : 400, "message" : "Invalid Request, please fill all the fields !"}),400
       try:
            report = Reports.query.get(reportID)
            if not report:
                return jsonify({"status": 404, "message": "Report data not found !"}),404
            report.user_id= data['user_id']
            report.start_date= data['start_date']
            report.end_date=data['end_date']
            report.total_emission=data['total_emission']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update report data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and reportID is not None:
       try:
            report = Reports.query.get(reportID)
            if not report:
                return jsonify({"status": 404, "message": "Report data not found !"}),404
            db.session.delete(report)
            db.session.commit() 
            return jsonify({
                "status" : 200,
                "message" : "Delete report data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500