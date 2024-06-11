# data_access/data_loader.py

import json
from models import Hotel, User, Booking

class DataLoader:
    @staticmethod
    def load_hotels(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            hotels = []
            for hotel_data in data:
                hotel = Hotel(**hotel_data)
                hotels.append(hotel)
            return hotels

    @staticmethod
    def load_users(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            users = []
            for user_data in data:
                user = User(**user_data)
                users.append(user)
            return users

    @staticmethod
    def load_bookings(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            bookings = []
            for booking_data in data:
                booking = Booking(**booking_data)
                bookings.append(booking)
            return bookings

    @staticmethod
    def save_hotels(hotels, file_path):
        with open(file_path, 'w') as file:
            json.dump([hotel.__dict__ for hotel in hotels], file, indent=4)

    @staticmethod
    def save_users(users, file_path):
        with open(file_path, 'w') as file:
            json.dump([user.__dict__ for user in users], file, indent=4)

    @staticmethod
    def save_bookings(bookings, file_path):
        with open(file_path, 'w') as file:
            json.dump([booking.__dict__ for booking in bookings], file, indent=4, default=str)
