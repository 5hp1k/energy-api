from typing import Optional
from models import db, CompanyClient
from repositories.base import BaseRepository


class CompanyClientRepository(BaseRepository[CompanyClient]):
    """Репозиторий для работы с клиентами компаний"""
    
    def __init__(self):
        super().__init__(CompanyClient)
    
    def delete_by_id(self, client_id: int) -> bool:
        """Удалить клиента по ID"""
        client = self.get_by_id(client_id)
        if not client:
            return False
        self.delete(client)
        return True
    
    def to_dict(self, client: CompanyClient) -> dict:
        return client.to_dict()
