from flask_login import UserMixin
from models import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    # ==========================
    # Primary Key
    # ==========================
    id = db.Column(db.Integer, primary_key=True)

    # ==========================
    # Authentication
    # ==========================
    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    # ==========================
    # Personal Information
    # ==========================
    age = db.Column(db.Integer)

    gender = db.Column(db.String(20))

    height = db.Column(db.Float)

    weight = db.Column(db.Float)

    # ==========================
    # Fitness Profile
    # ==========================
    goal = db.Column(db.String(50))

    activity = db.Column(db.String(50))

    diet = db.Column(db.String(50))

    budget = db.Column(db.Integer)

    workout_days = db.Column(db.Integer)

    # ==========================
    # Relationship
    # ==========================
    plans = db.relationship(
        "Plan",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    progress = db.relationship(
    "Progress",
    backref="user",
    lazy=True,
    cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.name}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))