import requests as req
from flask import Blueprint, render_template
controller = Blueprint("controller-web", __name__)


# URL API
url = "http://127.0.0.1:5000/emisi-carbon/api/v1"
# Create Method for controll the routes

# Homepage
def index_home():
    return render_template("index.html")

# Halaman Emisi
def account_list():
    # Variable data untuk di kirim ke front end
    data = None
    # Melakukan proses fetching data dari API
    try:
        response = req.get(url= url+"/account")
        data = response.json()
    except ZeroDivisionError as e:
        data['error'] = e
    # Merender halaman beserta dilampirkan dengan data dari API
    return render_template("account-list.html", datas = data)

# Emisi Page
def emisi_page():
    data = None
    try:
        response = req.get(url=url+"/emisi")
        data = response.json()
    except ZeroDivisionError as e:
        data['error'] = e
    return render_template("emisi-page.html", datas = data)