# business/AdminManager.py

from models import Hotel, Room, Booking
import json

class AdminManager:
    def __init__(self, hotels):
        self.hotels = hotels

    def add_hotel(self, hotel: Hotel):
        self.hotels.append(hotel)
        self.save_hotels()
        print(f"Hotel '{hotel.name}' wurde hinzugefügt.")

    def remove_hotel(self, hotel_id: int):
        self.hotels = [hotel for hotel in self.hotels if hotel.hotel_id != hotel_id]
        self.save_hotels()
        print(f"Hotel mit ID {hotel_id} wurde entfernt.")

    def update_hotel(self, hotel_id: int, name: str = None, stars: int = None, city: str = None):
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                if name:
                    hotel.name = name
                if stars:
                    hotel.stars = stars
                if city:
                    hotel.city = city
                self.save_hotels()
                print(f"Hotel mit ID {hotel_id} wurde aktualisiert.")
                return
        print(f"Hotel mit ID {hotel_id} nicht gefunden.")

    def add_room_to_hotel(self, hotel_id: int, room: Room):
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                hotel.rooms.append(room)
                self.save_hotels()
                print(f"Zimmer mit ID {room.room_id} wurde zu Hotel mit ID {hotel_id} hinzugefügt.")
                return
        print(f"Hotel mit ID {hotel_id} nicht gefunden.")

    def view_all_bookings(self, bookings: list[Booking]):
        for booking in bookings:
            print(booking)

    def update_booking(self, bookings: list[Booking], booking_id: int, phone: str = None):
        for booking in bookings:
            if booking.booking_id == booking_id:
                if phone:
                    booking.phone = phone
                print(f"Buchung mit ID {booking_id} wurde aktualisiert.")
                return
        print(f"Buchung mit ID {booking_id} nicht gefunden.")

    def update_room_availability_and_price(self, hotel_id: int, room_id: int, availability: list[str] = None, price_per_night: float = None):
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                for room in hotel.rooms:
                    if room.room_id == room_id:
                        if availability is not None:
                            room.availability = availability
                        if price_per_night is not None:
                            room.price_per_night = price_per_night
                        self.save_hotels()
                        print(f"Zimmer mit ID {room_id} im Hotel mit ID {hotel_id} wurde aktualisiert.")
                        return
        print(f"Zimmer mit ID {room_id} im Hotel mit ID {hotel_id} nicht gefunden.")

    def save_hotels(self):
        with open('data/hotels.json', 'w') as f:
            json.dump([hotel.to_dict() for hotel in self.hotels], f, indent=4)
