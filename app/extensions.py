import flask_jwt_extended as flask_jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, upgrade, migrate
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from enum import Enum
from datetime import datetime


db = SQLAlchemy()
migrate_app = Migrate() 
bcrypt = Bcrypt()