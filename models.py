from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    room_type = Column(String, index=True)
    max_guests = Column(Integer)
    description = Column(String)
    price_per_night = Column(Float)
    available = Column(Boolean, default=True)
    amenities = Column(String)
    hotel = relationship("Hotel", back_populates="rooms")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    guest_name = Column(String)
    guest_email = Column(String)
    check_in = Column(Date)
    check_out = Column(Date)
    total_price = Column(Float)
    room = relationship("Room")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    bookings = relationship("Booking", back_populates="user")

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    stars = Column(Integer)
    rooms = relationship("Room", back_populates="hotel")
