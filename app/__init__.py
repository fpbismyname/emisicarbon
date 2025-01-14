from .extensions import *
from app.database.seeders.seeder import seed
from flask import Flask
from app.routes.api_route import api
from app.routes.web_route import web
from config import Environment, DevelopmentConfig, ProductionConfig
from app.database import models

def create_app(config = Environment):
    app = Flask(__name__, template_folder="views")
    app.register_blueprint(api)
    app.register_blueprint(web)
    
    app.config.from_object(DevelopmentConfig if Environment == "development" else ProductionConfig)

    db.init_app(app=app)
    migrate_app.init_app(app=app, db=db)
    bcrypt.init_app(app=app)
    
    jwt.init_app(app=app)
    
    corsOrigin.init_app(app=app)
    
    @app.cli.command("db-refresh")
    def db_refresh():
        # Remove Versions
        path = "migrations\\versions\\*.*"
        os.system(f"del /f /q {path}")
        # Drop All Table
        click.echo(" > Dropped All Database's...")
        db.drop_all()
        with db.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS alembic_version"))
            connection.commit()
        click.echo(" > Recreating All Database's...")
        migrate()
        upgrade()
        click.echo(" > Recreate All Database's Succeeded...")
        seed()
        click.echo(" > Seed all data Succeeded...")
        
    return app