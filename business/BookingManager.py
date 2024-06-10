# business/BookingManager.py
from models import Booking

class BookingManager:
    def __init__(self, bookings, users, hotels):
        self.bookings = bookings
        self.users = users
        self.hotels = hotels

    # User Story 1.3: Create a new booking
    def create_booking(self, user_id: int, room_id: int, hotel_id: int, start_date: str, end_date: str, total_price: float) -> Booking:
        booking_id = len(self.bookings) + 1
        new_booking = Booking(
            booking_id=booking_id, user_id=user_id, room_id=room_id, hotel_id=hotel_id,
            start_date=start_date, end_date=end_date, total_price=total_price
        )
        self.bookings.append(new_booking)
        user = next(user for user in self.users if user.user_id == user_id)
        user.booking_history.append(booking_id)
        return new_booking

    # User Story 2.1.1: Get user bookings for view, update, and cancel
    def get_user_bookings(self, user_id: int):
        return [booking for booking in self.bookings if booking.user_id == user_id]

    def cancel_booking(self, booking_id: int):
        booking = next(booking for booking in self.bookings if booking.booking_id == booking_id)
        self.bookings.remove(booking)
        user = next(user for user in self.users if user.user_id == booking.user_id)
        user.booking_history.remove(booking_id)
