import requests
from app.extensions import *
controller = Blueprint("controller-web", __name__)


# URL API
url = "http://127.0.0.1:5000/emisi-carbon/api/v1"
    
# Create Method for controll the routes
# LoginPage
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

# RegisterPage
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
    
# Logout
def logout_page():
    session.clear()
    return redirect(url_for('router-web.login'))

# DashboardPage
def dashboard_page():
    account = {
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
        }
    }
    return render_template("page/dashboard.html",account=account)