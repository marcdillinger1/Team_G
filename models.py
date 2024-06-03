from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    star_rating = Column(Integer)
    # Weitere Modelle folgen ...

def init_db(uri):
    # Initialisiert die Datenbank und erstellt alle definierten Tabellen
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    return engine
