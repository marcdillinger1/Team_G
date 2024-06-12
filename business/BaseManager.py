# business/BaseManager.py

from data_access.data_loader import DataLoader

class BaseManager:
    def __init__(self):
        self.hotels = DataLoader.load_hotels('data/hotels.json')
        self.users = DataLoader.load_users('data/users.json')
        self.bookings = DataLoader.load_bookings('data/bookings.json')
