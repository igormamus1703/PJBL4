from flask import Flask, render_template, request
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read
from controllers.writes_controller import write
from controllers.users_controller import user
from controllers.login_controller import login
from controllers.publish_controller import publish
from controllers.mqtt_controller import mqtt
from models.iot.read import Read
from models.iot.write import Write
#from models.user.roles import Role
from models.user.users import User
from models.db import db, instance
from flask_mqtt import Mqtt
import flask_login
from flask_login import LoginManager, logout_user
import json


def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")
    
    app.secret_key = 'd54gdh543trg@!54gdh'
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    app.register_blueprint(sensor_, url_prefix='/sensors')
    app.register_blueprint(actuator_, url_prefix="/actuators")
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    app.register_blueprint(user, url_prefix='/users')
    app.register_blueprint(login, url_prefix='/auth')
    app.register_blueprint(publish, url_prefix='/publish')
    app.register_blueprint(mqtt, url_prefix='/mqtt')

    @login_manager.user_loader
    def get_user(user_id):
        user = User.get_user_id(user_id)
        return user

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_USERNAME'] = '' # Set this item when you need to verify username and password
    app.config['MQTT_PASSWORD'] = '' # Set this item when you need to verify username and password
    app.config['MQTT_KEEPALIVE'] = 5000 # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False # If your broker supports TLS, set it True
    mqtt_client= Mqtt()
    mqtt_client.init_app(app)

    '''
    @login_manager.user_loader
    def get_user(user_id):
        user = User.query.get(user_id)
        return user    
    '''


    topic_subscribe = "honey/data"
    topic_subscribeled = "honeyactuator/led"
    topic_subscribebuz = "honeyactuator/buzzer"

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Broker Connected successfully')
            mqtt_client.subscribe(topic_subscribe) # subscribe topic
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        print(f"Received message on topic {message.topic}: {message.payload}")
        try:
            js = json.loads(message.payload.decode())
            print(f"Parsed JSON: {js}")
            with app.app_context():
                if "sensor" in js:
                    Read.save_read(js["sensor"], js["valor"])
                    print(f"Saved read: sensor={js['sensor']}, valor={js['valor']}")
                    if js["sensor"] == 'honey/sensorgas':  # gas sensor
                        global ultimo_estado_led
                        novo_estado_led = "ON" if int(js["valor"]) > 50 else "OFF"
                        try:
                            client.publish(topic_subscribeled, novo_estado_led)
                            print(f"Mensagem publicada em {topic_subscribeled}: {novo_estado_led}")
                            # Salvar estado no banco de dados
                            Write.save_write("actuator_led", novo_estado_led)
                        except Exception as e:
                            print(f"Erro ao publicar mensagem: {e}")
                        ultimo_estado_led = novo_estado_led
                        print(f"SENSOR GÁS LED: {novo_estado_led}")
                    elif js["sensor"] == 'honey/sensortemperatura':  # temperature sensor
                        global ultimo_estado_temperatura
                        novo_estado_temperatura = "ON" if float(js["valor"]) > 40 else "OFF"
                        try:
                            client.publish(topic_subscribebuz, novo_estado_temperatura)
                            print(f"Mensagem publicada em {topic_subscribebuz}: {novo_estado_temperatura}")
                            # Salvar estado no banco de dados
                            Write.save_write("actuator_buzzer", novo_estado_temperatura)
                        except Exception as e:
                            print(f"Erro ao publicar mensagem: {e}")
                        ultimo_estado_temperatura = novo_estado_temperatura
                        print(f"SENSOR TEMPERATURA BUZZER: {novo_estado_temperatura}")
                elif "actuator" in js:
                    Write.save_write(js["actuator"], js["valor"])
                    print(f"Saved write: actuator={js['actuator']}, valor={js['valor']}")
                else:
                    print("Unknown data type")
        except Exception as e:
            print(f"Failed to process message: {e}")


    @app.route('/')
    def index():
        return render_template("login.html")

    @app.route('/home')
    @flask_login.login_required
    def home():
        return render_template("home.html")
    
    return app