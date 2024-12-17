from app.extensions import db
def MigrationModel():
    class Account(db.Model):
        __tablename__ = "Account"
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), nullable=False, unique=True)
        email = db.Column(db.String(50), nullable=False, unique=True)
        
        def __repr__(self):
            return f"<Account {self.username}>"
        
    class Emisi(db.Model):
        __tablename__ = "Emisi"
        id = db.Column(db.Integer, primary_key=True)
        emisi_name = db.Column(db.String(80), nullable=False, unique=True)
        emisi_desc = db.Column(db.String(50), nullable=False, unique=True)
        
        def __repr__(self):
            return f"<Emisi {self.emisi_name}>"
        
    class CategoryEmisi(db.Model):
        __tablename__ = "CategoryEmisi"
        id = db.Column(db.Integer, primary_key = True)
        category_name = db.Column(db.String(50), nullable = False, unique = False)
        category_type = db.Column(db.String(50), nullable = False, unique = False)
        
        def __repr__(self):
            return f"<CategoryEmisi {self.category_name}>"
        
    class TotalEmisi(db.Model):
        __tablename__ = "Total"
        id = db.Column(db.Integer, primary_key = True)
        total_name = db.Column(db.String(50), nullable = False, unique = False)
        total_emisi = db.Column(db.Integer, nullable = False, unique = False)
        
        def __repr__(self):
            return f"<CategoryEmisi {self.category_name}>"
        
    class Wilayah(db.Model):
        __tablename__ = "Wilayah"
        id = db.Column(db.Integer, primary_key = True)
        wilayah_name = db.Column(db.String(50), nullable = False, unique = False)
        wilayah_emisi = db.Column(db.Integer, nullable = False, unique = False)
        
        def __repr__(self):
            return f"<Wilayah {self.wilayah_name}>"