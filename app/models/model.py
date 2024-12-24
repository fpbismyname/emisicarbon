from app import bcrypt, db
class Account(db.Model):
    __tablename__ = "Account"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False, unique=False)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)
        
    def check_password(hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }