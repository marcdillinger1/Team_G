import json

class AdminManager:
    def __init__(self, hotels_file, bookings_file):  # Constructor initializes the AdminManager with paths to the hotel and bookings files.
        self.hotels_file = hotels_file
        self.bookings_file = bookings_file
        self.hotels = self.load_hotels()  # Load hotels from file upon initialization.

    def load_hotels(self):    # Load hotels data from a JSON file.
        with open(self.hotels_file, 'r') as file:
            return json.load(file)

    def save_hotels(self):   # Save the current state of hotels data back to the JSON file.
        with open(self.hotels_file, 'w') as file:
            json.dump(self.hotels, file, indent=4)

    def add_hotel(self):    # Add a new hotel by collecting hotel information interactively.
        hotel_id = len(self.hotels) + 1
        name = input("Enter hotel name: ")
        address = input("Enter hotel address: ")
        city = input("Enter hotel city: ")
        stars = int(input("Enter number of stars: "))
        rooms = []
        while True:
            add_room = input("Add a room? (yes/no): ")
            if add_room.lower() != 'yes':
                break
            room_id = len(rooms) + 1
            room_type = input("Enter room type: ")
            max_guests = int(input("Enter maximum guests: "))
            description = input("Enter room description: ")
            amenities = input("Enter room amenities (comma separated): ").split(", ")
            price_per_night = float(input("Enter price per night: "))
            room = {
                'room_id': room_id,
                'hotel_id': hotel_id,
                'room_type': room_type,
                'max_guests': max_guests,
                'description': description,
                'amenities': amenities,
                'price_per_night': price_per_night
            }
            rooms.append(room)
        hotel = {
            'hotel_id': hotel_id,
            'name': name,
            'address': address,
            'city': city,
            'stars': stars,
            'rooms': rooms
        }
        self.hotels.append(hotel)
        self.save_hotels()
        print("Hotel added successfully.")

    def update_hotel(self):  # Update hotel information by inputting the hotel ID and new values interactively.
        hotel_id = int(input("Enter hotel ID to update: "))
        hotel = next((h for h in self.hotels if h['hotel_id'] == hotel_id), None)
        if not hotel:
            print("Invalid hotel ID.")
            return
        name = input(f"Enter hotel name ({hotel['name']}): ")
        address = input(f"Enter hotel address ({hotel['address']}): ")
        city = input(f"Enter hotel city ({hotel['city']}): ")
        stars = input(f"Enter number of stars ({hotel['stars']}): ")
        hotel['name'] = name if name else hotel['name']
        hotel['address'] = address if address else hotel['address']
        hotel['city'] = city if city else hotel['city']
        hotel['stars'] = int(stars) if stars else hotel['stars']
        self.save_hotels()
        print("Hotel updated successfully.")

    def delete_hotel(self): # Delete a hotel by its ID.
        hotel_id = int(input("Enter hotel ID to delete: "))
        hotel = next((h for h in self.hotels if h['hotel_id'] == hotel_id), None)
        if not hotel:
            print("Invalid hotel ID.")
            return
        self.hotels.remove(hotel)
        self.save_hotels()
        print("Hotel deleted successfully.")

    def view_all_bookings(self): # Display all bookings from the bookings JSON file.
        with open(self.bookings_file, 'r') as file:
            bookings = json.load(file)
        for booking in bookings:
            print(f"Booking ID: {booking['booking_id']}, Hotel: {booking['hotel_id']}, Room: {booking['room_id']}, Dates: {booking['start_date']} to {booking['end_date']}, Total Price: {booking['total_price']}")

    def update_booking(self):  # Update a booking by changing its start and end dates.
        with open(self.bookings_file, 'r') as file:
            bookings = json.load(file)
        booking_id = int(input("Enter booking ID to update: "))
        booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
        if not booking:
            print("Invalid booking ID.")
            return
        start_date = input(f"Enter new start date ({booking['start_date']}): ")
        end_date = input(f"Enter new end date ({booking['end_date']}): ")
        booking['start_date'] = start_date if start_date else booking['start_date']
        booking['end_date'] = end_date if end_date else booking['end_date']
        with open(self.bookings_file, 'w') as file:
            json.dump(bookings, file, indent=4)
        print("Booking updated successfully.")
