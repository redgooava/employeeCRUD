'''
Моделька таблицы employee
'''

from sqlalchemy import Column, Integer, String
from ..db import Base


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    email = Column(String(100), unique=True)

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"
