from app.extensions import *
from app.database.models.Users import Users

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