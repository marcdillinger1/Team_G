# business/AdminManager.py
from models import Hotel, Room

class AdminManager:
    def __init__(self, hotels):
        self.hotels = hotels

    # User Story 3.1.1: Add new hotel to the system
    def add_hotel(self, name: str, address: str, city: str, stars: int) -> Hotel:
        hotel_id = len(self.hotels) + 1
        new_hotel = Hotel(hotel_id=hotel_id, name=name, address=address, city=city, stars=stars, rooms=[])
        self.hotels.append(new_hotel)
        return new_hotel

    # User Story 3.1.2: Remove hotel from the system
    def remove_hotel(self, hotel_id: int):
        hotel = next(hotel for hotel in self.hotels if hotel.hotel_id == hotel_id)
        self.hotels.remove(hotel)

    # User Story 3.1.3: Update hotel information
    def update_hotel(self, hotel_id: int, name: str = None, address: str = None, city: str = None, stars: int = None):
        hotel = next(hotel for hotel in self.hotels if hotel.hotel_id == hotel_id)
        if name:
            hotel.name = name
        if address:
            hotel.address = address
        if city:
            hotel.city = city
        if stars:
            hotel.stars = stars

    # Optional: Manage room availability and real-time price updates
    def add_room_to_hotel(self, hotel_id: int, room_type: str, max_guests: int, description: str, amenities: list, price_per_night: float):
        hotel = next(hotel for hotel in self.hotels if hotel.hotel_id == hotel_id)
        room_id = len(hotel.rooms) + 1
        new_room = Room(room_id=room_id, hotel_id=hotel_id, room_type=room_type, max_guests=max_guests, description=description, amenities=amenities, price_per_night=price_per_night, availability=[])
        hotel.rooms.append(new_room)

    def remove_room_from_hotel(self, hotel_id: int, room_id: int):
        hotel = next(hotel for hotel in self.hotels if hotel.hotel_id == hotel_id)
        room = next(room for room in hotel.rooms if room.room_id == room_id)
        hotel.rooms.remove(room)
