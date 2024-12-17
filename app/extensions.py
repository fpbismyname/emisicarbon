from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, migrate
from sqlalchemy import text

db = SQLAlchemy()
migrate_app = Migrate() 