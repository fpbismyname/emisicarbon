from app.extensions import db
class Account(db.Model):
    __tablename__ = "Account"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
class Emisi(db.Model):
    __tablename__ = "Emisi"
    id = db.Column(db.Integer, primary_key=True)
    emisi_name = db.Column(db.String(80), nullable=False, unique=True)
    emisi_desc = db.Column(db.String(50), nullable=False, unique=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'emisi_name': self.emisi_name,
            'emisi_desc': self.emisi_desc
        }
    
class CategoryEmisi(db.Model):
    __tablename__ = "CategoryEmisi"
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(50), nullable = False, unique = False)
    category_type = db.Column(db.String(50), nullable = False, unique = False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
            'category_type': self.category_type
        }
    
class TotalEmisi(db.Model):
    __tablename__ = "Total"
    id = db.Column(db.Integer, primary_key = True)
    total_name = db.Column(db.String(50), nullable = False, unique = False)
    total_emisi = db.Column(db.Integer, nullable = False, unique = False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'total_name': self.total_name,
            'total_emisi': self.total_emisi
        }
    
class Wilayah(db.Model):
        __tablename__ = "Wilayah"
        id = db.Column(db.Integer, primary_key = True)
        wilayah_name = db.Column(db.String(50), nullable = False, unique = False)
        wilayah_emisi = db.Column(db.Integer, nullable = False, unique = False)
        
        def to_dict(self):
            return {
                'id': self.id,
                'wilayah_name': self.wilayah_name,
                'wilayah_emisi': self.wilayah_emisi
            }