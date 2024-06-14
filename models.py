class Hotel:
    def __init__(self, hotel_id, name, address, city, stars, rooms): # Initialisiert ein Hotel-Objekt mit den gegebenen Attributen
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.city = city
        self.stars = stars
        self.rooms = rooms

    def to_dict(self): # Wandelt das Hotel-Objekt in ein Dictionary um, inklusive der Zimmer
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'stars': self.stars,
            'rooms': [room.to_dict() for room in self.rooms]
        }

class Room:
    def __init__(self, room_id, hotel_id, room_type, max_guests, description, amenities, price_per_night, availability): # Initialisiert ein Zimmer-Objekt mit den gegebenen Attributen
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.room_type = room_type
        self.max_guests = max_guests
        self.description = description
        self.amenities = amenities
        self.price_per_night = price_per_night
        self.availability = availability

    def to_dict(self): # Wandelt das Zimmer-Objekt in ein Dictionary um
        return {
            'room_id': self.room_id,
            'hotel_id': self.hotel_id,
            'room_type': self.room_type,
            'max_guests': self.max_guests,
            'description': self.description,
            'amenities': self.amenities,
            'price_per_night': self.price_per_night,
            'availability': self.availability
        }

class Booking:
    def __init__(self, booking_id, user_id, room_id, hotel_id, start_date, end_date, total_price): # Initialisiert ein Buchungs-Objekt mit den gegebenen Attributen
        self.booking_id = booking_id
        self.user_id = user_id
        self.room_id = room_id
        self.hotel_id = hotel_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_price = total_price

    def to_dict(self): # Wandelt das Buchungs-Objekt in ein Dictionary um
        return {
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'room_id': self.room_id,
            'hotel_id': self.hotel_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_price': self.total_price
        }

class User:
    def __init__(self, user_id, email, password, booking_history): # Initialisiert ein Benutzer-Objekt mit den gegebenen Attributen
        self.user_id = user_id
        self.email = email
        self.password = password
        self.booking_history = booking_history

    def to_dict(self): # Wandelt das Benutzer-Objekt in ein Dictionary um
        return {
            'user_id': self.user_id,
            'email': self.email,
            'password': self.password,
            'booking_history': self.booking_history
        }
