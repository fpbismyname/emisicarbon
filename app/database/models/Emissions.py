from app.database.models import *

class Emissions(db.Model):
    __tablename__ = 'emissions'

    emission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.activity_id', ondelete='CASCADE'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.source_id', ondelete='SET NULL'), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    emission_date = db.Column(db.Date, nullable=False)
    report_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'emission_id': self.emission_id,
            'user_id': self.user_id,
            'activity_id': self.activity_id,
            'source_id': self.source_id,
            'amount': self.amount,
            'emission_date': self.emission_date.strftime('%Y-%m-%d'),
            'report_date': self.report_date.strftime('%Y-%m-%d')
        }