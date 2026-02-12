from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Type
from models import db

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Базовый репозиторий с общими CRUD операциями"""
    
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def get_all(self) -> List[T]:
        """Получить все записи"""
        return self.model_class.query.all()
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Получить запись по ID"""
        return self.model_class.query.get(entity_id)
    
    def add(self, entity: T) -> T:
        """Добавить запись"""
        db.session.add(entity)
        db.session.commit()
        return entity
    
    def delete(self, entity: T) -> None:
        """Удалить запись"""
        db.session.delete(entity)
        db.session.commit()
    
    @abstractmethod
    def to_dict(self, entity: T) -> dict:
        """Преобразовать сущность в словарь"""
        return
