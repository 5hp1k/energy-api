from datetime import datetime
from typing import List, Optional, Dict, Any
from models import db, EnergySupplyPoint, Company
from repositories.base import BaseRepository
from sqlalchemy import text


class EnergySupplyPointRepository(BaseRepository[EnergySupplyPoint]):
    """Репозиторий для работы с точками поставки"""
    
    def __init__(self):
        super().__init__(EnergySupplyPoint)
    
    def create(self, name: str, company_id: int, connection_date: str, max_power_kw: float) -> Optional[EnergySupplyPoint]:
        """Создать новую точку поставки"""
        # Проверка существования компании
        company = Company.query.get(company_id)
        if not company:
            return None
        
        point = EnergySupplyPoint(
            name=name,
            company_id=company_id,
            connection_date=datetime.strptime(connection_date, '%Y-%m-%d').date(),
            max_power_kw=max_power_kw
        )
        return self.add(point)
    
    def update(self, point: EnergySupplyPoint, data: Dict[str, Any]) -> Optional[EnergySupplyPoint]:
        """Обновить точку поставки"""
        if 'name' in data:
            point.name = data['name']
        if 'company_id' in data:
            company = Company.query.get(data['company_id'])
            if not company:
                return None
            point.company_id = data['company_id']
        if 'connection_date' in data:
            point.connection_date = datetime.strptime(
                data['connection_date'], '%Y-%m-%d'
            ).date()
        if 'max_power_kw' in data:
            point.max_power_kw = data['max_power_kw']
        
        db.session.commit()
        return point
    
    def search_by_date_range(self, date_from: Optional[str], date_to: Optional[str]) -> List[Dict[str, Any]]:
        """Поиск точек поставки по дате через хранимую функцию"""
        result = db.session.execute(
            text('SELECT * FROM search_energy_supply_points(:date_from, :date_to)'),
            {'date_from': date_from, 'date_to': date_to}
        )
        
        points = []
        for row in result:
            points.append({
                'id': row[0],
                'name': row[1],
                'company_id': row[2],
                'connection_date': row[3].isoformat() if row[3] else None,
                'max_power_kw': float(row[4]) if row[4] else None,
                'created_at': row[5].isoformat() if row[5] else None
            })
        return points
    
    def rent_energy(self, point_id: int, company_name: str, quantity_power: float) -> Dict[str, Any]:
        """Арендовать мощность через хранимую функцию"""
        result = db.session.execute(
            text('SELECT * FROM rent_energy(:point_id, :company_name, :quantity_power)'),
            {
                'point_id': point_id,
                'company_name': company_name,
                'quantity_power': quantity_power
            }
        )
        
        row = result.fetchone()
        success = row[0]
        message = row[1]
        
        if success:
            db.session.commit()
        else:
            db.session.rollback()
        
        return {'success': success, 'message': message}
    
    def to_dict(self, point: EnergySupplyPoint) -> dict:
        return point.to_dict()
