# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class Room:
    room_id: int
    hotel_id: int
    room_type: str
    max_guests: int
    description: str
    amenities: List[str]
    price_per_night: float
    availability: List[str]

@dataclass
class Hotel:
    hotel_id: int
    name: str
    address: str
    city: str
    stars: int
    rooms: List[Room]

@dataclass
class User:
    user_id: int
    email: str
    password: str
    booking_history: List[int]  # list of booking IDs

@dataclass
class Booking:
    booking_id: int
    user_id: int
    room_id: int
    hotel_id: int
    start_date: str
    end_date: str
    total_price: float
