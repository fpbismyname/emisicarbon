from app.extensions import *
from app.controllers import web_controller
from app.middleware.access_token import access_token
web = Blueprint("router-web", __name__)
    
# Create web routes here

# Login
@web.route("/login", methods=['GET', 'POST'])
def login():
    return web_controller.login_page()

# Register
@web.route("/register", methods=['GET', 'POST'])
def register():
    return web_controller.register_page()

# Logout
@web.route("/logout", methods=['POST'])
def logout():
    return web_controller.logout_page()

# Dashboard
@web.route("/", methods=['GET'])
@access_token
def dashboard():
    return web_controller.dashboard_page()