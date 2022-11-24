from db import Base

from sqlalchemy import Column, Integer, String


class ST(Base):
    __tablename__ = "stolitsa"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String, nullable=False)
    floor = Column(String, nullable=False)
    price = Column(String, nullable=False)
    link = Column(String, nullable=False)
    meters = Column(String, nullable=False)


"""
class Realt(ST):
    __tablename__ = 'realt'

    id_realt = Column(Integer, primary_key=True, nullable=False) 
    phone = Column(String, nullable=False)
    date_publ = Column(String, nullable=False)
"""
