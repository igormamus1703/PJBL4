from models.db import db
from models.iot.sensors import Sensor
from models.iot.devices import Device
from datetime import datetime

class Read(db.Model):
    __tablename__ = 'read'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True)
    read_datetime = db.Column(db.DateTime(), nullable=False)
    sensors_id = db.Column(db.Integer, db.ForeignKey(Sensor.id), nullable=False)
    value = db.Column(db.Float, nullable=True)

    @staticmethod
    def save_read(topic, value):
        print(f"save_read called with topic={topic} and value={value}")
        sensor = Sensor.query.filter(Sensor.topic == topic).first()
        if sensor:
            print(f"Found sensor: {sensor}")
        device = Device.query.filter(Device.id == sensor.devices_id).first()
        if device:
            print(f"Found device: {device}")
        if sensor is not None and device.is_active:
            read = Read(read_datetime=datetime.now(), sensors_id=sensor.id, value=float(value))
            db.session.add(read)
            db.session.commit()
            print("Data saved to database")
        else:
            print("Sensor or device not found or device not active")

    @staticmethod
    def get_read(device_id, start, end):
        sensor = Sensor.query.filter(Sensor.devices_id == device_id).first()
        read = Read.query.filter(Read.sensors_id == sensor.id,
                                Read.read_datetime > start,
                                Read.read_datetime<end).all()
        return read
