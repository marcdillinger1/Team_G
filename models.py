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

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    room_type = Column(String)
    price = Column(Float)
    hotel = relationship("Hotel", back_populates="rooms")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    room = relationship("Room", back_populates="bookings")

Hotel.rooms = relationship("Room", order_by=Room.id, back_populates="hotel")
Room.bookings = relationship("Booking", order_by=Booking.id, back_populates="room")

def init_db(uri):
    engine = create_engine(uri)
    Base.metadata.create_all(engine)
    return engine

