from flask import Blueprint, jsonify
from services.company_client_service import CompanyClientService
from error_handlers import NotFoundError

company_clients_bp = Blueprint('company_clients', __name__)
client_service = CompanyClientService()


@company_clients_bp.route('', methods=['GET'])
def get_company_clients():
    """Получить список всех клиентов"""
    clients = client_service.get_all_clients()
    return jsonify(clients), 200


@company_clients_bp.route('/<int:client_id>', methods=['GET'])
def get_company_client(client_id):
    """Получить клиента по ID"""
    client = client_service.get_client_by_id(client_id)
    
    if not client:
        raise NotFoundError(f'Company client with ID {client_id} not found')
    
    return jsonify(client), 200


@company_clients_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_company_client(client_id):
    """Удалить клиента"""
    success = client_service.delete_client(client_id)
    
    if not success:
        raise NotFoundError(f'Company client with ID {client_id} not found')
    
    return jsonify({
        'message': 'Company client deleted successfully',
        'client_id': client_id
    }), 200
