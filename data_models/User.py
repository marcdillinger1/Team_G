from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  # Base importieren, je nach deiner Projektstruktur

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  # Beachte Sicherheitspraktiken bei Produktionseinsatz!
    bookings = relationship("Booking", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username})>"
