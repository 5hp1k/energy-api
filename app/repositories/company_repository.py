from datetime import datetime
from typing import Optional, Dict, Any
from models import db, Company
from repositories.base import BaseRepository
from sqlalchemy import text


class CompanyRepository(BaseRepository[Company]):
    """Репозиторий для работы с компаниями"""
    
    def __init__(self):
        super().__init__(Company)
    
    def create(self, name: str, registration_date: str, status: str) -> Company:
        """Создать новую компанию"""
        company = Company(
            name=name,
            registration_date=datetime.strptime(registration_date, '%Y-%m-%d').date(),
            status=status
        )
        return self.add(company)
    
    def update(self, company: Company, data: Dict[str, Any]) -> Company:
        """Обновить компанию"""
        if 'name' in data:
            company.name = data['name']
        if 'registration_date' in data:
            company.registration_date = datetime.strptime(
                data['registration_date'], '%Y-%m-%d'
            ).date()
        if 'status' in data:
            company.status = data['status']
        
        db.session.commit()
        return company
    
    def get_statistics(self, company_id: int) -> Optional[Dict[str, Any]]:
        """Получить статистику по компании через хранимую функцию"""
        result = db.session.execute(
            text('SELECT * FROM get_company_statistics(:company_id)'),
            {'company_id': company_id}
        )
        row = result.fetchone()
        
        if row:
            return {
                'company_id': company_id,
                'total_supply_points': row[0],
                'max_total_power': float(row[1]) if row[1] else 0
            }
        return None
    
    def to_dict(self, company: Company) -> dict:
        return company.to_dict()
