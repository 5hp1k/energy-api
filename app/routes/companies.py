from flask import Blueprint, request, jsonify
from services.company_service import CompanyService


companies_bp = Blueprint('companies', __name__)
company_service = CompanyService()


@companies_bp.route('', methods=['GET'])
def get_companies():
    """Получить список всех компаний"""
    try:
        companies = company_service.get_all_companies()
        return jsonify(companies), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """Получить компанию по ID"""
    try:
        company = company_service.get_company_by_id(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        return jsonify(company), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('', methods=['POST'])
def create_company():
    """Создать новую компанию"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['name', 'registration_date', 'status']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        company = company_service.create_company(
            data['name'],
            data['registration_date'],
            data['status']
        )
        
        return jsonify(company), 201
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """Обновить компанию"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        company = company_service.update_company(company_id, data)
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        return jsonify(company), 200
    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """Удалить компанию"""
    try:
        success = company_service.delete_company(company_id)
        if not success:
            return jsonify({'error': 'Company not found'}), 404
        
        return jsonify({'message': 'Company deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@companies_bp.route('/<int:company_id>/statistics', methods=['GET'])
def get_company_statistics(company_id):
    """Получить статистику по компании"""
    try:
        statistics = company_service.get_company_statistics(company_id)
        if not statistics:
            return jsonify({'error': 'Company not found'}), 404
        
        return jsonify(statistics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
