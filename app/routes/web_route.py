from app.extensions import *
from app.controllers import web_controller
from app.middleware.middleware import access_token, adminOnly
web = Blueprint("router-web", __name__)
    
# Create web routes here

# region Login
@web.route("/login", methods=['GET', 'POST'])
def login():
    return web_controller.login_page()
# endregion

# region Register
@web.route("/register", methods=['GET', 'POST'])
def register():
    return web_controller.register_page()
# endregion

# region Logout
@web.route("/logout", methods=['POST'])
def logout(): 
    return web_controller.logout_page()
# endregion

# region Dashboard
@web.route("/", methods=['GET'])
@access_token
def dashboard():
    return web_controller.dashboard_page()
# endregion

# region Kelola user
@web.route("/users", defaults={ "id" : None }, methods=['GET'])
@web.route("/users/<int:id>", methods=['POST'])
@access_token
@adminOnly
def users(id):
    return web_controller.users_page(user_id=id)


# endregion
