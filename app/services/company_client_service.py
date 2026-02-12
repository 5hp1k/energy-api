from typing import List, Dict, Any, Optional
from repositories.company_client_repository import CompanyClientRepository


class CompanyClientService:
    """Сервис для бизнес-логики клиентов компаний"""
    
    def __init__(self):
        self.client_repo = CompanyClientRepository()
    
    def get_all_clients(self) -> List[Dict[str, Any]]:
        """Получить всех клиентов"""
        clients = self.client_repo.get_all()
        return [self.client_repo.to_dict(client) for client in clients]
    
    def get_client_by_id(self, client_id: int) -> Optional[Dict[str, Any]]:
        """Получить клиента по ID"""
        client = self.client_repo.get_by_id(client_id)
        return self.client_repo.to_dict(client) if client else None
    
    def delete_client(self, client_id: int) -> bool:
        """Удалить клиента"""
        return self.client_repo.delete_by_id(client_id)
