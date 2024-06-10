from flask import Blueprint, render_template, request
import flask_login
from models.user.decorators import role_required

publish = Blueprint("publish", __name__, template_folder="views")

@publish.route('/publish')
@flask_login.login_required
@role_required(1, 2)  # Admin/Moderador
def publish_view():
    return render_template("publish.html")
