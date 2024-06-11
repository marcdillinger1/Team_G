# business/SearchManager.py

from models import Hotel, Room
from datetime import datetime
from typing import List

class SearchManager:
    def __init__(self, hotels: List[Hotel]):
        self.hotels = hotels

    def search_by_city(self, city: str) -> List[Hotel]:
        return [hotel for hotel in self.hotels if hotel.city.lower() == city.lower()]

    def search_by_city_and_stars(self, city: str, stars: int) -> List[Hotel]:
        return [hotel for hotel in self.search_by_city(city) if hotel.stars == stars]

    def search_by_city_and_guests(self, city: str, guests: int) -> List[Hotel]:
        return [
            hotel for hotel in self.search_by_city(city)
            if any(room.max_guests >= guests for room in hotel.rooms)
        ]

    def search_by_city_dates_and_guests(self, city: str, guests: int, start_date: str, end_date: str, stars: int = None) -> List[Hotel]:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if stars:
            hotels = self.search_by_city_and_stars(city, stars)
        else:
            hotels = self.search_by_city(city)

        def room_available(room: Room) -> bool:
            for booking in room.bookings:
                booked_start = datetime.strptime(booking['start_date'], "%Y-%m-%d")
                booked_end = datetime.strptime(booking['end_date'], "%Y-%m-%d")
                if not (end_date < booked_start or start_date > booked_end):
                    return False
            return True

        return [
            hotel for hotel in hotels
            if any(room_available(room) and room.max_guests >= guests for room in hotel.rooms)
        ]

    def get_hotel_details(self, hotel_id: int) -> Hotel:
        for hotel in self.hotels:
            if hotel.hotel_id == hotel_id:
                return hotel
        return None
