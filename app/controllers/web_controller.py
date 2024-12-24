import requests as req
from flask import Blueprint, render_template
controller = Blueprint("controller-web", __name__)


# URL API
url = "http://127.0.0.1:5000/emisi-carbon/api/v1"
    
# Create Method for controll the routes
# Homepage
def index_home():
    return render_template("index.html")

# LoginPage
def loginPage():
    return render_template("login.html")