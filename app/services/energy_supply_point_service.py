from typing import List, Dict, Any, Optional
from repositories.energy_supply_point_repository import EnergySupplyPointRepository


class EnergySupplyPointService:
    """Сервис для бизнес-логики точек поставки"""
    
    def __init__(self):
        self.energy_point_repo = EnergySupplyPointRepository()
    
    def get_all_points(self) -> List[Dict[str, Any]]:
        """Получить все точки поставки"""
        points = self.energy_point_repo.get_all()
        return [self.energy_point_repo.to_dict(point) for point in points]
    
    def get_point_by_id(self, point_id: int) -> Optional[Dict[str, Any]]:
        """Получить точку поставки по ID"""
        point = self.energy_point_repo.get_by_id(point_id)
        return self.energy_point_repo.to_dict(point) if point else None
    
    def create_point(
        self,
        name: str,
        company_id: int,
        connection_date: str,
        max_power_kw: float
    ) -> Optional[Dict[str, Any]]:
        """Создать новую точку поставки"""
        point = self.energy_point_repo.create(
            name, company_id, connection_date, max_power_kw
        )
        if not point:
            return None
        return self.energy_point_repo.to_dict(point)
    
    def update_point(
        self,
        point_id: int,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Обновить точку поставки"""
        point = self.energy_point_repo.get_by_id(point_id)
        if not point:
            return None
        
        updated_point = self.energy_point_repo.update(point, data)
        if not updated_point:
            return None
        
        return self.energy_point_repo.to_dict(updated_point)
    
    def delete_point(self, point_id: int) -> bool:
        """Удалить точку поставки"""
        point = self.energy_point_repo.get_by_id(point_id)
        if not point:
            return False
        
        self.energy_point_repo.delete(point)
        return True
    
    def search_points_by_date(
        self,
        date_from: Optional[str],
        date_to: Optional[str]
    ) -> List[Dict[str, Any]]:
        """Поиск точек поставки по дате"""
        return self.energy_point_repo.search_by_date_range(date_from, date_to)
    
    def rent_energy(
        self,
        point_id: int,
        company_name: str,
        quantity_power: float
    ) -> Dict[str, Any]:
        """Арендовать мощность"""
        return self.energy_point_repo.rent_energy(
            point_id, company_name, quantity_power
        )
