import requests
from app.extensions import *
controller = Blueprint("controller-web", __name__)


# URL API
url = "http://127.0.0.1:5000/emisi-carbon/api/v1"
    
# Create Method for controll the routes
# Homepage
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
                user_id = decode_token(res_data['bearer_token'])
                resp = make_response(redirect(url_for('router-web.dashboard')))
                resp.set_cookie('access_token_cookie', str(res_data['bearer_token']))
                resp.set_cookie('role', str(res_data['role']))
                resp.set_cookie('id_user', str(user_id['sub']))
                return resp
            elif response.status_code == 400:
                flash(res_data['message'], "danger")
                return redirect(url_for('router-web.login'))
            elif response.status_code == 404:
                flash(res_data['message'], "danger")
                return redirect(url_for('router-web.login'))
        except ZeroDivisionError:
            return {"error" : "Error"}
    return render_template("auth/login.html")

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
            if response.status_code == 200:
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


def dashboard_page():
    return render_template("page/dashboard.html")