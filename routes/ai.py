import json

from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

from models import db
from models.plan import Plan
from services.openrouter_service import generate_fitness_plan

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/generate-plan")
@login_required
def generate_plan():

    try:

        plan = generate_fitness_plan(current_user)

        # Delete old plan
        Plan.query.filter_by(user_id=current_user.id).delete()

        new_plan = Plan(
            user_id=current_user.id,
            workout=json.dumps(plan["workout"]),
            diet=json.dumps(plan["diet"]),
            water=plan["water"],
            motivation=plan["motivation"]
        )

        db.session.add(new_plan)
        db.session.commit()

        flash("AI Plan Generated Successfully!", "success")

    except Exception as e:
        print(e)
        flash(str(e), "danger")

    return redirect(url_for("dashboard.dashboard"))