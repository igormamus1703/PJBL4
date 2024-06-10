from flask import Flask
from models import *

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all() 

        # Criar roles
        Role.save_role("Admin", "Usuário com acesso total")
        Role.save_role("Moderador", "Usuário com permissões de moderação")
        Role.save_role("Usuario", "Usuário comum")

        # Criar usuários
        User.save_user("Admin", "Admin", "admin", "admin")
        User.save_user("Moderador", "Moderador", "moderador", "moderador")
        User.save_user("Usuario", "Usuario", "usuario", "usuario")

        # Criar sensores
        Sensor.save_sensor(name="sensor_gas", brand="honey", model="honey", topic="honey/sensorgas", unit="%", is_active=True)
        Sensor.save_sensor(name="sensor_temperatura", brand="honey", model="honey", topic="honey/sensortemperatura", unit="celsius", is_active=True)
        Sensor.save_sensor(name="sensor_umidade", brand="honey", model="honey", topic="honey/sensorumidade", unit="%", is_active=True)

        Actuator.save_actuator(name="actuator_buzzer", brand="honey", model="honey", topic="honey/buzzer", unit="test", is_active=True)
        Actuator.save_actuator(name="actuator_led", brand="honey", model="honey", topic="honey/led", unit="test", is_active=True)