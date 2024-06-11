# business/AdminManager.py

from models import Hotel, Room
from typing import List

class AdminManager:
    def __init__(self, hotels: List[Hotel]):
        self.hotels = hotels

    def add_hotel(self, name: str, address: str, city: str, stars: int):
        hotel_id = max(hotel.hotel_id for hotel in self.hotels) + 1 if self.hotels else 1
        new_hotel = Hotel(hotel_id, name, address, city, stars, [])
        self.hotels.append(new_hotel)

    def remove_hotel(self, hotel_id: int):
        self.hotels = [hotel for hotel in self.hotels if hotel.hotel_id != hotel_id]

    def update_hotel(self, hotel_id: int, name: str, address: str, city: str, stars: int):
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                if name:
                    hotel.name = name
                if address:
                    hotel.address = address
                if city:
                    hotel.city = city
                if stars is not None:
                    hotel.stars = stars

    def add_room_to_hotel(self, hotel_id: int, room_type: str, max_guests: int, description: str, amenities: List[str], price_per_night: float):
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                room_id = max(room.room_id for room in hotel.rooms) + 1 if hotel.rooms else 1
                new_room = Room(room_id, hotel_id, room_type, max_guests, description, amenities, price_per_night, [])
                hotel.rooms.append(new_room)

    def remove_room_from_hotel(self, hotel_id: int, room_id: int):
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                hotel.rooms = [room for room in hotel.rooms if room.room_id != room_id]
