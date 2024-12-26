import os
from datetime import timedelta

Environment = "development"

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(12).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    # Debug Option
    DEBUG = True
    # JWT Token
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.urandom(12).hex()
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
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
    DEBUG = False
    # JWT Token
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.urandom(12).hex
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)
    # Database Mysql
    MYSQL_DATABASE = 'emisi-carbon'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_PORT = '3400'