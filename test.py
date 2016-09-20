
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

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
    classType = Column(String, nullable=False)
    classId = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    
    def __repr__(self):
        return "<User(88id='%s', name='%s'>" % (self.bbs_id, self.name)

