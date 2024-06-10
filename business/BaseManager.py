# business/BaseManager.py
from data_access.data_loader import DataLoader
from models import Hotel, User, Booking

class BaseManager:
    def __init__(self):
        self.hotels = DataLoader.load_hotels('data/hotels.json')
        self.users = DataLoader.load_users('data/users.json')
        self.bookings = DataLoader.load_bookings('data/bookings.json')

    def save_all(self):
        DataLoader.save_hotels(self.hotels, 'data/hotels.json')
        DataLoader.save_users(self.users, 'data/users.json')
        DataLoader.save_bookings(self.bookings, 'data/bookings.json')
