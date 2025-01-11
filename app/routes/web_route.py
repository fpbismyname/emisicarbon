from app.extensions import *
from app.controllers import web_controller
from app.middleware.middleware import *
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
@access_token(['admin','company', 'users'])
def dashboard():
    return web_controller.dashboard_page(method_url="dashboard", title="Dashboard")
# endregion

# region Kelola user
@web.route("/users", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/users/<int:id>", methods=['POST'])
@access_token('admin')
def users(id):
    return web_controller.users_page(user_id=id, method_url = "users", title="Kelola user")
# endregion

# region Kelola activities
@web.route("/activities", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/activities/<int:id>", methods=['POST'])
@access_token(['admin', 'company', 'user'])
def activities(id):
    return web_controller.activities_page(id=id, method_url="activities", title="Kelola aktivitas")
# endregion

# region Kelola sources
@web.route("/sources", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/sources/<int:id>", methods=['POST'])
@access_token('admin')
def sources(id):
    return web_controller.sources_page(id=id, method_url = "sources", title="Kelola sumber emisi")
# endregion

# region Kelola emissions
@web.route("/emissions", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/emissions/<int:id>", methods=['POST'])
@access_token('admin')
def emissions(id):
    return web_controller.emissions_page(id=id, method_url = "emissions", title="Kelola emisi")
# endregion

# region Kelola carbon factors
@web.route("/carbon_factors", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/carbon_factors/<int:id>", methods=['POST'])
@access_token('admin')
def carbon_factors(id):
    return web_controller.carbon_factors_page(id=id, method_url = "carbon_factors", title="Kelola faktor karbon")
# endregion

# region Kelola goals
@web.route("/goals", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/goals/<int:id>", methods=['POST'])
@access_token('admin')
def goals(id):
    return web_controller.goals_page(id=id, method_url = "goals", title="Kelola target emisi")
# endregion

# region Kelola offsets
@web.route("/offsets", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/offsets/<int:id>", methods=['POST'])
@access_token('admin')
def offsets(id):
    return web_controller.offsets_page(id=id, method_url = "offsets", title="Kelola offset")
# endregion

# region Kelola reports
@web.route("/reports", defaults={ "id" : None }, methods=['GET', 'POST'])
@web.route("/reports/<int:id>", methods=['POST'])
@access_token('admin')
def reports(id):
    return web_controller.reports_page(id=id, method_url = "reports", title="Kelola laporan emisi")
# endregion