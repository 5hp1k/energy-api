from flask import Blueprint, request, jsonify
from services.energy_supply_point_service import EnergySupplyPointService


energy_supply_points_bp = Blueprint('energy_supply_points', __name__)
energy_point_service = EnergySupplyPointService()


@energy_supply_points_bp.route('', methods=['GET'])
def get_energy_supply_points():
    """Получить список всех точек поставки"""
    try:
        points = energy_point_service.get_all_points()
        return jsonify(points), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@energy_supply_points_bp.route('/<int:point_id>', methods=['GET'])
def get_energy_supply_point(point_id):
    """Получить точку поставки по ID"""
    try:
        point = energy_point_service.get_point_by_id(point_id)
        if not point:
            return jsonify({'error': 'Energy supply point not found'}), 404
        return jsonify(point), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@energy_supply_points_bp.route('', methods=['POST'])
def create_energy_supply_point():
    """Создать новую точку поставки"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'company_id', 'connection_date', 'max_power_kw']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        point = energy_point_service.create_point(
            data['name'],
            data['company_id'],
            data['connection_date'],
            data['max_power_kw']
        )
        
        if not point:
            return jsonify({'error': 'Company not found'}), 404
        
        return jsonify(point), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@energy_supply_points_bp.route('/<int:point_id>', methods=['PUT'])
def update_energy_supply_point(point_id):
    """Обновить точку поставки"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        point = energy_point_service.update_point(point_id, data)
        if not point:
            return jsonify({'error': 'Energy supply point or company not found'}), 404
        
        return jsonify(point), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@energy_supply_points_bp.route('/<int:point_id>', methods=['DELETE'])
def delete_energy_supply_point(point_id):
    """Удалить точку поставки"""
    try:
        success = energy_point_service.delete_point(point_id)
        if not success:
            return jsonify({'error': 'Energy supply point not found'}), 404
        
        return jsonify({'message': 'Energy supply point deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@energy_supply_points_bp.route('/search', methods=['GET'])
def search_energy_supply_points():
    """Поиск точек поставки по дате присоединения"""
    try:
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        points = energy_point_service.search_points_by_date(date_from, date_to)
        return jsonify(points), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@energy_supply_points_bp.route('/<int:point_id>/rentals', methods=['POST'])
def rent_energy(point_id):
    """Арендовать мощность"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['company_name', 'quantity_power']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        result = energy_point_service.rent_energy(
            point_id,
            data['company_name'],
            data['quantity_power']
        )
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
