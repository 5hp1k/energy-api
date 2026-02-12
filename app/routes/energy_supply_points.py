from flask import Blueprint, request, jsonify
from services.energy_supply_point_service import EnergySupplyPointService
from error_handlers import ValidationError, NotFoundError


energy_supply_points_bp = Blueprint('energy_supply_points', __name__)
energy_point_service = EnergySupplyPointService()


@energy_supply_points_bp.route('', methods=['GET'])
def get_energy_supply_points():
    """Получить список всех точек поставки"""
    points = energy_point_service.get_all_points()
    return jsonify(points), 200


@energy_supply_points_bp.route('/<int:point_id>', methods=['GET'])
def get_energy_supply_point(point_id):
    """Получить точку поставки по ID"""
    point = energy_point_service.get_point_by_id(point_id)
    
    if not point:
        raise NotFoundError(f'Energy supply point with ID {point_id} not found')
    
    return jsonify(point), 200


@energy_supply_points_bp.route('', methods=['POST'])
def create_energy_supply_point():
    """Создать новую точку поставки"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('No data provided')
    
    # Валидация обязательных полей
    required_fields = ['name', 'company_id', 'connection_date', 'max_power_kw']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValidationError(
            f'Missing required fields: {", ".join(missing_fields)}',
            payload={'missing_fields': missing_fields}
        )
    
    # Валидация max_power_kw
    try:
        max_power = float(data['max_power_kw'])
        if max_power <= 0:
            raise ValidationError('max_power_kw must be greater than 0')
    except (ValueError, TypeError):
        raise ValidationError('max_power_kw must be a valid number')
    
    point = energy_point_service.create_point(
        data['name'],
        data['company_id'],
        data['connection_date'],
        max_power
    )
    
    if not point:
        raise NotFoundError(f'Company with ID {data["company_id"]} not found')
    
    return jsonify(point), 201


@energy_supply_points_bp.route('/<int:point_id>', methods=['PUT'])
def update_energy_supply_point(point_id):
    """Обновить точку поставки"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('No data provided')
    
    # Валидация max_power_kw если присутствует
    if 'max_power_kw' in data:
        try:
            max_power = float(data['max_power_kw'])
            if max_power <= 0:
                raise ValidationError('max_power_kw must be greater than 0')
        except (ValueError, TypeError):
            raise ValidationError('max_power_kw must be a valid number')
    
    point = energy_point_service.update_point(point_id, data)
    
    if not point:
        raise NotFoundError(f'Energy supply point with ID {point_id} not found or related company not found')
    
    return jsonify(point), 200


@energy_supply_points_bp.route('/<int:point_id>', methods=['DELETE'])
def delete_energy_supply_point(point_id):
    """Удалить точку поставки"""
    success = energy_point_service.delete_point(point_id)
    
    if not success:
        raise NotFoundError(f'Energy supply point with ID {point_id} not found')
    
    return jsonify({
        'message': 'Energy supply point deleted successfully',
        'point_id': point_id
    }), 200


@energy_supply_points_bp.route('/search', methods=['GET'])
def search_energy_supply_points():
    """Поиск точек поставки по дате присоединения"""
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    # Валидация параметров поиска
    if date_from or date_to:
        if date_from and date_to:
            # Проверка что date_from <= date_to будет в сервисе
            pass
        elif date_from:
            # Только date_from
            pass
        elif date_to:
            # Только date_to
            pass
    
    points = energy_point_service.search_points_by_date(date_from, date_to)
    return jsonify(points), 200


@energy_supply_points_bp.route('/<int:point_id>/rentals', methods=['POST'])
def rent_energy(point_id):
    """Арендовать мощность"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('No data provided')
    
    # Валидация обязательных полей
    required_fields = ['company_name', 'quantity_power']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValidationError(
            f'Missing required fields: {", ".join(missing_fields)}',
            payload={'missing_fields': missing_fields}
        )
    
    # Валидация quantity_power
    try:
        quantity_power = float(data['quantity_power'])
        if quantity_power <= 0:
            raise ValidationError('quantity_power must be greater than 0')
    except (ValueError, TypeError):
        raise ValidationError('quantity_power must be a valid number')
    
    result = energy_point_service.rent_energy(
        point_id,
        data['company_name'],
        quantity_power
    )
    
    if result['success']:
        return jsonify(result), 201
    else:
        # Сервис вернул ошибку
        raise ValidationError(result.get('message', 'Failed to rent energy'), payload=result)

