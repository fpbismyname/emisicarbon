from app.extensions import *
from app import db, flask_jwt, IntegrityError
from flask import Blueprint, jsonify, request
from app.database.models.Users import Users
from app.database.models.Sources import Sources
from app.database.models.Emissions import Emissions
from app.database.models.Activities import Activities
from app.database.models.Carbonfactors import CarbonFactors
from app.database.models.Goals import Goals
from app.database.models.Offsets import Offsets
from app.database.models.Reports import Reports

api = Blueprint("controller-api", __name__)

# Create Method for controller the routes
# Login users controller
def login_user():
    data = request.get_json()
    if not data or not data['email'] or not data['password']:
        return jsonify({"status" : 400, "message" : "Please fill the email and password"}),400
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
        return jsonify({"status" : 400, "message" : "Please fill all the fields !"}), 400
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
                "accounts" : users,
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
       if not data:
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

   if methods == "GET" and activityID is None:
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                activity = Activities.query.all()
                activities = [activity.to_dict() for activity in activity]
                if not activities:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            else:
                activity = Activities.query.filter_by(user_id = token['sub'])
                activities = [activity.to_dict() for activity in activity]
                if not activities:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "Get all activities",
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                activity = Activities.query.filter_by(activity_id=activityID).first()
                if not activity:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            else:
                activity = Activities.query.filter_by(user_id=token['sub'], activity_id=activityID).first()
                if not activity:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One emission data found !",
                "activity" : activity.to_dict()
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
       if not data or not data['factor_id'] or not data['amount'] or not data['activity_date']:
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            FactorConversion = CarbonFactors.query.filter_by(factor_id=data['factor_id']).first().to_dict()
            if not FactorConversion:
                return jsonify({"status" : 400, "message" : "Factor data not found !"})
            amountEmisi = float(data['amount']) * float(FactorConversion['conversion_factor'])
            addActivity = Activities(
                user_id = token['sub'],
                factor_id= data['factor_id'],
                amount= data['amount'],
                activity_date= data['activity_date'],
            )
            db.session.add(addActivity)
            db.session.flush()
            db.session.commit()
            addEmission = Emissions(
                activity_id=addActivity.activity_id,
                user_id=token['sub'],
                source_id=FactorConversion['source_id'],
                amount=amountEmisi,
                emission_date=data['activity_date']
            )
            db.session.add(addEmission)
            db.session.commit()
            return jsonify({
                "status" : 201,
                "message" : "Add activity data successfully",
                "added_activity" : data
            }), 201
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                "err" : str(err)
            }), 500
           
    # Update one of source data
   if methods == "PUT" and activityID is not None:
       data = request.get_json()
       if not data['activity_date']:
           return jsonify({"status" : 400, "message" : "Please fill the date !"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                activity = Activities.query.filter_by(activity_id = activityID).first()
                if not activity:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            else:
                activity = Activities.query.filter_by(user_id=token['sub'], activity_id = activityID).first()
                if not activity:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            carbonFactors = CarbonFactors.query.filter_by(factor_id=data['factor_id']).first().to_dict()
            # return FactorConversion
            for emisi in activity.emissions:
                emisi.amount = float(data['amount']) * float(carbonFactors['conversion_factor'])
                emisi.source_id = carbonFactors['source_id']
                emisi.emission_date = data['activity_date']
            # return data.to_dict()
            activity.factor_id= data['factor_id']
            activity.amount= data['amount']
            activity.activity_date= data['activity_date']
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                activity = Activities.query.filter_by(activity_id = activityID).first()
                if not activity:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            else:
                activity = Activities.query.filter_by(user_id=token['sub'], activity_id = activityID).first()
                if not activity:
                    return jsonify({"status": 404, "message": "Activity data not found !"}), 404
            db.session.delete(activity)
            db.session.commit() 
            return jsonify({
                "status" : 202,
                "message" : "Delete activity data successfully",
            }), 202
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                "err" : str(err)
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
       if not data:
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
   
   if methods == "GET" and emissionID is None:
       token = decode_token(request.headers.get('Authorization').split(" ")[1])
       totalEmissions = None
       try:
            if token and token['role'] == "admin":
                emission = Emissions.query.all()
                emissions = [emission.to_dict() for emission in emission]
                if not emissions:
                    return jsonify({"status": 404, "message": "Emission data not found !"}), 404
                totalEmissions = db.session.query(func.sum(Emissions.amount)).scalar()
            else:
                emission = Emissions.query.filter_by(user_id=token['sub'])
                emissions = [emission.to_dict() for emission in emission]
                if not emissions:
                    return jsonify({"status": 404, "message": "Emission data not found !"}), 404
                totalEmissions = db.session.query(func.sum(Emissions.amount)).filter(Emissions.user_id == token['sub']).scalar()
            return jsonify({
                "status" : 200,
                "message" : "Get all emissions",
                "emissions" : emissions,
                "total_emissions" : totalEmissions
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                emission = Emissions.query.filter_by(emission_id = emissionID).first()
                if not emission:
                    return jsonify({"status": 404, "message": "Emission data not found !"}), 404
            else:
                emission = Emissions.query.filter_by(user_id=token['sub'], emission_id = emissionID).first()
                if not emission:
                    return jsonify({"status": 404, "message": "Emission data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One emission data found !",
                "emissions" : emission.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one emission data
#    if methods == "POST" and emissionID is None:
#        data = request.get_json()
#        if not data or not data['user_id'] or not data['source_id'] or not data['amount'] or not data['emission_date'] :
#            return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
#        try:
#             addEmissions = Emissions(
#                 user_id=data['user_id'],
#                 source_id=data['source_id'],
#                 amount=data['amount'],
#                 emission_date=data['emission_date'],
#             )
#             db.session.add(addEmissions)
#             db.session.commit()
#             return jsonify({
#                 "status" : 201,
#                 "message" : "Add data emission successfully",
#                 "added_emission" : data
#             }), 201
#        except IntegrityError as err:
#            return jsonify({
#                 "status" : 500,
#                 "message" : "Internal Server Error",
#                 # "err" : str(err)
#             }), 500
           
#     # Update one of source data
#    if methods == "PUT" and emissionID is not None:
#        data = request.get_json()
#        if not data['emission_date']:
#            return jsonify({"status" : 400, "message" : "Please fill the date !"}),400
#        try:
#             token = decode_token(request.headers.get('Authorization').split(" ")[1])
#             if token and token['role'] == "admin":
#                 emission = Emissions.query.filter_by(emission_id = emissionID).first()
#                 if not emission:
#                     return jsonify({"status": 404, "message": "Emission data not found !"}), 404
#             else:
#                 emission = Emissions.query.filter_by(user_id=token['sub'], emission_id = emissionID).first()
#                 if not emission:
#                     return jsonify({"status": 404, "message": "Emission data not found !"}), 404
#             emission.source_id= data['source_id']
#             emission.amount= data['amount']
#             emission.emission_date= data['emission_date']
#             db.session.commit()
#             return jsonify({
#                 "status" : 200,
#                 "message" : "Update data emission successfully",
#                 "updated_emission" : data
#             }), 200
#        except IntegrityError as err:
#            return jsonify({
#                 "status" : 500,
#                 "message" : "Internal Server Error",
#                 # "err" : str(err)
#             }), 500
       
#     # Delete one of source data
#    if methods == "DELETE" and emissionID is not None:
#        try:
#             token = decode_token(request.headers.get('Authorization').split(" ")[1])
#             if token and token['role'] == "admin":
#                 emission = Emissions.query.filter_by(emission_id = emissionID).first()
#                 if not emission:
#                     return jsonify({"status": 404, "message": "Emission data not found !"}), 404
#             else:
#                 emission = Emissions.query.filter_by(user_id=token['sub'], emission_id = emissionID).first()
#                 if not emission:
#                     return jsonify({"status": 404, "message": "Emission data not found !"}), 404
#             db.session.delete(emission)
#             db.session.commit()
#             return jsonify({
#                 "status" : 202,
#                 "message" : "Delete emission data successfully",
#             }), 202
#        except IntegrityError as err:
#            return jsonify({
#                 "status" : 500,
#                 "message" : "Internal Server Error",
#                 "err" : str(err)
#             }), 500
           
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
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
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
       if not data:
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
   
    # Get all the goals data
   if methods == "GET" and goalID is None:
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                goal = Goals.query.all()
                goals = [goal.to_dict() for goal in goal]
                if not goals:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
                # get data emission
                emission = Emissions.query.all()
                emissions = [emission.to_dict() for emission in emission]
                # get data offset
                offset = Offsets.query.all()
                offsets = [offset.to_dict() for offset in offset]
            else:
                goal = Goals.query.filter_by(user_id = token['sub'])
                goals = [goal.to_dict() for goal in goal]
                if not goals:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
                # get data emission
                emission = Emissions.query.filter(Emissions.user_id == token['sub']).all()
                emissions = [emission.to_dict() for emission in emission]
                # get data offset
                offset = Offsets.query.filter(Offsets.user_id == token['sub']).all()
                offsets = [offset.to_dict() for offset in offset]
                
            # Total emission & Offsets calculation
            totalEmissions = 0.0
            totalOffsets = 0.0
            for emission in emissions:
                amountEmission = emission['amount']
                totalEmissions += float(amountEmission)
            for offset in offsets:
                amountOffset  = offset['offset_amount']
                totalOffsets += float(amountOffset)
            totalReportEmissions = float(totalEmissions) - float(totalOffsets)
            if totalReportEmissions <= 0 :
                totalReportEmissions = 0.0
                
            # total goal
            totalGoalEmissions = 0.0
            
            # Logic current status
            for Goal in goal:
                # get every single goal
                oneGoal = Goal.to_dict()
                # save every goal amount
                totalGoalEmissions += float(oneGoal['target_emission'])
                # Time Now
                current_time = datetime.now().strftime('%Y-%m-%d')
                timeNow = datetime.strptime(str(current_time), '%Y-%m-%d')
                # Deadline
                Deadline = datetime.strptime(oneGoal['deadline'], '%Y-%m-%d' )
                # status got missed if it's on deadline when amount doens't hit the target
                if timeNow >= Deadline:
                    Goal.status = "missed"
                    db.session.commit()
                elif timeNow <= Deadline and totalReportEmissions > oneGoal['target_emission'] :
                    Goal.status = "achieved"
                    db.session.commit()
                elif timeNow <= Deadline and totalReportEmissions < oneGoal['target_emission'] :
                    Goal.status = "in_progress"
                    db.session.commit()
            
            return jsonify({
                "status" : 200,
                "message" : "Get all goals",
                "goals" : goals,
                "total_goal_emissions" : totalGoalEmissions
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                goal = Goals.query.filter_by(goal_id=goalID).first()
                if not goal:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
            else:
                goal = Goals.query.filter_by(user_id=token['sub'], goal_id=goalID).first()
                if not goal:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One goal data found !",
                "source" : goal.to_dict()
            }), 200
       except IntegrityError as err:
           return jsonify({
                "status" : 500,
                "message" : "Internal Server Error",
                # "err" : str(err)
            }), 500
       
    # Add one source data
   if methods == "POST" and goalID is None:
       token = decode_token(request.headers.get('Authorization').split(" ")[1])
       data = request.get_json()
       if not data or not data['target_emission'] or not data['deadline']:
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       if float(data['target_emission']) <= 0:
           return jsonify({"status" : 400, "message" : "Target emission must greater then 0 !"}),400
           
       try:
            addGoal = Goals(
                user_id=token['sub'],
                target_emission=data['target_emission'],
                deadline=data['deadline'],
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
       if not data['deadline']:
           return jsonify({"status" : 400, "message" : "Please fill the date !"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                goal = Goals.query.filter_by(goal_id=goalID).first()
                if not goal:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
            else:
                goal = Goals.query.filter_by(user_id=token['sub'], goal_id=goalID).first()
                if not goal:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                goal = Goals.query.filter_by(goal_id=goalID).first()
                if not goal:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
            else:
                goal = Goals.query.filter_by(user_id=token['sub'], goal_id=goalID).first()
                if not goal:
                    return jsonify({"status": 404, "message": "Goal data not found !"}), 404
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
   
    # Get all the offset data
   if methods == "GET" and offsetID is None:
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                offset = Offsets.query.all()
                offsets = [offset.to_dict() for offset in offset]
                if not offsets:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            else:
                offset = Offsets.query.filter_by(user_id = token['sub'])
                offsets = [offset.to_dict() for offset in offset]
                if not offsets:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "Get all offsets",
                "offsets" : offsets
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                offset = Offsets.query.filter_by(offset_id=offsetID).first()
                if not offset:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            else:
                offset = Offsets.query.filter_by(user_id=token['sub'], offset_id=offsetID).first()
                if not offset:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One offset data found !",
                "source" : offset.to_dict()
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
       if not data or not data['project_name'] or not data['offset_amount'] or not data['offset_date']:
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       if float(data['offset_amount']) <= 0:
           return jsonify({"status" : 400, "message" : "Offset amount must greater then 0 !"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            addOffset = Offsets(
                user_id=token['sub'],
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
       if not data['offset_date']:
           return jsonify({"status" : 400, "message" : "Please fill the date !"}),400
       if float(data['offset_amount']) <= 0:
           return jsonify({"status" : 400, "message" : "Offset amount must greater then 0 !"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                offset = Offsets.query.filter_by(offset_id=offsetID).first()
                if not offset:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            else:
                offset = Offsets.query.filter_by(user_id=token['sub'], offset_id=offsetID).first()
                if not offset:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                offset = Offsets.query.filter_by(offset_id=offsetID).first()
                if not offset:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
            else:
                offset = Offsets.query.filter_by(user_id=token['sub'], offset_id=offsetID).first()
                if not offset:
                    return jsonify({"status": 404, "message": "Offset data not found !"}), 404
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

    # Get all the report data
   if methods == "GET" and reportID is None:
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                # get data report
                dt = Reports.query.all()
                dts = [dt.to_dict() for dt in dt]
                if not dt:
                    return jsonify({"status": 404, "message": "Report data not found !"}),404
                # get data emission
                emission = Emissions.query.all()
                emissions = [emission.to_dict() for emission in emission]
                # get data offset
                offset = Offsets.query.all()
                offsets = [offset.to_dict() for offset in offset]
            else:
                # get data report
                dt = Reports.query.filter(Reports.user_id == token['sub']).all()
                dts = [dt.to_dict() for dt in dt]
                if not dt:
                    return jsonify({"status": 404, "message": "Report data not found !"}),404
                # get data emission
                emission = Emissions.query.filter(Emissions.user_id == token['sub']).all()
                emissions = [emission.to_dict() for emission in emission]
                # get data offset
                offset = Offsets.query.filter(Offsets.user_id == token['sub']).all()
                offsets = [offset.to_dict() for offset in offset]
            # Total emission & Offsets calculation
            totalEmissions = 0.0
            totalOffsets = 0.0
            for emission in emissions:
                amountEmission = emission['amount']
                totalEmissions += float(amountEmission)
            for offset in offsets:
                amountOffset  = offset['offset_amount']
                totalOffsets += float(amountOffset)
            totalReportEmissions = float(totalEmissions) - float(totalOffsets)
            if totalReportEmissions <= 0 :
                totalReportEmissions = 0
                        
            # Update total emission report value
            for data in dt:
                data.total_emission = totalReportEmissions
                db.session.commit()
            
            if token and token['role'] == "admin":
                # get data report
                end_dt = Reports.query.all()
                end_dts = [end_dt.to_dict() for end_dt in end_dt]
                if not dt:
                    return jsonify({"status": 404, "message": "Report data not found !"}),404
            else:
                # get data report
                end_dt = Reports.query.filter(Reports.user_id == token['sub']).all()
                end_dts = [end_dt.to_dict() for end_dt in end_dt]
                if not dt:
                    return jsonify({"status": 404, "message": "Report data not found !"}),404

            return jsonify({
                "status" : 200,
                "message" : "Get all reports",
                "reports" : end_dts,
                "total_emissions" : totalReportEmissions
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                report = Reports.query.filter_by(report_id=reportID).first()
                if not report:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            else:
                report = Reports.query.filter_by(user_id=token['sub'], report_id=reportID).first()
                if not report:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            return jsonify({
                "status" : 200,
                "message" : "One report  data found !",
                "source" : report.to_dict()
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
       if not data or not data['start_date'] or not data['end_date']:
           return jsonify({"status" : 400, "message" : "Please fill all the fields !"}),400
       start_date = datetime.strptime(str(data['start_date']), '%Y-%m-%d').date()
       end_date = datetime.strptime(str(data['end_date']), '%Y-%m-%d').date()
       if start_date > end_date:
           return jsonify({"status" : 400, "message" : "Start date should be less then end date"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                data = Emissions.query.filter(Emissions.emission_date >= start_date, Emissions.emission_date <= end_date).all()
                datas = [data.to_dict() for data in data]
                # get data offset
                offset = Offsets.query.all()
                offsets = [offset.to_dict() for offset in offset]
                if not datas:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            else:
                data = Emissions.query.filter(Emissions.emission_date >= start_date, Emissions.emission_date <= end_date, Emissions.user_id == token['sub']).all()
                datas = [data.to_dict() for data in data]
                # get data offset
                offset = Offsets.query.filter(Offsets.user_id == token['sub']).all()
                offsets = [offset.to_dict() for offset in offset]
                if not datas:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            # total emission
            totalEmissions = 0.0
            # total offset
            totalOffsets = 0.0
            
            for emission in datas:
                totalEmissions += float(emission['amount'])
            for offset in offsets:
                totalOffsets += float(offset['offset_amount'])
            
            # Calculate Emission - Offset
            total_emission = totalEmissions - totalOffsets
            # Checking value to dont < from 0
            if total_emission < 0:
                total_emission = 0.0
            
            addReport = Reports(
                user_id=token['sub'],
                start_date=start_date,
                end_date=end_date,
                total_emission=total_emission
            )
            db.session.add(addReport)
            db.session.commit()
            return jsonify({
                "status" : 201,
                "message" : "Add Report data successfully",
                "added_report" : addReport.total_emission
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
       if not data['start_date'] or not data['end_date']:
           return jsonify({"status" : 400, "message" : "Please fill the date !"}),400
       start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
       end_date = datetime.strptime(str(data['end_date']), '%Y-%m-%d').date()
       if start_date > end_date:
           return jsonify({"status" : 400, "message" : "Start date should be less then end date"}),400
       try:
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                report = Reports.query.filter(Reports.report_id == reportID).first()
                dt = Emissions.query.filter(Emissions.emission_date >= start_date, Emissions.emission_date <= end_date).all()
                dts = [dt.to_dict() for dt in dt]
                # get data offset
                offset = Offsets.query.all()
                offsets = [offset.to_dict() for offset in offset]
                if not dts:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            else:
                report = Reports.query.filter(Reports.report_id == reportID, Reports.user_id == token['sub']).first()
                dt = Emissions.query.filter(Emissions.emission_date >= start_date, Emissions.emission_date <= end_date, Emissions.user_id == token['sub']).all()
                dts = [dt.to_dict() for dt in dt]
                # get data offset
                offset = Offsets.query.filter(Offsets.user_id == token['sub']).all()
                offsets = [offset.to_dict() for offset in offset]
                if not dts:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            # total emission
            totalEmissions = 0.0
            # total offset
            totalOffsets = 0.0
            
            for emission in dts:
                totalEmissions += float(emission['amount'])
            for offset in offsets:
                totalOffsets += float(offset['offset_amount'])
            
            # Calculate Emission - Offset
            total_emission = float(totalEmissions) - float(totalOffsets)
            # Checking value to dont < from 0
            if total_emission < 0:  
                total_emission = 0.0
            
            report.start_date= data['start_date']
            report.end_date= data['end_date']
            report.total_emission=total_emission
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
            token = decode_token(request.headers.get('Authorization').split(" ")[1])
            if token and token['role'] == "admin":
                report = Reports.query.filter_by(report_id=reportID).first()
                if not report:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
            else:
                report = Reports.query.filter_by(user_id=token['sub'], report_id=reportID).first()
                if not report:
                    return jsonify({"status": 404, "message": "Report data not found !"}), 404
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