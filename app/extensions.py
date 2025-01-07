import flask_jwt_extended as flask_jwt
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate, upgrade, migrate
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from enum import Enum
from datetime import datetime
from flask_cors import CORS


db = SQLAlchemy()
migrate_app = Migrate() 
bcrypt = Bcrypt()
corsOrigin = CORS()