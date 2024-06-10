from flask import Blueprint, render_template
from models.iot.read import Read
from models.iot.sensors import Sensor
import flask_login
from models.user.decorators import role_required

mqtt = Blueprint("mqtt", __name__, template_folder="views")

@mqtt.route('/tempo_real')
@flask_login.login_required
@role_required(1, 2, 3)  # Todos
def tempo_real():
    try:
        # Buscar os sensores
        sensors = Sensor.get_sensors()
        
        # Buscar os valores mais recentes para cada sensor
        reads = {}
        for sensor in sensors:
            recent_read = Read.query.filter_by(sensors_id=sensor.id).order_by(Read.read_datetime.desc()).first()
            if recent_read:
                reads[sensor.id] = recent_read.value
            else:
                reads[sensor.id] = 'N/A'  # Ou um valor padrão

        return render_template("tr.html", sensors=sensors, reads=reads)
    except Exception as e:
        # Logar o erro
        print(f"Erro ao carregar dados de sensores: {e}")
        return render_template("error.html", message="Erro ao carregar dados de sensores.")
