from datetime import datetime
from database import db


class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_code = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20), default='Diesel')
    tank_capacity_liters = db.Column(db.Float)

    fuel_logs = db.relationship(
        'FuelLog', backref='vehicle', lazy=True, cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_code': self.vehicle_code,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'fuel_type': self.fuel_type,
            'tank_capacity_liters': self.tank_capacity_liters,
        }


class FuelLog(db.Model):
    __tablename__ = 'fuel_logs'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    liters_filled = db.Column(db.Float, nullable=False)
    odometer_km = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float)
    route = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'vehicle_id': self.vehicle_id,
            'log_date': self.log_date.isoformat() if self.log_date else None,
            'liters_filled': self.liters_filled,
            'odometer_km': self.odometer_km,
            'cost': self.cost,
            'route': self.route,
        }
