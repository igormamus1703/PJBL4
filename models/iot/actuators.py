from models.db import db
from models.iot.devices import Device
#from models.iot.actuators import Actuator

class Actuator(db.Model):
    __tablename__ = 'actuators'
    id = db.Column('id', db.Integer, primary_key=True)
    devices_id = db.Column(db.Integer, db.ForeignKey(Device.id))
    unit = db.Column(db.String(50))
    topic = db.Column(db.String(50))

    device = db.relationship('Device', back_populates='actuators')
    
    @staticmethod
    def save_actuator(name, brand, model, topic, unit, is_active):
        # Criar o dispositivo
        device = Device(name=name, brand=brand, model=model, is_active=is_active)
        db.session.add(device)
        db.session.commit()  # Confirmar o dispositivo para garantir que ele tenha um ID
        
        # Criar o atuador
        actuator = Actuator(devices_id=device.id, unit=unit, topic=topic)
        db.session.add(actuator)
        db.session.commit()  # Confirmar o atuador para salvar no banco de dados

    @staticmethod
    def get_actuators():
        actuators = Actuator.query.join(Device, Device.id == Actuator.devices_id) \
            .add_columns(Device.id, Device.name, Device.brand, Device.model, 
                         Device.is_active, Actuator.topic, Actuator.unit).all()
        return actuators
    
    @staticmethod
    def get_single_actuator(id):
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if actuator is not None:

            actuator = Actuator.query.filter(Actuator.devices_id == id)\
            .join(Device).add_columns(Device.id, Device.name, Device.brand,
            Device.model, Device.is_active, Actuator.topic, Actuator.unit).first()
            return [actuator]
        
    @staticmethod
    def update_actuator(id, name, brand, model, topic, unit, is_active):
        device = Device.query.filter(Device.id == id).first()
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        if device is not None:
            device.name = name
            device.brand = brand
            device.model = model
            actuator.topic = topic
            actuator.unit = unit
            device.is_active = is_active
            db.session.commit()
            return Actuator.get_actuators()
        
    @staticmethod
    def delete_actuator(id):
        device = Device.query.filter(Device.id == id).first()
        actuator = Actuator.query.filter(Actuator.devices_id == id).first()
        db.session.delete(actuator)
        db.session.delete(device)
        db.session.commit()
        return Actuator.get_actuators()

