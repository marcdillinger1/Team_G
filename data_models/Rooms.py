from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  # Base importieren, je nach deiner Projektstruktur

class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    number = Column(String)
    type = Column(String)
    max_guests = Column(Integer)
    description = Column(String)
    amenities = Column(String)
    price = Column(Float)
    hotel_id = Column(Integer, ForeignKey('hotel.id'))
    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

    def __repr__(self):
        return f"<Room(number={self.number}, type={self.type}, max_guests={self.max_guests})>"
