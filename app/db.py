'''
Коннект к БД
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import Config


class Base(DeclarativeBase):
    pass


engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True, connect_args={'client_encoding': 'utf8'})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables() -> None:
    Base.metadata.create_all(engine)

create_db_and_tables()
