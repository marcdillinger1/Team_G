# business/BaseManager.py

import json
from data_access.data_loader import DataLoader

class BaseManager:
    def __init__(self):
        self.hotels = DataLoader.load_hotels('data/hotels.json')
        self.users = DataLoader.load_users('data/users.json')
        self.bookings = DataLoader.load_bookings('data/bookings.json')

    def save_all(self):
        try:
            DataLoader.save_hotels(self.hotels, 'data/hotels.json')
            DataLoader.save_users(self.users, 'data/users.json')
            DataLoader.save_bookings(self.bookings, 'data/bookings.json')
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
