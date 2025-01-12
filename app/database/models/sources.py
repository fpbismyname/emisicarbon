from app.database.models import *

class Sources(db.Model):
    __tablename__= "sources"
    source_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    source_name = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    emissions = db.relationship('Emissions', backref='source_emission', lazy='joined')
    carbon_factors = db.relationship('CarbonFactors', backref='source_factor', lazy='joined')
    
    def to_dict(self):
        return {
            'source_id': self.source_id,
            'source_name': self.source_name,
            'description': self.description,
            'created_at' : self.created_at.strftime('%Y-%m-%d')
        }
