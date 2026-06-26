from datetime import datetime
from models import db


class Plan(db.Model):
    __tablename__ = "plans"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    workout = db.Column(db.Text, nullable=False)

    diet = db.Column(db.Text, nullable=False)

    water = db.Column(db.String(100))

    motivation = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )