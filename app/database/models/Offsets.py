from app.database.models import *

class Offsets(db.Model):
    __tablename__ = 'offsets'

    offset_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    offset_amount = db.Column(db.Numeric(10, 2), nullable=False)
    offset_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    user = db.relationship('Users', backref='offsets', cascade='all, delete-orphan', single_parent = True)

    def to_dict(self):
        return {
            'offset_id': self.offset_id,
            'user_id': self.user_id,
            'project_name': self.project_name,
            'offset_amount': str(self.offset_amount),
            'offset_date': self.offset_date.isoformat(),
            'created_at': self.created_at.isoformat(),
        }