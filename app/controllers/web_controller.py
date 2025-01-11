import requests
from app.extensions import *
web = Blueprint("controller-web", __name__)


# URL API
url_api = "http://127.0.0.1:5000/emisi-carbon/api/v1"
    
# Create Method for controll the routes
# Menu selecter controller
def menuBar(method):
    data = {
            "dashboard" : True if method == "dashboard" else False,
            "users" : True if method == "users" else False,
            "activities" : True if method == "activities" else False,
            "sources" : True if method == "sources" else False,
            "emissions" : True if method == "emissions" else False,
            "carbon_factors" : True if method == "carbon_factors" else False,
            "goals" : True if method == "goals" else False,
            "offsets" : True if method == "offsets" else False,
            "reports" : True if method == "reports" else False
        }
    return json.dumps(data)

# payload loader controller
def payload(method_url):
    payloads = {}
    match method_url:
        case "users":
            payloads = {
                "username": request.form.get("username"),
                "role": request.form.get("role"),
                "email": request.form.get("email"),
                "password": request.form.get("password"),
            }
        case "activities":
            payloads = {
                "user_id": request.form.get("user_id"),
                "factor_id": request.form.get("factor_id"),
                "amount": request.form.get("amount"),
                "activity_date": request.form.get("activity_date"),
            }
        case "sources":
            payloads = {
                "source_name": request.form.get("source_name"),
                "description": request.form.get("description"),
            }
        case "emissions":
            payloads = {
                    "user_id" : request.form.get("user_id"),
                    "source_id" : request.form.get("source_id"),
                    "amount" : request.form.get("amount"),
                    "emission_date" : request.form.get("emission_date"),
                }
        case "carbon_factors":
            payloads = {
                "source_id" : request.form.get("source_id"),
                "description" : request.form.get("description"),
                "conversion_factor" : request.form.get("conversion_factor"),
                "unit" : request.form.get("unit")
            }
        case "goals":
            payloads = {
                "user_id" : request.form.get("user_id")	,
                "target_emission" : request.form.get("target_emission"),
                "deadline" : request.form.get("deadline"),
                "status" : request.form.get("status")
            }
        case "goals":
            payloads = {
                "user_id" : request.form.get("user_id")	,
                "target_emission" : request.form.get("target_emission"),
                "deadline" : request.form.get("deadline")
            }
        case "offsets":
            payloads = {
                    "user_id" : request.form.get("user_id"),
                    "project_name" : request.form.get("project_name"),
                    "offset_amount" : request.form.get("offset_amount"),
                    "offset_date" : request.form.get("offset_date")
                }
        case "reports":
            payloads = {
                "user_id" : request.form.get("user_id"),
                "start_date" : request.form.get("start_date"),
                "end_date" : request.form.get("end_date"),
                "total_emission" : request.form.get("total_emission")
            }
    return json.dumps(payloads)

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
            response = requests.post(url=f"{url_api}/login", json=payloads, headers=headers)
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
            response = requests.post(url=f"{url_api}/register", json=payloads, headers=headers)
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
def dashboard_page(method_url, title=""):
    method = method_url
    # region fetch api
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/emissions", headers=headers)
    allEmission = response.json()
    # endregion   
    # region data dashboard
    data = {
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "totalEmisi" : allEmission
    }
    # endregion
    return render_template("page/dashboard.html", data = data)
# endregion

# region kelola users
# View users
def users_page(user_id, method_url, title=""):
    methods = request.form.get("_method")
    userId = user_id
    # methods
    if methods is None and userId is None:
        return users_get(url = method_url, title=title)
    if methods == "POST" and userId is None:
        return users_add(url = method_url)
    if methods == "PUT" and userId is not None:
        return users_edit(userId, url = method_url)
    if methods == "DELETE" and userId is not None:
        return users_delete(userId, url = method_url)
# region users add
def users_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
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
def users_get(url = "", title=""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # endregion
    # region data users
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region users edit
def users_edit(users_id = None, url = ""):
    # region fetch api
    user_id = users_id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{user_id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        if payloads['password'] and session.get('username') == payloads['username']:
            session.clear()
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region users delete 
def users_delete(users_id = None, url = ""):
    # region fetch api
    user_id = users_id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{user_id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        if session.get('user_id') == user_id:
            session.clear()
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion 

# region kelola activities
# View activities
def activities_page(id, method_url, title=""):
    Id = id
    methods = request.form.get("_method")
    # methods
    if methods is None and Id is None:
        return activities_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return activities_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return activities_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return activities_delete(Id, url = method_url)
# region activities get
def activities_get(url = "", title = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # data users
    response_users = requests.get(url=f"{url_api}/users", headers=headers)
    userData = response_users.json()
    # data carbon factors
    response_factors = requests.get(url=f"{url_api}/carbon_factors", headers=headers)
    factorData = response_factors.json() 
    # endregion
    # region data users
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata,
        "carbon_factors" : factorData,
        "users" : userData
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region activity add
def activities_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region activities edit
def activities_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region activities delete
def activities_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    print(response.json())
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion

# region kelola sources
# View sources
def sources_page(id, method_url, title=""):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return sources_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return sources_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return sources_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return sources_delete(Id, url = method_url)
# region sources get
def sources_get(url = "", title=""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # endregion
    # region data users
     
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region sources add
def sources_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region sources edit
def sources_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region sources delete
def sources_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion

# region kelola emissions
# View emissions
def emissions_page(id, method_url, title = ""):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return emissions_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return emissions_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return emissions_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return emissions_delete(Id, url = method_url)
# region emissions get
def emissions_get(url = "", title = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # sources data
    response_source = requests.get(url=f"{url_api}/sources", headers=headers)
    sourceData = response_source.json() 
    # users data
    response_users = requests.get(url=f"{url_api}/users", headers=headers)
    userData = response_users.json() 
    # endregion
    # region data users
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata,
        "sources" : sourceData,
        "users" : userData
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region emissions add
def emissions_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region emissions edit
def emissions_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region emissions delete
def emissions_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion

# region kelola carbon factors
# View emissions
def carbon_factors_page(id, method_url, title=""):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return carbon_factors_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return carbon_factors_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return carbon_factors_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return carbon_factors_delete(Id, url = method_url)
# region emissions get
def carbon_factors_get(url = "", title =""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    response_source = requests.get(url=f"{url_api}/sources", headers=headers)
    sourceData = response_source.json()
    # endregion
    # region data users
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata,
        "sources" : sourceData
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region emissions add
def carbon_factors_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region emissions edit
def carbon_factors_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region emissions delete
def carbon_factors_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion

# region kelola goals
# View goals
def goals_page(id, method_url, title=""):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return goals_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return goals_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return goals_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return goals_delete(Id, url = method_url)
# region goals get
def goals_get(url = "", title =""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # data user
    response_users = requests.get(url=f"{url_api}/users", headers=headers)
    userData = response_users.json() 
    # endregion
    # region data users
     
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata,
        "users" : userData
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region goals add
def goals_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region goals edit
def goals_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region goals delete
def goals_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion

# region kelola offsets
# View offsets
def offsets_page(id, method_url, title=""):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return offsets_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return offsets_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return offsets_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return offsets_delete(Id, url = method_url)
# region offsets get
def offsets_get(url = "", title =""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # data user
    response_users = requests.get(url=f"{url_api}/users", headers=headers)
    userData = response_users.json() 
    # endregion
    # region data users
     
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata,
        "users" : userData
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region offsets add
def offsets_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region offsets edit
def offsets_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region offsets delete
def offsets_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion

# region kelola offsets
# View offsets
def reports_page(id, method_url, title=""):
    methods = request.form.get("_method")
    Id = id
    # methods
    if methods is None and Id is None:
        return reports_get(url = method_url, title=title)
    if methods == "POST" and Id is None:
        return reports_add(url = method_url)
    if methods == "PUT" and Id is not None:
        return reports_edit(Id, url = method_url)
    if methods == "DELETE" and Id is not None:
        return reports_delete(Id, url = method_url)
# region offsets get
def reports_get(url = "", title =""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.get(url=f"{url_api}/{method}", headers=headers)
    alldata = response.json()
    # data user
    response_users = requests.get(url=f"{url_api}/users", headers=headers)
    userData = response_users.json() 
    # endregion
    # region data users
     
    # data
    account = decode_token(session.get('access_token_cookie'))
    data = {
        "user_id" : account['sub'],
        "title" : title,
        "username" : session.get('username'),
        "role" : session.get('role'),
        "menu" : json.loads(menuBar(method=method)),
        "datas" : alldata,
        "users" : userData
    }
    return render_template(f"page/{method}.html", data=data)
    # endregion
# endregion
# region offsets add
def reports_add(url = ""):
    # region fetch api
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.post(url=f"{url_api}/{method}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 201:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region offsets edit
def reports_edit(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    payloads = json.loads(payload(method_url=method))
    response = requests.put(url=f"{url_api}/{method}/{Id}", headers=headers, json=payloads)
    res_data = response.json()
    # Response Data
    if response.status_code == 200:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# region offsets delete
def reports_delete(id = None, url = ""):
    # region fetch api
    Id = id
    method = url
    headers = {
                'Content-Type': 'application/json',
                'Authorization' : f"Bearer {session.get('access_token_cookie')}"
            }
    response = requests.delete(url=f"{url_api}/{method}/{Id}", headers=headers)
    res_data = response.json()
    
    # Response Data
    if response.status_code == 202:
        flash(res_data['message'], "success")
    else : 
        flash(res_data['message'], "danger")
        
    return redirect(url_for(f"router-web.{method}"))
    # endregion
# endregion
# endregion