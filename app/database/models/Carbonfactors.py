from app.database.models import *

class CarbonFactors(db.Model):
    __tablename__ = 'carbon_factors'

    factor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.source_id', ondelete='SET NULL'), nullable=True)
    description = db.Column(db.Text)
    conversion_factor = db.Column(db.Numeric(10, 4), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    activities = db.relationship('Activities', backref="factor_activity", lazy='joined')

    def to_dict(self):
        return {
            'factor_id': self.factor_id,
            'source_id': self.source_id,
            'description': self.description,
            'conversion_factor': str(self.conversion_factor),
            'unit': self.unit,
        }