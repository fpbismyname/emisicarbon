from app.database.models import *

class Activities(db.Model): 
    __tablename__ = 'activities' 

    activity_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    factor_id = db.Column(db.Integer, db.ForeignKey('carbon_factors.factor_id', ondelete='SET NULL'), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    report_date = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())


    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'factor_id': self.factor_id,
            'amount': self.amount,
            'activity_date': self.activity_date.strftime('%Y-%m-%d'),
            'report_date': self.report_date.strftime('%Y-%m-%d')
        }