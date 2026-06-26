from flask import Blueprint, send_file
from flask_login import login_required, current_user

import json

from models.plan import Plan
from models.progress import Progress

from services.fitness import *

from services.pdf_service import create_pdf

report_bp = Blueprint("report", __name__)


@report_bp.route("/report")
@login_required
def report():

    latest = Progress.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Progress.created_at.desc()
    ).first()

    weight = current_user.weight

    if latest:
        weight = latest.weight

    plan = Plan.query.filter_by(
        user_id=current_user.id
    ).first()

    workout = json.loads(plan.workout)

    diet = json.loads(plan.diet)

    analytics = {

        "weight": weight,

        "bmi": calculate_bmi(current_user.height, weight),

        "calories": calories(weight, current_user.goal),

        "protein": protein(weight),

        "water": water(weight)

    }

    create_pdf(

        "fitness_report.pdf",

        current_user,

        {

            "workout": workout,

            "diet": diet

        },

        analytics

    )

    return send_file(

        "fitness_report.pdf",

        as_attachment=True

    )