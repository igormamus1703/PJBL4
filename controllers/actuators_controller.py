from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.iot.actuators import Actuator
import flask_login
from models.user.decorators import role_required

actuator_ = Blueprint("actuator_", __name__, template_folder="views")

@actuator_.route('/register_actuator')
@flask_login.login_required
@role_required(1)  # Somente Admin
def register_actuator():
    return render_template("register_actuator.html")

@actuator_.route('/add_actuator', methods=['POST'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def add_actuator():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")

    is_active = True if request.form.get("is_active") == "on" else False

    Actuator.save_actuator(name, brand, model, topic, unit, is_active)
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators = actuators)

@actuator_.route('/actuators')
@role_required(1, 2, 3)  # Todos
@flask_login.login_required
def actuators():
    actuators = Actuator.get_actuators()
    return render_template("actuators.html", actuators=actuators)

@actuator_.route('/edit_actuator')
@flask_login.login_required
@role_required(1)  # Somente Admin
def edit_actuator():
    id = request.args.get('id', None)
    actuator = Actuator.get_single_actuator(id)
    return render_template("update_actuator.html", actuator=actuator)

@actuator_.route('/update_actuator', methods=['POST'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def update_actuator():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    actuators = Actuator.update_actuator(id, name, brand, model, topic, unit, is_active)
    return render_template("actuators.html", actuators=actuators)

@actuator_.route('/del_actuator', methods=['GET'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def del_actuator():
    id = request.args.get('id', None)
    actuators = Actuator.delete_actuator(id)
    return render_template("actuators.html", actuators=actuators)
