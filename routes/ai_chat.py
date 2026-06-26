from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from services.chat_service import ask_fitness_ai

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat")
@login_required
def chat():

    return render_template("ai_chat.html")


@chat_bp.route("/chat-api", methods=["POST"])
@login_required
def chat_api():

    data = request.get_json()

    message = data.get("message", "")

    if not message:

        return jsonify({
            "reply": "Please enter a question."
        })

    reply = ask_fitness_ai(message)

    return jsonify({
        "reply": reply
    })