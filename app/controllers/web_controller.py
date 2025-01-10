import requests
from app.extensions import *
controller = Blueprint("controller-web", __name__)


# URL API
url = "http://127.0.0.1:5000/emisi-carbon/api/v1"
    
# Create Method for controll the routes

# region LoginPage
def login_page():
    if request.method == "POST" :
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            payloads = {
                "email": request.form.get("email"),
                "password": request.form.get("password"),
            }
            response = requests.post(url=f"{url}/login", json=payloads, headers=headers)
            res_data = response.json()
            
            if response.status_code == 200:
                userToken = decode_token(res_data['bearer_token'])
                session['id_user'] = userToken['sub']
                session['username'] = userToken['username']
                session['role'] = res_data['role']
                session['access_token_cookie'] = res_data['bearer_token']
                return redirect(url_for('router-web.dashboard'))
            elif response.status_code == 400:
                flash(res_data['message'], "danger")
                return redirect(url_for('router-web.login'))
            elif response.status_code == 404:
                flash(res_data['message'], "danger")
                return redirect(url_for('router-web.login'))
        except ZeroDivisionError:
            return {"error" : "Error"}
    return render_template("auth/login.html")
# endregion

# region RegisterPage
def register_page():
    if request.method == "POST" :
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            payloads = {
                "username": request.form.get("username"),
                "role": request.form.get("role"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
            }
            response = requests.post(url=f"{url}/register", json=payloads, headers=headers)
            res_data = response.json()
            if response.status_code == 201:
                flash(res_data['message'], 'success')
                return redirect(url_for('router-web.login'))
            elif response.status_code == 400:
                flash(res_data['message'], 'danger')
                return redirect(url_for('router-web.register'))
            elif response.status_code == 409:
                flash(res_data['message'], 'danger')
                return redirect(url_for('router-web.register'))
        
        except ZeroDivisionError:
            return {"error" : "Error"}
    return render_template("auth/register.html")
# endregion

# region logout function
def logout_page():
    session.clear()
    return redirect(url_for('router-web.login'))
# endregion

# region DashboardPage
def dashboard_page():
    # region fetch api
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url}/emissions", headers=headers)
    allEmission = response.json()
    # endregion   
    # region data dashboard
    data = {
        "title" : "Dashboard",
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : {
            "dashboard" : True,
            "activities" : False,
            "sources" : False,
            "emissions" : False,
            "factor_carbons" : False,
            "goals" : False,
            "offsets" : False,
            "reports" : False,
            "users" : False
        },
        "totalEmisi" : allEmission
    }
    # endregion
    return render_template("page/dashboard.html", data = data)
# endregion

# region kelola users
# View users
def users_page(user_id):
    methods = request.form.get("_method")
    userId = user_id
    # methods
    if methods is None and userId is None:
        return users_get()
    if methods == "POST" and userId is None:
        return users_add()
    if methods == "PUT" and userId is not None:
        return users_edit(userId)
    if methods == "DELETE" and userId is not None:
        return users_delete(userId)
# region users add
def users_add():
    # region fetch api
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = {
                "username": request.form.get("username"),
                "role": request.form.get("role"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
            }
    response = requests.post(url=f"{url}/users", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for("router-web.users"))
    # endregion
# endregion
# region user get
def users_get():
    # region fetch api
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url}/users", headers=headers)
    alldata = response.json()
    # endregion
    # region data users
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : "Kelola user",
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : {
            "dashboard" : False,
            "activities" : False,
            "sources" : False,
            "emissions" : False,
            "factor_carbons" : False,
            "goals" : False,
            "offsets" : False,
            "reports" : False,
            "users" : True
        },
        "datas" : alldata
    }
    return render_template("page/users.html", data=data)
    # endregion
# endregion
# region users edit
def users_edit(users_id = None):
    # region fetch api
    user_id = users_id
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = {
                "username": request.form.get("username"),
                "role": request.form.get("role"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
            }
    response = requests.put(url=f"{url}/users/{user_id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        if payloads['password'] and session.get('username') == payloads['username']:
            session.clear()
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for("router-web.users"))
    # endregion
# endregion
# region users delete
def users_delete(users_id = None):
    # region fetch api
    user_id = users_id
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url}/users/{user_id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        if session.get('user_id') == user_id:
            session.clear()
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for("router-web.users"))
    # endregion
# endregion
# endregion

# region kelola activities
# View activities
def activities_page(id):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return activities_get()
    if methods == "POST" and Id is None:
        return activities_add()
    if methods == "PUT" and Id is not None:
        return activities_edit(Id)
    if methods == "DELETE" and Id is not None:
        return users_delete(Id)
# region user get
def activities_get():
    # region fetch api
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url}/activities", headers=headers)
    alldata = response.json()
    # endregion
    # region data users
    # function 
    def formatTime(dates, format="%d-%m-%Y %H:%M:%S"):
        return dates.strftime(format)
    function = {
        "current_time" : formatTime
    }
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : "Kelola Aktivitas",
        "username" : session.get('username'),
        "role" : session.get('role'),
        "func" : function,
        "menu" : {
            "dashboard" : False,
            "activities" : True,
            "sources" : False,
            "emissions" : False,
            "factor_carbons" : False,
            "goals" : False,
            "offsets" : False,
            "reports" : False,
            "users" : False
        },
        "datas" : alldata
    }
    return render_template("page/activities.html", data=data)
    # endregion
# endregion
# region activity add
def activities_add():
    # region fetch api
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = {
                "user_id": request.form.get("user_id"),
                "factor_id": request.form.get("factor_id"),
                "amount": request.form.get("amount"),
                "activity_date": request.form.get("activity_date"),
            }
    response = requests.post(url=f"{url}/activities", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for("router-web.activities"))
    # endregion
# endregion
# region users edit
def activities_edit(id = None):
    # region fetch api
    Id = id
    method = "activities"
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = {
                "user_id": request.form.get("user_id"),
                "factor_id": request.form.get("factor_id"),
                "amount": request.form.get("amount"),
                "activity_date": request.form.get("activity_date"),
            }
    response = requests.put(url=f"{url}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for("router-web.activities"))
    # endregion
# endregion
# region users delete
def users_delete(id = None):
    # region fetch api
    Id = id
    method = "activities"
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for("router-web.activities"))
    # endregion
# endregion
# endregion