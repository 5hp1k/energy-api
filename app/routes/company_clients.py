from flask import Blueprint, jsonify
from services.company_client_service import CompanyClientService

company_clients_bp = Blueprint('company_clients', __name__)
client_service = CompanyClientService()


@company_clients_bp.route('', methods=['GET'])
def get_company_clients():
    """Получить список всех клиентов"""
    try:
        clients = client_service.get_all_clients()
        return jsonify(clients), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_clients_bp.route('/<int:client_id>', methods=['GET'])
def get_company_client(client_id):
    """Получить клиента по ID"""
    try:
        client = client_service.get_client_by_id(client_id)
        if not client:
            return jsonify({'error': 'Company client not found'}), 404
        return jsonify(client), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_clients_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_company_client(client_id):
    """Удалить клиента"""
    try:
        success = client_service.delete_client(client_id)
        if not success:
            return jsonify({'error': 'Company client not found'}), 404
        
        return jsonify({'message': 'Company client deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
