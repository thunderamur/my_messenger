import sys


try:
    import sqlalchemy
    print(sqlalchemy.__version__)
except ImportError:
    print('Библиотека SQLAlchemy не найдена')
    sys.exit(13)


from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///mydb.sqlite', echo=True)
Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    login = Column(String(20))
    info = Column(String(50))

    def __init__(self, login, info):
        self.login = login
        self.info = info

    def __repr__(self):
        return "<User('{}', '{}')>".format(self.login, self.info)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
print('Session:', session)

client = Client('Client-1', '')
session.add(client)
session.commit()