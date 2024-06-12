# data_access/data_loader.py

import json
from models import Hotel, Room, Booking, User

class DataLoader:
    @staticmethod
    def load_hotels(file_path):
        with open(file_path, 'r') as file:
            hotels_data = json.load(file)
            hotels = []
            for hotel_data in hotels_data:
                rooms = [Room(**room_data) for room_data in hotel_data.pop('rooms')]
                hotel = Hotel(rooms=rooms, **hotel_data)
                hotels.append(hotel)
            return hotels

    @staticmethod
    def load_users(file_path):
        with open(file_path, 'r') as file:
            users_data = json.load(file)
            return [User(**user_data) for user_data in users_data]

    @staticmethod
    def load_bookings(file_path):
        with open(file_path, 'r') as file:
            bookings_data = json.load(file)
            return [Booking(**booking_data) for booking_data in bookings_data]
