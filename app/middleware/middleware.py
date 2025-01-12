from app.extensions import *
from app import jwt as Jwt
from app.database.models.Users import Users

# Custom token expired redirect
@Jwt.invalid_token_loader
def invalid_token_callback(reason):
    return redirect(url_for("router-web.login"))

@Jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for("router-web.login"))

# Checking access token
def access_token(roles=[]):
        def wrapper(func):
            @wraps(func)
            def decorated_function(*args, **kwargs):
                try:
                    # Checking avalable token
                    token = session.get('access_token_cookie')
                    if not token:
                        return redirect(url_for("router-web.login"))
                    # Reading the current token
                    read_token = decode_token(token)
                    # Validating token that account is available
                    checkUser = Users.query.filter_by(username=read_token['username']).first()
                    if not checkUser:
                        return redirect(url_for("router-web.login"))
                    # Validating role based
                    if roles:
                        allowed_role = roles
                        if read_token['role'] not in allowed_role:
                            return redirect(request.referrer)
                    # Continue the process
                except ZeroDivisionError:
                    return redirect(url_for("router-web.login"))
                return func(*args, **kwargs)
            return decorated_function
        return wrapper