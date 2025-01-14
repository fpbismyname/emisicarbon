import importlib
import json
import click
import os
import requests
from decimal import Decimal
import flask_jwt_extended as flask_jwt
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token, set_access_cookies, JWTManager, exceptions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy import text, func, Table, MetaData
from sqlalchemy.exc import IntegrityError
from functools import wraps
from enum import Enum
from datetime import datetime, timedelta


db = SQLAlchemy()
migrate_app = Migrate() 
bcrypt = Bcrypt()
corsOrigin = CORS()
jwt = JWTManager()

def generate_password(password):
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    return password