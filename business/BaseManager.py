# business/BaseManager.py
import json
from data_access.data_loader import DataLoader
from models import Hotel, User, Booking

class BaseManager:
    def __init__(self):
        try:
            self.hotels = DataLoader.load_hotels('data/hotels.json')
            self.users = DataLoader.load_users('data/users.json')
            self.bookings = DataLoader.load_bookings('data/bookings.json')
        except json.JSONDecodeError as e:
            print(f"Error loading data: {e}")
            self.hotels = []
            self.users = []
            self.bookings = []
        except FileNotFoundError as e:
            print(f"Error: File not found: {e}")
            self.hotels = []
            self.users = []
            self.bookings = []
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.hotels = []
            self.users = []
            self.bookings = []

    def save_all(self):
        try:
            DataLoader.save_hotels(self.hotels, 'data/hotels.json')
            DataLoader.save_users(self.users, 'data/users.json')
            DataLoader.save_bookings(self.bookings, 'data/bookings.json')
        except Exception as e:
            print(f"Error saving data: {e}")
