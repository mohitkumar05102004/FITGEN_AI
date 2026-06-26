from datetime import datetime
from models import db


class Progress(db.Model):

    __tablename__ = "progress"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    weight = db.Column(db.Float, nullable=False)

    chest = db.Column(db.Float)

    waist = db.Column(db.Float)

    arms = db.Column(db.Float)

    bmi = db.Column(db.Float)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )