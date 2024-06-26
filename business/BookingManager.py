import json
from datetime import datetime

class BookingManager:  # Initialize the manager with paths to booking, user, and hotel data files.
    def __init__(self, bookings_file, users_file, hotels_file):
        self.bookings_file = bookings_file
        self.users_file = users_file
        self.hotels_file = hotels_file
        self.bookings = self.load_bookings()
        self.users = self.load_users()
        self.hotels = self.load_hotels()

    def load_bookings(self): # Load bookings from JSON file.
        with open(self.bookings_file, 'r') as file:
            return json.load(file)

    def save_bookings(self):  # Save bookings to JSON file.
        with open(self.bookings_file, 'w') as file:
            json.dump(self.bookings, file, indent=4)

    def load_users(self): # Load user data from JSON file.
        with open(self.users_file, 'r') as file:
            return json.load(file)

    def load_hotels(self): # Load hotel data from JSON file and map it by hotel ID.
        with open(self.hotels_file, 'r') as file:
            hotels = json.load(file)
            return {hotel['hotel_id']: hotel for hotel in hotels}

    def get_bookings_by_user(self, user_id): # Return bookings made by a specific user.
        return [b for b in self.bookings if b['user_id'] == user_id]

    def calculate_price(self, hotel_id, room_id, start_date, end_date): # Calculate the price of a stay given hotel and room IDs and dates.
        hotel = self.hotels.get(int(hotel_id))
        if not hotel:
            return 0
        room = next((r for r in hotel['rooms'] if r['room_id'] == int(room_id)), None)
        if not room:
            return 0
        days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
        return days * room['price_per_night']

    def make_booking(self, user_id, hotel_id, room_id, start_date, end_date, total_price):   # Record a new booking in the system.
        booking_id = len(self.bookings) + 1
        booking = {
            'booking_id': booking_id,
            'user_id': user_id,
            'hotel_id': hotel_id,
            'room_id': room_id,
            'start_date': start_date,
            'end_date': end_date,
            'total_price': total_price
        }
        self.bookings.append(booking)
        self.save_bookings()
        return booking

    def make_booking_as_guest(self, hotel_id, room_id, start_date, end_date, total_price): # Create a booking without requiring a registered user.
        booking_id = len(self.bookings) + 1
        booking = {
            'booking_id': booking_id,
            'user_id': None,
            'hotel_id': hotel_id,
            'room_id': room_id,
            'start_date': start_date,
            'end_date': end_date,
            'total_price': total_price
        }
        self.bookings.append(booking)
        self.save_bookings()
        self.generate_booking_confirmation(booking)
        return booking

    def generate_booking_confirmation(self, booking): # Generate a booking confirmation file.
        confirmation_file = f"booking_confirmation_{booking['booking_id']}.json"
        with open(confirmation_file, 'w') as file:
            json.dump(booking, file, indent=4)

    def update_booking(self, booking_id, start_date, end_date):   # Update existing booking dates.
        booking = next((b for b in self.bookings if b['booking_id'] == booking_id), None)
        if not booking:
            return False
        booking['start_date'] = start_date
        booking['end_date'] = end_date
        self.save_bookings()
        return True

    def cancel_booking(self, booking_id):  # Remove a booking from the system.
        booking = next((b for b in self.bookings if b['booking_id'] == booking_id), None)
        if not booking:
            return False
        self.bookings.remove(booking)
        self.save_bookings()
        return True

    def is_room_available(self, hotel_id, room_id, start_date, end_date):  # Check if a room is available during a specific period.
        for booking in self.bookings:
            if booking['hotel_id'] == hotel_id and booking['room_id'] == room_id and (
                (start_date >= booking['start_date'] and start_date <= booking['end_date']) or
                (end_date >= booking['start_date'] and end_date <= booking['end_date'])
            ):
                return False
        return True
