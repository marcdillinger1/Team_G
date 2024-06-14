import json

class SearchManager: # Initialize the SearchManager with hotel and booking data files.
    def __init__(self, hotels_file, bookings_file):
        self.hotels_file = hotels_file
        self.bookings_file = bookings_file
        self.hotels = self.load_hotels()
        self.bookings = self.load_bookings()

    def load_hotels(self): # Load hotel data from the specified JSON file.
        with open(self.hotels_file, 'r') as file:
            return json.load(file)

    def load_bookings(self): # Load booking data from the specified JSON file.
        with open(self.bookings_file, 'r') as file:
            return json.load(file)

    def search(self, city, stars=None, guests=None, start_date=None, end_date=None):  # Search for hotels based on city, star rating, guest capacity, and availability dates.
        results = []
        for hotel in self.hotels:
            if hotel['city'].lower() == city.lower():
                if stars and hotel['stars'] != stars:
                    continue
                available_rooms = []
                for room in hotel['rooms']:
                    if guests and room['max_guests'] < guests:
                        continue
                    if start_date and end_date and not self.is_room_available(room['hotel_id'], room['room_id'], start_date, end_date):
                        continue
                    available_rooms.append(room)
                if available_rooms:
                    results.append({
                        'hotel_id': hotel['hotel_id'],
                        'name': hotel['name'],
                        'address': hotel['address'],
                        'stars': hotel['stars'],
                        'city': hotel['city'],
                        'rooms': available_rooms
                    })
        return results

    def search_by_city(self, city): # Search for all hotels in a specified city.
        results = []
        for hotel in self.hotels:
            if hotel['city'].lower() == city.lower():
                results.append(hotel)
        return results

    def is_room_available(self, hotel_id, room_id, start_date, end_date): # Check if a specific room is available between given start and end dates.
        for booking in self.bookings:
            if booking['hotel_id'] == hotel_id and booking['room_id'] == room_id and (
                (start_date >= booking['start_date'] and start_date <= booking['end_date']) or
                (end_date >= booking['start_date'] and end_date <= booking['end_date'])
            ):
                return False
        return True
