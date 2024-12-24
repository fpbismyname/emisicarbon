from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, migrate
from sqlalchemy import text
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate_app = Migrate() 
bcrypt = Bcrypt()