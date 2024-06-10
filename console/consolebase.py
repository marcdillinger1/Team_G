# console/consolebase.py
from business.BaseManager import BaseManager
from business.SearchManager import SearchManager
from business.UserManager import UserManager
from business.BookingManager import BookingManager
from business.AdminManager import AdminManager

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
                print("1. Search Hotels\n2. View Booking History\n3. Logout")
                if self.current_user.email == 'admin@hotel.com':  # Example admin check
                    print("4. Admin Menu")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.search_hotels()
                elif choice == '2':
                    self.view_booking_history()
                elif choice == '3':
                    self.current_user = None
                elif choice == '4' and self.current_user.email == 'admin@hotel.com':
                    self.admin_menu()
                else:
                    print("Invalid choice!")
            else:
                print("1. Register\n2. Login\n3. Search Hotels as Guest")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.search_hotels()
                else:
                    print("Invalid choice!")

    # User Story 1.6: Register user
    def register(self):
        email = input("Email: ")
        password = input("Password: ")
        try:
            self.current_user = self.user_manager.register_user(email, password)
            self.base_manager.save_all()
            print("Registration successful!")
        except ValueError as e:
            print(f"Error: {e}")

    # User Story 2.1: Login user
    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        try:
            self.current_user = self.user_manager.login_user(email, password)
            print("Login successful!")
        except ValueError as e:
            print(f"Error: {e}")

    # User Story 1.1: Search hotels as guest
    def search_hotels(self):
        city = input("Enter city: ")
        hotels = self.search_manager.search_by_city(city)
        if hotels:
            print(f"Hotels in {city}:")
            for hotel in hotels:
                print(f"{hotel.name} - {hotel.address} - {hotel.stars} stars")
        else:
            print("No hotels found.")

    # User Story 2.1.1: View booking history
    def view_booking_history(self):
        bookings = self.booking_manager.get_user_bookings(self.current_user.user_id)
        if bookings:
            print("Your bookings:")
            for booking in bookings:
                print(f"Booking ID: {booking.booking_id}, Hotel ID: {booking.hotel_id}, Room ID: {booking.room_id}, Dates: {booking.start_date} to {booking.end_date}")
        else:
            print("No bookings found.")

    # Admin menu to manage hotels and rooms
    def admin_menu(self):
        print("Admin Menu")
        print("1. Add Hotel\n2. Remove Hotel\n3. Update Hotel\n4. Add Room\n5. Remove Room")
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
        else:
            print("Invalid choice!")

    # User Story 3.1.1: Add hotel
    def add_hotel(self):
        name = input("Hotel name: ")
        address = input("Address: ")
        city = input("City: ")
        stars = int(input("Stars: "))
        self.admin_manager.add_hotel(name, address, city, stars)
        self.base_manager.save_all()
        print("Hotel added successfully!")

    # User Story 3.1.2: Remove hotel
    def remove_hotel(self):
        hotel_id = int(input("Hotel ID to remove: "))
        self.admin_manager.remove_hotel(hotel_id)
        self.base_manager.save_all()
        print("Hotel removed successfully!")

    # User Story 3.1.3: Update hotel
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

    # Admin can add room to hotel
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

    # Admin can remove room from hotel
    def remove_room(self):
        hotel_id = int(input("Hotel ID: "))
        room_id = int(input("Room ID to remove: "))
        self.admin_manager.remove_room_from_hotel(hotel_id, room_id)
        self.base_manager.save_all()
        print("Room removed successfully!")
