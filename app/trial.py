import json
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tutorial.db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    bbs_id = Column(String)
    name = Column(String)
    sex = Column(String, nullable=False)
    city = Column(String)
    state = Column(String)
    class_type = Column(String, nullable=False)
    class_id = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    
    def __repr__(self):
        return "<User(88id='%s', name='%s'>" % (self.bbs_id, self.name)

Base.metadata.create_all(engine)


with open('ckc00.json') as fin:
    usrs = json.load(fin)

usr = usrs[0]

a = User(**usr)

Session = sessionmaker(bind=engine)

session = Session()

for usr in usrs:
    pass