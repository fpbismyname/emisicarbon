from app.extensions import *
from app import jwt
from app.database.models.Users import Users

# Custom token expired redirect
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for("router-web.login"))

def access_token(f):
    @wraps(f)
    def func(*args, **kwargs):
        token = session.get('access_token_cookie')
        if not token:
            return redirect(url_for("router-web.login"))
        users = decode_token(token)
        checkUser = Users.query.filter_by(username=users['username']).first()
        if not checkUser:
            return redirect(url_for("router-web.login"))
        return f(*args, **kwargs)
    return func

def adminOnly(f):
    @wraps(f)
    def func(*args, **kwargs):
        token = session.get('access_token_cookie')
        if not token:
            return redirect(url_for("router-web.login"))
        users = decode_token(token)
        if users['role'] != "admin" : 
            return redirect(request.referrer)
        checkUser = Users.query.filter_by(username=users['username']).first()
        if not checkUser:
            return redirect(url_for("router-web.login"))
        return f(*args, **kwargs)
    return func