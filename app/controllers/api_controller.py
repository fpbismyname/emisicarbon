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

# Login users controller
def login_user():
    data = request.get_json()
    if not data or not data['email'] or not data['password']:
        return jsonify({"status" : 400, "message" : "Invalid Request, please fill the email and password"}),400
    currentUsers = Users.query.filter_by(email=data['email']).first()
    if not currentUsers : return jsonify({"status": 404, "message": "Invalid Credentials !"}), 404
    currentUser = currentUsers.to_dict()
    try:
        if not Users.check_password(currentUser['password_hash'], data['password']) : 
            return jsonify({"status":404, "message" : "Invalid Credentials !"}), 404
        user_id = str(currentUser['user_id'])
        addional_claims= {
            'username': currentUser['username'],
            'role' : currentUser['role'],
            'password' : currentUser['password_hash'] 
        }
        bearer_token = flask_jwt.create_access_token(identity=user_id, additional_claims=addional_claims)
        return jsonify({
            "status" : 200,
            "role" : currentUser['role'],
            "message": "Login Success",
            "bearer_token" : bearer_token
        }), 200 
    except IntegrityError:
        return jsonify({"status": 500, "message": "Internal Server Error"}), 500 

# Register users controller
def register_user():
    data = request.get_json()
    if not data or not data['email'] or not data['username'] or not data['password'] or not data['role']:
        return jsonify({"status" : 400, "message" : "Please fill the username and password"}), 400
    role = data['role'] if data['role'] != "admin" else "user"
    checkDuplicationEmail = Users.query.filter_by(email=data['email']).first()
    checkDuplicationUsername = Users.query.filter_by(username=data['username']).first()
    
    if checkDuplicationEmail or checkDuplicationUsername:
        return jsonify({"status" : 409, "message" : "Account already exists"}), 409
    try:
        newUsers = Users(username=data['username'], email=data['email'], role=role) 
        newUsers.set_password(data['password'])
        db.session.add(newUsers)  
        db.session.commit() 
        return jsonify({
            "status" : 201,
            "message": "Register Success"
            }), 201
    except IntegrityError:
        return jsonify({
                "status" : 500,
                "message": "Internal Server Error !",
        }), 500
   
# Activities Controller
def users(users_id):
   methods = request.method
   userID = users_id
   
   if methods == "GET" and userID is None:
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token['role'] != 'admin':
                return jsonify({"status": 403, "message": "Forbidden"}), 403
            if not request.get_data():
                # data = request.get_json()
                user = Users.query.all()
                users = [user.to_dict() for user in user]
            else :
                data = request.get_json()
                if not data or not data['email']:
                    return jsonify({"status" : 400, "message" : "Please fill the email"}),400
                user = Users.query.filter_by(email=data['email'])
                users = [user.to_dict() for user in user]
            return jsonify({
                "status" : 200,
                "message" : "Get all users",
                "Accounts" : users,
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
   if methods == "POST" and userID is None:
        data = request.get_json()
        if not data or not data['username'] or not data['email'] or not data['password'] or not data['role']:
            return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
        try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token['role'] != 'admin':
                return jsonify({"status": 403, "message": "Forbidden"}), 403
            checkDuplicationEmail = Users.query.filter_by(email=data['email']).first()
            checkDuplicationUsername = Users.query.filter_by(username=data['username']).first()
            if checkDuplicationEmail or checkDuplicationUsername:
                return jsonify({"status" : 409, "message" : "Account already exists"}), 409
            user = Users(username=data['username'], email=data['email'], role=data['role'])
            user.set_password(password=data['password'])
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "status" : 201,
                "message" : "Create account successfully !",
                "Accounts" : data
            }), 201
        except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500   
   if methods == "PUT" and userID is not None:
       data = request.get_json()
       if not data or not data['username'] or not data['email'] or not data['role']:
            return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token['role'] != 'admin':
                return jsonify({"status": 403, "message": "Forbidden"}), 403
            user = Users.query.get(userID)
            if not user:
                return jsonify({"status": 404, "message": "User not found !"}),404
            if data['password'] : 
                newPassword = bcrypt.generate_password_hash(data['password'])
                user.password_hash= newPassword.decode('utf-8')
            user.username= data['username']
            user.email= data['email']
            user.role= data['role']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Edit account data successfully",
                "edited_account" : data
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and userID is not None:
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token['role'] != 'admin':
                return jsonify({"status": 403, "message": "Forbidden"}), 403
            user = Users.query.get(userID)
            if not user:
                return jsonify({"status": 404, "message": "Account not found !"}),404
            db.session.delete(user)
            db.session.commit() 
            return jsonify({
                "status" : 202,
                "message" : "Delete Account data successfully",
            }), 202
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
   
           
# Activities Controller
def activities(activity_id):
   methods = request.method
   activityID = activity_id
   
    # Get all the Activities data
   if methods == "GET" and activityID is None:
       try:
            activity = Activities.query.all()
            activities = [activity.to_dict() for activity in activity]
            return jsonify({
                "status" : 200,
                "message" : "Get all carbon factors",
                "activities" : activities,
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Get one of Activities data
   if methods == "GET" and activityID is not None:
       try:
            oneActivity = Activities.query.get(activityID)
            if not oneActivity:
                return jsonify({"status": 404, "message": "Emission data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One emission data found !",
                "activity" : oneActivity.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and activityID is None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['factor_id'] or not data['amount'] or not data['activity_date'] or not data['report_date']:
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       try:
            addActivity = Activities(
                user_id = data['user_id'],
                factor_id= data['factor_id'],
                amount= data['amount'],
                activity_date= data['activity_date'],
                report_date= data['report_date']
            )
            db.session.add(addActivity)
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Add carbon factor data successfully",
                "added_activity" : data
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and activityID is not None:
       data = request.get_json()
       if not data or not data['user_id'] or not data['factor_id'] or not data['amount'] or not data['activity_date'] or not data['report_date']:
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       try:
            activity = Activities.query.get(activityID)
            if not activity:
                return jsonify({"status": 404, "message": "Activity not found !"}),404
            activity.user_id= data['user_id']
            activity.factor_id= data['factor_id']
            activity.amount= data['amount']
            activity.activity_date= data['activity_date']
            activity.report_date= data['report_date']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update carbon factor data successfully",
                "updated_activity" : data
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Delete one of source data
   if methods == "DELETE" and activityID is not None:
       try:
            activity = Activities.query.get(activityID)
            if not activity:
                return jsonify({"status": 404, "message": "Activity not found !"}),404
            db.session.delete(activity)
            db.session.commit() 
            return jsonify({
                "status" : 200,
                "message" : "Delete activity data successfully",
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500

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
                "status" : 201,
                "message" : "Add data source successfully",
                "added_source" : data
            }), 201
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
                "Updated_source" : data
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
                "status" : 202,
                "message" : "Delete data source successfully",
            }), 202
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
                "status" : 201,
                "message" : "Add data emission successfully",
                "added_emission" : data
            }), 201
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
                "updated_emission" : data
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
                "status" : 202,
                "message" : "Delete emission data successfully",
            }), 202
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
                "status" : 201,
                "message" : "Add carbon factor data successfully",
                "added_carbon_factor" : data
            }), 201
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
            carbonFact.description= data['description']
            carbonFact.conversion_factor= data['conversion_factor']
            carbonFact.unit= data['unit']
            db.session.commit()
            return jsonify({
                "status" : 200,
                "message" : "Update carbon factor data successfully",
                "updated_carbon_factor" : data
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
                "status" : 202,
                "message" : "Delete carbon factor data successfully",
            }), 202
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
                "status" : 201,
                "message" : "Add goal data successfully",
                "added_goal" : data
            }), 201
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
                "updated_goal" : data
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
                "status" : 202,
                "message" : "Delete goal data successfully",
            }), 202
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
                "message" : "One offset data found !",
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
                "status" : 201,
                "message" : "Add offset data successfully",
                "added_offset" : data
            }), 201
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
                "updated_offset" : data
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
                "status" : 202,
                "message" : "Delete offset data successfully",
            }), 202
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
                "message" : "Get all reports",
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
                "message" : "One report  data found !",
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
                "status" : 201,
                "message" : "Add Report data successfully",
                "added_report" : data
            }), 201
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
                "updated_report" : data
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
                "status" : 202,
                "message" : "Delete report data successfully",
            }), 202
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500