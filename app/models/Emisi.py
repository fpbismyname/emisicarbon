from app import db
class Emisi(db.Model):
    __tablename__ = "Emisi"
    id = db.Column(db.Integer, primary_key=True)
    emisi_name = db.Column(db.String(128), nullable=False, unique=True)
    emisi_desc = db.Column(db.String(128), nullable=False, unique=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'emisi_name': self.emisi_name,
            'emisi_desc': self.emisi_desc
        }