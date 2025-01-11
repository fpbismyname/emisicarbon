from app.database.models import *

class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=False)
    role = db.Column(db.Enum('admin', 'company', 'user'), default="user")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password: str) -> str:
        self.password_hash = bcrypt.generate_password_hash(password)
        
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'role' : self.role,
            'created_at' : self.created_at.strftime('%Y-%m-%d')
        }