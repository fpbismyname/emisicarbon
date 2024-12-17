from flask import Flask
from .extensions import *
from app.routes.api import router as api
from app.routes.web import router as web
from config import DevConfig

def create_app(config = DevConfig):
    app = Flask(__name__, template_folder="views")
    app.register_blueprint(api)
    app.register_blueprint(web)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}"
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models import Account
    return app