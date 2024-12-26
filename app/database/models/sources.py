from app.database.models import *

class sources(db.Model):
    __tablename__= "sources"
    source_id = db.Column(db.Integer, primary_key = True)
    source_name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'source_id': self.source_id,
            'source_name': self.source_name,
            'description': self.description,
            'created_at' : self.created_at,
        }
