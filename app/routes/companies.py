from flask import Blueprint, request, jsonify
from services.company_service import CompanyService
from error_handlers import ValidationError, NotFoundError


companies_bp = Blueprint('companies', __name__)
company_service = CompanyService()


@companies_bp.route('', methods=['GET'])
def get_companies():
    """Получить список всех компаний"""
    companies = company_service.get_all_companies()
    return jsonify(companies), 200


@companies_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """Получить компанию по ID"""
    company = company_service.get_company_by_id(company_id)
    
    if not company:
        raise NotFoundError(f'Company with ID {company_id} not found')
    
    return jsonify(company), 200


@companies_bp.route('', methods=['POST'])
def create_company():
    """Создать новую компанию"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('No data provided')
    
    # Валидация обязательных полей
    required_fields = ['name', 'registration_date', 'status']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValidationError(
            f'Missing required fields: {", ".join(missing_fields)}',
            payload={'missing_fields': missing_fields}
        )
    
    # Валидация статуса
    valid_statuses = ['active', 'inactive', 'pending']
    if data['status'] not in valid_statuses:
        raise ValidationError(
            f'Invalid status. Must be one of: {", ".join(valid_statuses)}',
            payload={'valid_statuses': valid_statuses}
        )
    
    company = company_service.create_company(
        data['name'],
        data['registration_date'],
        data['status']
    )
    
    return jsonify(company), 201


@companies_bp.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """Обновить компанию"""
    data = request.get_json()
    
    if not data:
        raise ValidationError('No data provided')
    
    # Валидация статуса если он присутствует
    if 'status' in data:
        valid_statuses = ['active', 'inactive', 'pending']
        if data['status'] not in valid_statuses:
            raise ValidationError(
                f'Invalid status. Must be one of: {", ".join(valid_statuses)}',
                payload={'valid_statuses': valid_statuses}
            )
    
    company = company_service.update_company(company_id, data)
    
    if not company:
        raise NotFoundError(f'Company with ID {company_id} not found')
    
    return jsonify(company), 200


@companies_bp.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """Удалить компанию"""
    success = company_service.delete_company(company_id)
    
    if not success:
        raise NotFoundError(f'Company with ID {company_id} not found')
    
    return jsonify({
        'message': 'Company deleted successfully',
        'company_id': company_id
    }), 200


@companies_bp.route('/<int:company_id>/statistics', methods=['GET'])
def get_company_statistics(company_id):
    """Получить статистику по компании"""
    statistics = company_service.get_company_statistics(company_id)
    
    if not statistics:
        raise NotFoundError(f'Company with ID {company_id} not found')
    
    return jsonify(statistics), 200
