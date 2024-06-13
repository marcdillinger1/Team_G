import json
import os

class BaseManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.hotels = self.load_json('hotels.json')
        self.bookings = self.load_json('bookings.json')
        self.users = self.load_json('users.json')

    def load_json(self, filename):
        with open(os.path.join(self.data_dir, filename), 'r') as file:
            return json.load(file)
