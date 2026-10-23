
"""Safely populate an empty database with sample fleet data."""

import random
from datetime import date, timedelta

from database import db
from models import Vehicle, FuelLog

VEHICLE_SAMPLES = [
    {"vehicle_code": "TRK-001", "make": "Volvo", "model": "FH16", "year": 2020, "fuel_type": "Diesel", "tank_capacity_liters": 400},
    {"vehicle_code": "TRK-002", "make": "Scania", "model": "R450", "year": 2019, "fuel_type": "Diesel", "tank_capacity_liters": 380},
    {"vehicle_code": "VAN-001", "make": "Ford", "model": "Transit", "year": 2021, "fuel_type": "Petrol", "tank_capacity_liters": 80},
    {"vehicle_code": "TRK-003", "make": "MAN", "model": "TGX", "year": 2022, "fuel_type": "Diesel", "tank_capacity_liters": 420},
    {"vehicle_code": "VAN-002", "make": "Mercedes", "model": "Sprinter", "year": 2020, "fuel_type": "Diesel", "tank_capacity_liters": 93},
]

ROUTES = [
    "City-Depot A",
    "Highway North",
    "Highway South",
    "Regional East",
    "Port Route",
]


def populate_if_empty():
    # Do not delete or overwrite existing data.
    if Vehicle.query.count() > 0:
        print("Vehicles already exist; skipping sample-data setup.")
        return

    vehicles = [Vehicle(**item) for item in VEHICLE_SAMPLES]
    db.session.add_all(vehicles)
    db.session.commit()

    start_date = date.today() - timedelta(days=180)

    for vehicle in vehicles:
        odometer = random.randint(10000, 50000)
        current_date = start_date

        while current_date <= date.today():
            liters = round(
                random.uniform(30, vehicle.tank_capacity_liters * 0.8), 1
            )
            odometer += random.randint(300, 900)

            db.session.add(FuelLog(
                vehicle_id=vehicle.id,
                log_date=current_date,
                liters_filled=liters,
                odometer_km=odometer,
                cost=round(liters * random.uniform(1.4, 1.9), 2),
                route=random.choice(ROUTES),
            ))

            current_date += timedelta(days=random.randint(5, 12))

    db.session.commit()
    print("Sample vehicles and fuel logs added successfully.")
