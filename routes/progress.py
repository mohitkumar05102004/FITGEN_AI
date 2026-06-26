from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user

from models import db
from models.progress import Progress

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/progress", methods=["GET", "POST"])
@login_required
def progress():

    # ----------------------------
    # Save Progress
    # ----------------------------
    if request.method == "POST":

        weight = float(request.form["weight"])
        chest = float(request.form["chest"])
        waist = float(request.form["waist"])
        arms = float(request.form["arms"])

        bmi = round(
            weight / ((current_user.height / 100) ** 2),
            1
        )

        new_progress = Progress(
            user_id=current_user.id,
            weight=weight,
            chest=chest,
            waist=waist,
            arms=arms,
            bmi=bmi
        )

        db.session.add(new_progress)
        db.session.commit()

        flash("Progress Saved Successfully!", "success")

        return redirect("/progress")

    # ----------------------------
    # Get Progress History
    # ----------------------------
    progress_list = Progress.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Progress.created_at.desc()
    ).all()

    # ----------------------------
    # Summary Statistics
    # ----------------------------

    current_weight = current_user.weight
    starting_weight = current_user.weight
    current_bmi = 0
    weight_change = 0

    if progress_list:

        latest = progress_list[0]
        oldest = progress_list[-1]

        current_weight = latest.weight
        starting_weight = oldest.weight

        current_bmi = latest.bmi

        weight_change = round(
            current_weight - starting_weight,
            1
        )

    return render_template(
        "progress.html",

        progress_list=progress_list,

        current_weight=current_weight,

        starting_weight=starting_weight,

        weight_change=weight_change,

        current_bmi=current_bmi
    )


# ------------------------------------
# Delete Progress Entry
# ------------------------------------

@progress_bp.route("/delete-progress/<int:id>")
@login_required
def delete_progress(id):

    progress = Progress.query.get_or_404(id)

    if progress.user_id != current_user.id:

        flash("Unauthorized!", "danger")

        return redirect("/progress")

    db.session.delete(progress)

    db.session.commit()

    flash("Progress Deleted!", "success")

    return redirect("/progress")