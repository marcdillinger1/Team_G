# business/BookingManager.py

from models import Booking, User, Hotel, Room
from datetime import datetime
from typing import List

class BookingManager:
    def __init__(self, bookings: List[Booking], users: List[User], hotels: List[Hotel]):
        self.bookings = bookings
        self.users = users
        self.hotels = hotels

    def create_booking(self, user_id: int, room_id: int, hotel_id: int, start_date: str, end_date: str) -> Booking:
        booking_id = max(booking.booking_id for booking in self.bookings) + 1 if self.bookings else 1
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        room = self.get_room(hotel_id, room_id)

        if not self.is_room_available(room, start_date, end_date):
            raise ValueError("Room is not available for the selected dates.")

        total_price = (end_date - start_date).days * room.price_per_night
        new_booking = Booking(booking_id, user_id, room_id, hotel_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), total_price)
        self.bookings.append(new_booking)
        return new_booking

    def get_room(self, hotel_id: int, room_id: int) -> Room:
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                for room in hotel.rooms:
                    if room.room_id == room_id:
                        return room
        return None

    def is_room_available(self, room: Room, start_date: datetime, end_date: datetime) -> bool:
        for booking in self.bookings:
            if booking.room_id == room.room_id:
                booked_start = datetime.strptime(booking.start_date, "%Y-%m-%d")
                booked_end = datetime.strptime(booking.end_date, "%Y-%m-%d")
                if not (end_date <= booked_start or start_date >= booked_end):
                    return False
        return True

    def get_bookings_by_user(self, user_id: int) -> List[Booking]:
        return [booking for booking in self.bookings if booking.user_id == user_id]

    def cancel_booking(self, booking_id: int) -> bool:
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                self.bookings.remove(booking)
                return True
        return False

    def get_all_bookings(self) -> List[Booking]:
        return self.bookings
