from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.iot.sensors import Sensor
import flask_login
from models.user.decorators import role_required

sensor_ = Blueprint("sensor_",__name__, template_folder="views")

@sensor_.route('/register_sensor')
@flask_login.login_required
@role_required(1)  # Somente Admin
def register_sensor():
    return render_template("register_sensor.html")

@sensor_.route('/add_sensor', methods=['POST'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def add_sensor():
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")

    is_active = True if request.form.get("is_active") == "on" else False

    Sensor.save_sensor(name, brand, model, topic, unit, is_active )
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors = sensors)

@sensor_.route('/sensors')
@flask_login.login_required
@role_required(1, 2, 3) # Todos
def sensors():
    sensors = Sensor.get_sensors()
    return render_template("sensors.html", sensors=sensors)

@sensor_.route('/edit_sensor')
@role_required(1)  # Somente Admin
@flask_login.login_required
def edit_sensor():
    id = request.args.get('id', None)
    sensor = Sensor.get_single_sensor(id)
    return render_template("update_sensor.html", sensor = sensor)

@sensor_.route('/update_sensor', methods=['POST'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def update_sensor():
    id = request.form.get("id")
    name = request.form.get("name")
    brand = request.form.get("brand")
    model = request.form.get("model")
    topic = request.form.get("topic")
    unit = request.form.get("unit")
    is_active = True if request.form.get("is_active") == "on" else False

    sensors = Sensor.update_sensor(id, name, brand, model, topic, unit, is_active )

    return render_template("sensors.html", sensors = sensors)

@sensor_.route('/del_sensor', methods=['GET'])
@flask_login.login_required
@role_required(1)  # Somente Admin
def del_sensor():
    id = request.args.get('id', None)
    sensors = Sensor.delete_sensor(id)
    return render_template("sensors.html", sensors = sensors)