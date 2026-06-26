from flask import Flask, render_template
from config import Config
from models import db, login_manager, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from routes.auth import auth
    from routes.dashboard import dashboard_bp
    from routes.progress import progress_bp
    from routes.profile import profile_bp
    from routes.ai import ai_bp
    from routes.report import report_bp
    from routes.ai_chat import chat_bp

    app.register_blueprint(auth)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(chat_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
