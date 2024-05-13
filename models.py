from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    zip = Column(String)
    city = Column(String)

    def __repr__(self):
        return f"<Address(street={self.street}, city={self.city}, zip={self.zip})>"

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stars = Column(Integer)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship("Address", back_populates="hotels")
    rooms = relationship("Room", back_populates="hotel")

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    type = Column(String)
    max_guests = Column(Integer)
    description = Column(String)
    amenities = Column(String)
    price = Column(Float)
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    hotel = relationship("Hotel", back_populates="rooms")
    bookings = relationship("Booking", back_populates="room")

class Guest(Base):
    __tablename__ = 'guests'
    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    address_id = Column(Integer, ForeignKey('addresses.id'))
    address = relationship("Address")
    bookings = relationship("Booking", back_populates="guest")

class RegisteredGuest(Guest):
    __tablename__ = 'registered_guests'
    guest_id = Column(Integer, ForeignKey('guests.id'), primary_key=True)
    login_id = Column(Integer, ForeignKey('logins.id'))
    login = relationship("Login", back_populates="registered_guest")

class Login(Base):
    __tablename__ = 'logins'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="logins")
    registered_guest = relationship("RegisteredGuest", back_populates="login", uselist=False)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    access_level = Column(Integer)
    logins = relationship("Login", back_populates="role")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    guest_id = Column(Integer, ForeignKey('guests.id'))
    number_of_guests = Column(Integer)
    start_date = Column(Date)
    end_date = Column(Date)
    comment = Column(String)
    room = relationship("Room", back_populates="bookings")
    guest = relationship("Guest", back_populates="bookings")

def create_database():
    engine = create_engine('sqlite:///hotel.db')  # Hier kannst du deine Datenbank-URL konfigurieren
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    create_database()
(room={self.room!r}, guest={self.guest!r}, start_date={self.start_date!r}, end_date={self.end_date!r}, comment={self.comment!r})"
