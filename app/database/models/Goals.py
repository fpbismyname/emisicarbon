from app.database.models import *

class Goals(db.Model):
    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    target_emission = db.Column(db.Numeric(10, 2), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('in_progress', 'achieved', 'missed', name='goal_status'), default='in_progress')
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'goal_id': self.goal_id,
            'user_id': self.user_id,
            'target_emission': self.target_emission,
            'deadline': self.deadline.strftime('%Y-%m-%d'),
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }