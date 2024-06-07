from sqlalchemy.orm import Session
from models import Room, Booking, User
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from database import SessionLocal, engine
import hashlib
from datetime import datetime

app = FastAPI()

class RoomDetails(BaseModel):
    room_type: str
    max_guests: int
    description: str
    price_per_night: float
    amenities: str

class BookingRequest(BaseModel):
    room_id: int
    guest_name: str
    guest_email: str
    check_in: str
    check_out: str

class UserRegistration(BaseModel):
    email: str
    password: str

# Abhängigkeit, um die DB-Sitzung zu erhalten
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User Story 1.2: Details zu verschiedenen Zimmertypen anzeigen
@app.get("/rooms/{hotel_id}", response_model=List[RoomDetails])
def get_rooms(hotel_id: int, db: Session = Depends(get_db)):
    # User Story 1.2.2: Nur verfügbare Zimmer anzeigen
    rooms = db.query(Room).filter(Room.hotel_id == hotel_id, Room.available == True).all()
    # User Story 1.2.1: Zimmerinformationen anzeigen
    return [
        {
            "room_type": room.room_type,
            "max_guests": room.max_guests,
            "description": room.description,
            "price_per_night": room.price_per_night,
            "amenities": room.amenities
        }
        for room in rooms
    ]

# User Story 1.3: Zimmer buchen
# User Story 1.4: Minimale Informationen für Buchung
@app.post("/book")
def book_room(request: BookingRequest, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == request.room_id, Room.available == True).first()
    if not room:
        raise HTTPException(status_code=404, detail="Zimmer nicht verfügbar")
    check_in_date = datetime.strptime(request.check_in, '%Y-%m-%d')
    check_out_date = datetime.strptime(request.check_out, '%Y-%m-%d')
    total_price = (check_out_date - check_in_date).days * room.price_per_night
    booking = Booking(
        room_id=request.room_id,
        guest_name=request.guest_name,
        guest_email=request.guest_email,
        check_in=check_in_date,
        check_out=check_out_date,
        total_price=total_price
    )
    room.available = False
    db.add(booking)
    db.commit()
    return {"message": "Buchung erfolgreich", "booking_id": booking.id}

# User Story 1.5: Buchungsdetails anzeigen und speichern
@app.get("/reservation/{booking_id}")
def get_reservation(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Buchung nicht gefunden")
    return {
        "guest_name": booking.guest_name,
        "guest_email": booking.guest_email,
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "total_price": booking.total_price
    }

# User Story 1.6: Benutzerregistrierung
@app.post("/register")
def register_user(request: UserRegistration, db: Session = Depends(get_db)):
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
    user = User(email=request.email, password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "Benutzer erfolgreich registriert"}