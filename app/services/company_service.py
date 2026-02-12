from typing import List, Dict, Any, Optional
from repositories.company_repository import CompanyRepository


class CompanyService:
    """Сервис для бизнес-логики компаний"""
    
    def __init__(self):
        self.company_repo = CompanyRepository()
    
    def get_all_companies(self) -> List[Dict[str, Any]]:
        """Получить все компании"""
        companies = self.company_repo.get_all()
        return [self.company_repo.to_dict(company) for company in companies]
    
    def get_company_by_id(self, company_id: int) -> Optional[Dict[str, Any]]:
        """Получить компанию по ID"""
        company = self.company_repo.get_by_id(company_id)
        return self.company_repo.to_dict(company) if company else None
    
    def create_company(
        self, 
        name: str, 
        registration_date: str, 
        status: str
    ) -> Dict[str, Any]:
        """Создать новую компанию"""
        company = self.company_repo.create(name, registration_date, status)
        return self.company_repo.to_dict(company)
    
    def update_company(
        self, 
        company_id: int, 
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Обновить компанию"""
        company = self.company_repo.get_by_id(company_id)
        if not company:
            return None
        
        updated_company = self.company_repo.update(company, data)
        return self.company_repo.to_dict(updated_company)
    
    def delete_company(self, company_id: int) -> bool:
        """Удалить компанию"""
        company = self.company_repo.get_by_id(company_id)
        if not company:
            return False
        
        self.company_repo.delete(company)
        return True
    
    def get_company_statistics(self, company_id: int) -> Optional[Dict[str, Any]]:
        """Получить статистику по компании"""
        company = self.company_repo.get_by_id(company_id)
        if not company:
            return None
        
        return self.company_repo.get_statistics(company_id)
