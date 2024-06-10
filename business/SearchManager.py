# business/SearchManager.py
from models import Hotel, Room

class SearchManager:
    def __init__(self, hotels):
        self.hotels = hotels

    # User Story 1.1.1: Search hotels by city
    def search_by_city(self, city: str):
        return [hotel for hotel in self.hotels if hotel.city.lower() == city.lower()]

    # User Story 1.1.2: Search hotels by city and stars
    def search_by_stars(self, city: str, stars: int):
        return [hotel for hotel in self.hotels if hotel.city.lower() == city.lower() and hotel.stars == stars]

    # User Story 1.1.3: Search hotels by city and number of guests
    def search_by_guests(self, city: str, guests: int):
        return [
            hotel for hotel in self.hotels
            if hotel.city.lower() == city.lower() and any(room.max_guests >= guests for room in hotel.rooms)
        ]

    # User Story 1.1.4: Search hotels by city, number of guests, and availability
    def search_by_availability(self, city: str, guests: int, start_date: str, end_date: str):
        available_hotels = []
        for hotel in self.hotels:
            if hotel.city.lower() != city.lower():
                continue
            available_rooms = [
                room for room in hotel.rooms
                if room.max_guests >= guests and all(date not in room.availability for date in self._daterange(start_date, end_date))
            ]
            if available_rooms:
                available_hotels.append(hotel)
        return available_hotels

    @staticmethod
    def _daterange(start_date: str, end_date: str):
        from datetime import datetime, timedelta
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
