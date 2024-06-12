# business/BookingManager.py

from models import Booking

class BookingManager:
    def __init__(self, bookings, users, hotels):
        self.bookings = bookings
        self.users = users
        self.hotels = hotels

    def get_bookings_by_user(self, user_id):
        return [booking for booking in self.bookings if booking.user_id == user_id]

    def make_booking(self, user_id, hotel_id, room_id, start_date, end_date, total_price):
        booking_id = len(self.bookings) + 1  # Generate a new booking ID
        new_booking = Booking(booking_id, user_id, room_id, hotel_id, start_date, end_date, total_price)
        self.bookings.append(new_booking)
        return new_booking

    def update_booking(self, booking):
        for i, b in enumerate(self.bookings):
            if b.booking_id == booking.booking_id:
                self.bookings[i] = booking
                return True
        return False

    def cancel_booking(self, booking_id):
        for i, booking in enumerate(self.bookings):
            if booking.booking_id == booking_id:
                del self.bookings[i]
                return True
        return False

    def get_booking_by_id(self, booking_id):
        for booking in self.bookings:
            if booking.booking_id == booking_id:
                return booking
        return None
