from app import db
from app.database.models.Users import Users
def seed():
    if not Users.query.first():
        user1 = Users(email='admin@gmail.com', username='Admin Account', role='admin')
        user1.set_password(password='AdMin123')
        db.session.add(user1)
        db.session.commit()