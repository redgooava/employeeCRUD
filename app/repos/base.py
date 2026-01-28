'''
Абстракция для репозитория
'''
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Абстрактный базовый класс репозитория"""

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def get(self, id: int) -> Optional[T]:
        """Получить запись по ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Получить все записи"""
        pass

    @abstractmethod
    def create(self, **kwargs) -> T:
        """Создать новую запись"""
        pass

    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Обновить запись"""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Удалить запись"""
        pass

    def commit(self):
        """Сохранить изменения"""
        self.db.commit()

    def rollback(self):
        """Откатить изменения"""
        self.db.rollback()