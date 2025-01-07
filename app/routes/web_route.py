from app.extensions import *
from app.controllers import web_controller
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

# Dashboard
@web.route("/", methods=['GET'])
def dashboard():
    return web_controller.dashboard_page()