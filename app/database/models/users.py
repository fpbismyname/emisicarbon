from app import bcrypt, db, Enum, datetime

class Role(Enum):
    ADMIN = 'admin'
    COMPANY = 'company'
    USER = 'user'

class users(db.Model):
    __tablename__ = "Account"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=False)
    role = db.Column(db.Enum(Role), default=Role.USER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
        
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password,
            'role' : self.role,
            'created_at' : self.created_at
        }