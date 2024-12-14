from flask import Blueprint, render_template
controller = Blueprint("controller-web", __name__)

# Create Method for controll the routes
def index_home():
    return render_template("index.html")