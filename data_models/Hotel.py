from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  # Base importieren, je nach deiner Projektstruktur

class Hotel(Base):
    __tablename__ = 'hotel'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    stars = Column(Integer)
    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship("Address", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotel")

    def __repr__(self):
        return f"<Hotel(name={self.name}, stars={self.stars})>"
