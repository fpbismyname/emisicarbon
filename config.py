import os
from datetime import timedelta

# Environment : development / production
Environment = "development" 

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or "Emisi-Carbon-01"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    # Debug Option
    DEBUG = True
    # JWT Token
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or Config.SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    # Session Config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    # Database Mysql
    DATABASE_ENGINE = "mysql"
    DATABASE_NAME = 'emisi-carbon'
    HOST_NAME = 'localhost'
    USERNAME_DATABASE = 'root'
    PASSWORD_DATABASE = ''
    PORT_DATABASE = '3400'
    # Database URI
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_ENGINE}+pymysql://{USERNAME_DATABASE}:{PASSWORD_DATABASE}@{HOST_NAME}:{PORT_DATABASE}/{DATABASE_NAME}"
    
class ProductionConfig(Config):
    # Debug Option
    DEBUG = False
    # JWT Token
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.urandom(32).hex()
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    # Session Config
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    # Database Mysql
    DATABASE_ENGINE = "mysql"
    DATABASE_NAME = 'emisi-carbon'
    HOST_NAME = 'localhost'
    USERNAME_DATABASE = 'root'
    PASSWORD_DATABASE = ''
    PORT_DATABASE = '3400'
    # Database URI
    SQLALCHEMY_DATABASE_URI = f"{DATABASE_ENGINE}+pymysql://{USERNAME_DATABASE}:{PASSWORD_DATABASE}@{HOST_NAME}:{PORT_DATABASE}/{DATABASE_NAME}"