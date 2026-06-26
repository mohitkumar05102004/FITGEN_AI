import json
from datetime import datetime

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.progress import Progress

from models.plan import Plan
from services.fitness import (
    calculate_bmi,
    bmi_status,
    calories,
    protein,
    water
)

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    # -----------------------------
    # Get Latest AI Plan
    # -----------------------------
    plan = Plan.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Plan.id.desc()
    ).first()

    workout = {}
    diet = {}

    if plan:
        workout = json.loads(plan.workout)
        diet = json.loads(plan.diet)

    # -----------------------------
    # Latest Progress
    # -----------------------------

    latest_progress = Progress.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Progress.created_at.desc()
    ).first()

    current_weight = current_user.weight

    if latest_progress:
        current_weight = latest_progress.weight

    # -----------------------------
    # Fitness Analytics
    # -----------------------------

    bmi = calculate_bmi(
        current_user.height,
        current_weight
    )

    bmi_result = bmi_status(bmi)

    daily_calories = calories(
        current_weight,
        current_user.goal
    )

    daily_protein = protein(
        current_weight
    )

    daily_water = water(
        current_weight
    )

    # -----------------------------
    # Today's Workout
    # -----------------------------
    today = datetime.now().strftime("%A")

    today_workout = workout.get(today, [])

    total_exercises = len(today_workout)

    completed = 0

    progress = 0

    if total_exercises > 0:
        progress = int(
            (completed / total_exercises) * 100
        )

    return render_template(

        "dashboard.html",

        user=current_user,

        plan=plan,

        workout=workout,

        diet=diet,

        bmi=bmi,

        bmi_result=bmi_result,

        daily_calories=daily_calories,

        daily_protein=daily_protein,

        daily_water=daily_water,

        current_weight=current_weight,

        today=today,

        today_workout=today_workout,

        progress=progress,

        completed=completed,

        total_exercises=total_exercises
    )