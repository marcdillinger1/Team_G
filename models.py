from dataclasses import dataclass, field
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

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "hotel_id": self.hotel_id,
            "room_type": self.room_type,
            "max_guests": self.max_guests,
            "description": self.description,
            "amenities": self.amenities,
            "price_per_night": self.price_per_night,
            "availability": self.availability
        }

@dataclass
class Hotel:
    hotel_id: int
    name: str
    address: str
    city: str
    stars: int
    rooms: List[Room] = field(default_factory=list)

    def __post_init__(self):
        self.rooms = [Room(**room) if isinstance(room, dict) else room for room in self.rooms]

    def to_dict(self):
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "stars": self.stars,
            "rooms": [room.to_dict() for room in self.rooms]
        }

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
