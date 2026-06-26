from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        current_user.age = int(request.form["age"])
        current_user.gender = request.form["gender"]
        current_user.height = float(request.form["height"])
        current_user.weight = float(request.form["weight"])

        current_user.goal = request.form["goal"]
        current_user.activity = request.form["activity"]
        current_user.diet = request.form["diet"]

        current_user.budget = int(request.form["budget"])
        current_user.workout_days = int(request.form["workout_days"])

        db.session.commit()

        flash("Profile Updated Successfully!", "success")

        return redirect(url_for("dashboard.dashboard"))

    return render_template("profile.html", user=current_user)