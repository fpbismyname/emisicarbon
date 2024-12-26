from app.database.models import *

class Activities(db.Model):
    __tablename__ = 'activities'

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    factor_id = db.Column(db.Integer, db.ForeignKey('carbon_factors.factor_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    report_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    user = db.relationship('Users', backref='activities', cascade='all, delete-orphan', single_parent = True)
    carbon_factor = db.relationship('CarbonFactors', backref='activities', cascade='all, delete-orphan', single_parent = True)

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'factor_id': self.factor_id,
            'amount': self.amount,
            'activity_date': self.activity_date.isoformat(),
            'report_date': self.report_date.isoformat(),
        }