# business/BookingManager.py

from models import Booking
from datetime import datetime
from typing import List
import json


class BookingManager:
    def __init__(self, bookings: List[Booking], users, hotels):
        self.bookings = bookings
        self.users = users
        self.hotels = hotels

    def create_booking(self, user_id: int, room_id: int, hotel_id: int, start_date: str, end_date: str) -> Booking:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        total_price = self.calculate_total_price(room_id, start_date_dt, end_date_dt)

        booking = Booking(
            booking_id=len(self.bookings) + 1,
            user_id=user_id,
            room_id=room_id,
            hotel_id=hotel_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price
        )
        self.bookings.append(booking)
        self.save_booking_to_file(booking)
        return booking

    def calculate_total_price(self, room_id: int, start_date: datetime, end_date: datetime) -> float:
        room = next(room for hotel in self.hotels for room in hotel.rooms if room.room_id == room_id)
        return room.price_per_night * (end_date - start_date).days

    def save_booking_to_file(self, booking: Booking):
        try:
            hotel = next(hotel for hotel in self.hotels if hotel.hotel_id == booking.hotel_id)
            room = next(room for room in hotel.rooms if room.room_id == booking.room_id)
        except StopIteration:
            print(f"Error: Hotel ID {booking.hotel_id} or Room ID {booking.room_id} not found.")
            return

        booking_details = {
            "booking_id": booking.booking_id,
            "user_id": booking.user_id,
            "room_id": booking.room_id,
            "hotel_id": booking.hotel_id,
            "hotel_name": hotel.name,
            "hotel_address": hotel.address,
            "hotel_city": hotel.city,  # Hinzufügen der Stadt/Ort des Hotels
            "room_type": room.room_type,
            "room_description": room.description,
            "room_amenities": room.amenities,
            "max_guests": room.max_guests,
            "price_per_night": room.price_per_night,  # Hinzufügen des Preises pro Nacht
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "total_price": booking.total_price
        }

        with open(f"booking_{booking.booking_id}.json", 'w') as file:
            json.dump(booking_details, file, indent=4)

    def get_bookings_by_user(self, user_id: int) -> List[Booking]:
        return [booking for booking in self.bookings if booking.user_id == user_id]

    def cancel_booking(self, booking_id: int) -> bool:
        booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
        if booking:
            self.bookings.remove(booking)
            return True
        return False

    def get_all_bookings(self) -> List[Booking]:
        return self.bookings
