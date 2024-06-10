# data_access/data_loader.py
import json
from models import Hotel, Room, User, Booking
from typing import List

class DataLoader:
    @staticmethod
    def load_hotels(file_path: str) -> List[Hotel]:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [Hotel(**hotel) for hotel in data]

    @staticmethod
    def load_users(file_path: str) -> List[User]:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [User(**user) for user in data]

    @staticmethod
    def load_bookings(file_path: str) -> List[Booking]:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return [Booking(**booking) for booking in data]

    @staticmethod
    def save_hotels(hotels: List[Hotel], file_path: str):
        with open(file_path, 'w') as file:
            json.dump([hotel.__dict__ for hotel in hotels], file, indent=4)

    @staticmethod
    def save_users(users: List[User], file_path: str):
        with open(file_path, 'w') as file:
            json.dump([user.__dict__ for user in users], file, indent=4)

    @staticmethod
    def save_bookings(bookings: List[Booking], file_path: str):
        with open(file_path, 'w') as file:
            json.dump([booking.__dict__ for booking in bookings], file, indent=4)
