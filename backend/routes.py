from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import func

from database import db
from models import Vehicle, FuelLog

api_bp = Blueprint('api', __name__)


# ---------- Vehicles ----------

@api_bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([v.to_dict() for v in vehicles])


@api_bp.route('/vehicles', methods=['POST'])
def add_vehicle():
    data = request.get_json()
    vehicle = Vehicle(
        vehicle_code=data['vehicle_code'],
        make=data.get('make'),
        model=data.get('model'),
        year=data.get('year'),
        fuel_type=data.get('fuel_type', 'Diesel'),
        tank_capacity_liters=data.get('tank_capacity_liters'),
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify(vehicle.to_dict()), 201


# ---------- Fuel Logs ----------

@api_bp.route('/fuel-logs', methods=['GET'])
def get_fuel_logs():
    vehicle_id = request.args.get('vehicle_id')
    query = FuelLog.query
    if vehicle_id:
        query = query.filter_by(vehicle_id=vehicle_id)
    logs = query.order_by(FuelLog.log_date.desc()).all()
    return jsonify([l.to_dict() for l in logs])


@api_bp.route('/fuel-logs', methods=['POST'])
def add_fuel_log():
    data = request.get_json()
    log = FuelLog(
        vehicle_id=data['vehicle_id'],
        log_date=datetime.strptime(data['log_date'], '%Y-%m-%d').date(),
        liters_filled=data['liters_filled'],
        odometer_km=data['odometer_km'],
        cost=data.get('cost'),
        route=data.get('route'),
    )
    db.session.add(log)
    db.session.commit()
    return jsonify(log.to_dict()), 201


# ---------- Analytics ----------

@api_bp.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    total_fuel = db.session.query(func.sum(FuelLog.liters_filled)).scalar() or 0
    total_cost = db.session.query(func.sum(FuelLog.cost)).scalar() or 0
    total_vehicles = Vehicle.query.count()
    total_logs = FuelLog.query.count()
    return jsonify({
        'total_fuel_liters': round(total_fuel, 2),
        'total_cost': round(total_cost, 2),
        'total_vehicles': total_vehicles,
        'total_fuel_logs': total_logs,
    })


@api_bp.route('/analytics/vehicle/<int:vehicle_id>', methods=['GET'])
def analytics_vehicle(vehicle_id):
    logs = FuelLog.query.filter_by(vehicle_id=vehicle_id).order_by(FuelLog.odometer_km.asc()).all()
    if len(logs) < 2:
        return jsonify({'error': 'Not enough fuel-log data to compute consumption'}), 400

    total_distance = logs[-1].odometer_km - logs[0].odometer_km
    total_fuel = sum(l.liters_filled for l in logs[1:])  # fuel used between fill-ups
    avg_consumption = round((total_fuel / total_distance) * 100, 2) if total_distance > 0 else None

    return jsonify({
        'vehicle_id': vehicle_id,
        'total_distance_km': total_distance,
        'total_fuel_liters': round(total_fuel, 2),
        'avg_consumption_l_per_100km': avg_consumption,
        'log_count': len(logs),
    })


@api_bp.route('/analytics/monthly', methods=['GET'])
def analytics_monthly():
    logs = FuelLog.query.all()
    monthly = {}
    for log in logs:
        key = log.log_date.strftime('%Y-%m')
        if key not in monthly:
            monthly[key] = {'month': key, 'total_liters': 0, 'total_cost': 0, 'fill_count': 0}
        monthly[key]['total_liters'] += log.liters_filled
        monthly[key]['total_cost'] += (log.cost or 0)
        monthly[key]['fill_count'] += 1

    result = sorted(monthly.values(), key=lambda x: x['month'])
    for r in result:
        r['total_liters'] = round(r['total_liters'], 2)
        r['total_cost'] = round(r['total_cost'], 2)
    return jsonify(result)
