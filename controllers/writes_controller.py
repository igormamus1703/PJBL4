from flask import Blueprint, request, render_template
from models.iot.write import Write
from models.iot.actuators import Actuator
import flask_login
from models.user.decorators import role_required

write = Blueprint("write", __name__, template_folder="views")

@write.route('/add_write', methods=['POST'])
@flask_login.login_required
def add_write():
    topic = request.form.get("topic")
    value = request.form.get("value")
    Write.save_write(topic, value)
    return "Write saved successfully"

@write.route("/history_write")
@flask_login.login_required
@role_required(1, 2)  # Admin/Moderador
def history_write():
    actuators = Actuator.get_actuators()
    write = {}
    return render_template("history_write.html", actuators=actuators, write=write)

@write.route("/get_write", methods=['POST'])
@flask_login.login_required
def get_write():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        write = Write.get_write(id, start, end)
        actuators = Actuator.get_actuators()
        return render_template("history_write.html", actuators=actuators, write=write)
