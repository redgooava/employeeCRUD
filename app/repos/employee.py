'''
Репозиторий EmployeeRepository
'''

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from ..models.employee import Employee
from ..repos.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):

    def __init__(self, db: Session):
        super().__init__(db)
        self.model = Employee

    def get(self, id: int) -> Optional[Employee]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> list[type[Employee]]:
        return self.db.query(self.model).all()

    def create(self, **kwargs) -> Employee:
        db_employee = self.model(**kwargs)
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return db_employee

    def update(self, id: int, **kwargs) -> Optional[Employee]:
        employee = self.get(id)
        if not employee:
            return None

        for key, value in kwargs.items():
            if hasattr(employee, key):
                setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, id: int) -> bool:
        employee = self.get(id)
        if not employee:
            return False

        self.db.delete(employee)
        self.db.commit()
        return True

    def get_or_404(self, id: int) -> Optional[Employee]:
        data = self.db.query(self.model).filter(self.model.id == id).first()
        return data if data else None
