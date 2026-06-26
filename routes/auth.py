from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models import db, bcrypt
from models.user import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already registered.","danger")
            return redirect(url_for("auth.register"))

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            name=name,
            email=email,
            password=hashed
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful.","success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password,password):

            login_user(user)

            return redirect(url_for("dashboard.dashboard"))

        flash("Invalid Email or Password","danger")

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged Out Successfully","success")

    return redirect(url_for("home"))