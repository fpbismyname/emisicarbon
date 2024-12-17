from flask import Flask
from .extensions import *
from app.routes.api import router as api
from app.routes.web import router as web
from config import DevConfig
import click
import os

def create_app(config = DevConfig):
    app = Flask(__name__, template_folder="views")
    app.register_blueprint(api)
    app.register_blueprint(web)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DATABASE}"
    
    db.init_app(app)
    migrate_app.init_app(app, db)
    
    from app.models.model import MigrationModel
    MigrationModel()
    
    @app.cli.command("db-refresh")
    def db__refresh():
        # Remove Versions
        path = "migrations\\versions\\*.*"
        os.system(f"del /f /q {path}")
        # Drop All Table
        click.echo(" > Dropped All Database's...")
        db.drop_all()
        with db.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
            connection.commit()
        # Recreate Table
        click.echo(" > Recreating All Database's...")
        migrate()
        upgrade()
        click.echo(" > Recreate All Database's Succeeded...")
    return app