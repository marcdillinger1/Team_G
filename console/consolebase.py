# console/consolebase.py
from business.base_manager import BaseManager
from business.search_manager import SearchManager
from business.user_manager import UserManager
from business.booking_manager import BookingManager
from business.admin_manager import AdminManager
from datetime import datetime

class ConsoleApp:
    def __init__(self):
        self.base_manager = BaseManager()
        self.search_manager = SearchManager(self.base_manager.hotels)
        self.user_manager = UserManager(self.base_manager.users)
        self.booking_manager = BookingManager(self.base_manager.bookings, self.base_manager.users, self.base_manager.hotels)
        self.admin_manager = AdminManager(self.base_manager.hotels)
        self.current_user = None

    def run(self):
        while True:
            print("\nHotel Reservations System")
            if self.current_user:
                print(f"Logged in as: {self.current_user.email}")
                print("1. Search Hotels")
                print("2. View Booking History")
                print("3. Make a Booking")
                print("4. Cancel a Booking")
                print("5. Logout")
                if self.current_user.email == 'admin@hotel.com':  # Example admin check
                    print("6. Admin Menu")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.search_hotels()
                elif choice == '2':
                    self.view_booking_history()
                elif choice == '3':
                    self.make_booking()
                elif choice == '4':
                    self.cancel_booking()
                elif choice == '5':
                    self.current_user = None
                elif choice == '6' and self.current_user.email == 'admin@hotel.com':
                    self.admin_menu()
                else:
                    print("Invalid choice!")
            else:
                print("1. Register")
                print("2. Login")
                print("3. Search Hotels as Guest")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.search_hotels_as_guest()
                else:
                    print("Invalid choice!")

    def register(self):
        email = input("Email: ")
        password = input("Password: ")
        try:
            self.current_user = self.user_manager.register_user(email, password)
            self.base_manager.save_all()
            print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        try:
            self.current_user = self.user_manager.login_user(email, password)
            print("Login successful!")
        except ValueError as e:
            print(f"Error: {e}")

    def search_hotels_as_guest(self):
        while True:
            print("\nSearch Options")
            print("1. Search by City")
            print("2. Search by City and Stars")
            print("3. Search by City and Guests")
            print("4. Search by City, Guests, and Availability")
            print("5. Back to Main Menu")
            choice = input("Choose an option: ")
            if choice == '1':
                self.search_by_city()
            elif choice == '2':
                self.search_by_city_and_stars()
            elif choice == '3':
                self.search_by_city_and_guests()
            elif choice == '4':
                self.search_by_city_guests_and_availability()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")

    def search_by_city(self):
        city = input("Enter city: ")
        hotels = self.search_manager.search_by_city(city)
        if hotels:
            print(f"Hotels in {city}:")
            for hotel in hotels:
                print(f"{hotel.name} - {hotel.address} - {hotel.stars} stars")
                self.view_hotel_details(hotel.hotel_id)
        else:
            print("No hotels found.")

    def search_by_city_and_stars(self):
        city = input("Enter city: ")
        stars = int(input("Enter number of stars: "))
        hotels = self.search_manager.search_by_stars(city, stars)
        if hotels:
            print(f"Hotels in {city} with {stars} stars:")
            for hotel in hotels:
                print(f"{hotel.name} - {hotel.address} - {hotel.stars} stars")
                self.view_hotel_details(hotel.hotel_id)
        else:
            print("No hotels found.")

    def search_by_city_and_guests(self):
        city = input("Enter city: ")
        guests = int(input("Enter number of guests: "))
        hotels = self.search_manager.search_by_guests(city, guests)
        if hotels:
            print(f"Hotels in {city} with rooms for {guests} guests:")
            for hotel in hotels:
                print(f"{hotel.name} - {hotel.address} - {hotel.stars} stars")
                self.view_hotel_details(hotel.hotel_id)
        else:
            print("No hotels found.")

    def search_by_city_guests_and_availability(self):
        city = input("Enter city: ")
        guests = int(input("Enter number of guests: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        hotels = self.search_manager.search_by_availability(city, guests, start_date, end_date)
        if hotels:
            print(f"Hotels in {city} with rooms for {guests} guests from {start_date} to {end_date}:")
            for hotel in hotels:
                print(f"{hotel.name} - {hotel.address} - {hotel.stars} stars")
                self.view_hotel_details(hotel.hotel_id)
        else:
            print("No hotels found.")

    def view_hotel_details(self, hotel_id):
        hotel = next((hotel for hotel in self.base_manager.hotels if hotel.hotel_id == hotel_id), None)
        if hotel:
            print(f"Hotel Name: {hotel.name}")
            print(f"Address: {hotel.address}")
            print(f"Stars: {hotel.stars}")
            print("Rooms:")
            for room in hotel.rooms:
                if isinstance(room, dict):
                    print(f"Room ID: {room['room_id']}, Type: {room['room_type']}, Max Guests: {room['max_guests']}, Description: {room['description']}, Price per Night: {room['price_per_night']}, Amenities: {', '.join(room['amenities'])}")
                else:
                    print(f"Room ID: {room.room_id}, Type: {room.room_type}, Max Guests: {room.max_guests}, Description: {room.description}, Price per Night: {room.price_per_night}, Amenities: {', '.join(room.amenities)}")
        else:
            print("Hotel not found.")

    def make_booking(self):
        city = input("Enter city: ")
        hotels = self.search_manager.search_by_city(city)
        if not hotels:
            print("No hotels found.")
            return

        print("Available hotels:")
        for hotel in hotels:
            print(f"{hotel.hotel_id}. {hotel.name} - {hotel.address} - {hotel.stars} stars")

        hotel_id = int(input("Enter hotel ID to book: "))
        hotel = next((hotel for hotel in hotels if hotel.hotel_id == hotel_id), None)
        if not hotel:
            print("Invalid hotel ID.")
            return

        print("Available rooms:")
        for room in hotel.rooms:
            if isinstance(room, dict):
                print(f"Room ID: {room['room_id']}, Type: {room['room_type']}, Price per night: {room['price_per_night']}, Max guests: {room['max_guests']}")
            else:
                print(f"Room ID: {room.room_id}, Type: {room.room_type}, Price per night: {room.price_per_night}, Max guests: {room.max_guests}")

        room_id = int(input("Enter room ID to book: "))
        room = next((room for room in hotel.rooms if room['room_id'] == room_id), None)
        if not room:
            print("Invalid room ID.")
            return

        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        total_price = room['price_per_night'] * (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
        booking = self.booking_manager.create_booking(self.current_user.user_id, room_id, hotel_id, start_date, end_date, total_price)
        self.base_manager.save_all()
        print(f"Booking successful! Booking ID: {booking.booking_id}")

    def cancel_booking(self):
        booking_id = int(input("Enter booking ID to cancel: "))
        try:
            self.booking_manager.cancel_booking(booking_id)
            self.base_manager.save_all()
            print("Booking cancelled successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def view_booking_history(self):
        bookings = self.booking_manager.get_user_bookings(self.current_user.user_id)
        if bookings:
            print("Your bookings:")
            for booking in bookings:
                print(f"Booking ID: {booking.booking_id}, Hotel ID: {booking.hotel_id}, Room ID: {booking.room_id}, Dates: {booking.start_date} to {booking.end_date}")
        else:
            print("No bookings found.")

    def admin_menu(self):
        print("Admin Menu")
        print("1. Add Hotel")
        print("2. Remove Hotel")
        print("3. Update Hotel")
        print("4. Add Room")
        print("5. Remove Room")
        print("6. View All Bookings")
        choice = input("Choose an option: ")
        if choice == '1':
            self.add_hotel()
        elif choice == '2':
            self.remove_hotel()
        elif choice == '3':
            self.update_hotel()
        elif choice == '4':
            self.add_room()
        elif choice == '5':
            self.remove_room()
        elif choice == '6':
            self.view_all_bookings()
        else:
            print("Invalid choice!")

    def add_hotel(self):
        name = input("Hotel name: ")
        address = input("Address: ")
        city = input("City: ")
        stars = int(input("Stars: "))
        self.admin_manager.add_hotel(name, address, city, stars)
        self.base_manager.save_all()
        print("Hotel added successfully!")

    def remove_hotel(self):
        hotel_id = int(input("Hotel ID to remove: "))
        self.admin_manager.remove_hotel(hotel_id)
        self.base_manager.save_all()
        print("Hotel removed successfully!")

    def update_hotel(self):
        hotel_id = int(input("Hotel ID to update: "))
        name = input("New name (leave blank to skip): ")
        address = input("New address (leave blank to skip): ")
        city = input("New city (leave blank to skip): ")
        stars = input("New stars (leave blank to skip): ")
        stars = int(stars) if stars else None
        self.admin_manager.update_hotel(hotel_id, name, address, city, stars)
        self.base_manager.save_all()
        print("Hotel updated successfully!")

    def add_room(self):
        hotel_id = int(input("Hotel ID: "))
        room_type = input("Room type: ")
        max_guests = int(input("Max guests: "))
        description = input("Description: ")
        amenities = input("Amenities (comma separated): ").split(',')
        price_per_night = float(input("Price per night: "))
        self.admin_manager.add_room_to_hotel(hotel_id, room_type, max_guests, description, amenities, price_per_night)
        self.base_manager.save_all()
        print("Room added successfully!")

    def remove_room(self):
        hotel_id = int(input("Hotel ID: "))
        room_id = int(input("Room ID to remove: "))
        self.admin_manager.remove_room_from_hotel(hotel_id, room_id)
        self.base_manager.save_all()
        print("Room removed successfully!")

    def view_all_bookings(self):
        bookings = self.booking_manager.get_all_bookings()
        if bookings:
            print("All bookings:")
            for booking in bookings:
                print(f"Booking ID: {booking.booking_id}, User ID: {booking.user_id}, Hotel ID: {booking.hotel_id}, Room ID: {booking.room_id}, Dates: {booking.start_date} to {booking.end_date}, Total Price: {booking.total_price}")
        else:
            print("No bookings found.")
