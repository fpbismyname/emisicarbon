from app.database.models import *

class Reports(db.Model):
    __tablename__ = 'reports'

    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_emission = db.Column(db.Numeric(12, 2), nullable=False)
    report_generated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    user = db.relationship('Users', backref='reports', cascade='all, delete-orphan', single_parent = True)

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'user_id': self.user_id,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'total_emission': str(self.total_emission),
            'report_generated_at': self.report_generated_at.isoformat(),
        }