"""
Populates the database with sample vehicles and fuel logs.
Run with:  python seed_data.py
"""
import random
from datetime import date, timedelta

from app import create_app
from database import db
from models import Vehicle, FuelLog

VEHICLE_SAMPLES = [
    {'vehicle_code': 'TRK-001', 'make': 'Volvo', 'model': 'FH16', 'year': 2020, 'fuel_type': 'Diesel', 'tank_capacity_liters': 400},
    {'vehicle_code': 'TRK-002', 'make': 'Scania', 'model': 'R450', 'year': 2019, 'fuel_type': 'Diesel', 'tank_capacity_liters': 380},
    {'vehicle_code': 'VAN-001', 'make': 'Ford', 'model': 'Transit', 'year': 2021, 'fuel_type': 'Petrol', 'tank_capacity_liters': 80},
    {'vehicle_code': 'TRK-003', 'make': 'MAN', 'model': 'TGX', 'year': 2022, 'fuel_type': 'Diesel', 'tank_capacity_liters': 420},
    {'vehicle_code': 'VAN-002', 'make': 'Mercedes', 'model': 'Sprinter', 'year': 2020, 'fuel_type': 'Diesel', 'tank_capacity_liters': 93},
]

ROUTES = ['City-Depot A', 'Highway North', 'Highway South', 'Regional East', 'Port Route']


def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        vehicles = []
        for v in VEHICLE_SAMPLES:
            vehicle = Vehicle(**v)
            db.session.add(vehicle)
            vehicles.append(vehicle)
        db.session.commit()

        start_date = date.today() - timedelta(days=180)
        for vehicle in vehicles:
            odometer = random.randint(10000, 50000)
            current_date = start_date
            while current_date <= date.today():
                liters = round(random.uniform(30, vehicle.tank_capacity_liters * 0.8), 1)
                distance = random.randint(300, 900)
                odometer += distance
                cost = round(liters * random.uniform(1.4, 1.9), 2)
                log = FuelLog(
                    vehicle_id=vehicle.id,
                    log_date=current_date,
                    liters_filled=liters,
                    odometer_km=odometer,
                    cost=cost,
                    route=random.choice(ROUTES),
                )
                db.session.add(log)
                current_date += timedelta(days=random.randint(5, 12))

        db.session.commit()
        print(f"Seeded {len(vehicles)} vehicles with fuel logs into the database.")


if __name__ == '__main__':
    seed()
