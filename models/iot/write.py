from models.db import db
from models.iot.actuators import Actuator
from models.iot.devices import Device
from datetime import datetime

class Write(db.Model):
    __tablename__ = 'write'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    write_datetime = db.Column(db.DateTime(), nullable=False)
    actuators_id = db.Column(db.Integer, db.ForeignKey(Actuator.id), nullable=False)
    #value = db.Column(db.Float, nullable=True)
    value = db.Column(db.String(10), nullable=True)

    @staticmethod
    def save_write(actuator_name, value):
        print(f"save_write called with actuator_name: {actuator_name}, value: {value}")  # Debug print
        actuator = Actuator.query.join(Device).filter(Device.name == actuator_name).first()
        if actuator:
            device = Device.query.filter(Device.id == actuator.devices_id).first()
            if device and device.is_active:
                write = Write(write_datetime=datetime.now(), actuators_id=actuator.id, value=value)
                db.session.add(write)
                db.session.commit()
                print("Write saved successfully")
            else:
                print("Device is not active or does not exist")
        else:
            print("Actuator not found")

    @staticmethod
    def get_write(actuator_id, start, end):
        actuator = Actuator.query.filter(Actuator.devices_id == actuator_id).first()
        write = Write.query.filter(Write.actuators_id == actuator.id,
                                   Write.write_datetime > start,
                                   Write.write_datetime < end).all()
        return write
