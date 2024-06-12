# console/consolebase.py

from business.BaseManager import BaseManager
from business.SearchManager import SearchManager
from business.UserManager import UserManager
from business.BookingManager import BookingManager
from business.AdminManager import AdminManager
from datetime import datetime
from models import Hotel, Room, Booking

class ConsoleApp:
    def __init__(self):
        self.base_manager = BaseManager()
        self.search_manager = SearchManager(self.base_manager.hotels, self.base_manager.bookings)
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
                print("4. Update a Booking")
                print("5. Cancel a Booking")
                print("6. Logout")
                if self.user_manager.is_admin(self.current_user.email, self.current_user.password):
                    print("7. Admin Menu")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.search_hotels()
                elif choice == '2':
                    self.view_booking_history()
                elif choice == '3':
                    self.make_booking()
                elif choice == '4':
                    self.update_booking()
                elif choice == '5':
                    self.cancel_booking()
                elif choice == '6':
                    self.current_user = None
                elif choice == '7' and self.user_manager.is_admin(self.current_user.email, self.current_user.password):
                    self.admin_menu()
            else:
                print("1. Register")
                print("2. Login")
                print("3. Search Hotels as Guest")
                print("4. Make a Booking as Guest")
                print("5. Admin Actions")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.search_hotels()
                elif choice == '4':
                    self.make_booking()
                elif choice == '5':
                    self.admin_actions()

    def admin_actions(self):
        password = input("Enter Admin Password: ")
        if password == "Admin1":
            self.admin_menu()
        else:
            print("Incorrect password!")

    def admin_menu(self):
        while True:
            print("\nAdmin Menu")
            print("1. Add Hotel")
            print("2. Remove Hotel")
            print("3. Update Hotel")
            print("4. View All Bookings")
            print("5. Update Booking")
            print("6. Update Room Availability and Price")
            print("7. Add Room to Hotel")
            print("8. Back to Main Menu")
            choice = input("Choose an option: ")
            if choice == '1':
                self.add_hotel()
            elif choice == '2':
                self.remove_hotel()
            elif choice == '3':
                self.update_hotel()
            elif choice == '4':
                self.view_all_bookings()
            elif choice == '5':
                self.update_booking()
            elif choice == '6':
                self.update_room_availability_and_price()
            elif choice == '7':
                self.add_room_to_hotel()
            elif choice == '8':
                break

    def add_hotel(self):
        name = input("Hotel Name: ")
        address = input("Hotel Address: ")
        city = input("Hotel City: ")
        stars = int(input("Hotel Stars: "))
        hotel_id = len(self.base_manager.hotels) + 1  # Generating a new hotel ID
        new_hotel = Hotel(hotel_id, name, address, city, stars, [])
        self.admin_manager.add_hotel(new_hotel)

    def remove_hotel(self):
        hotel_id = int(input("Hotel ID to remove: "))
        self.admin_manager.remove_hotel(hotel_id)

    def update_hotel(self):
        hotel_id = int(input("Hotel ID to update: "))
        name = input("New Name (leave blank to keep current): ")
        address = input("New Address (leave blank to keep current): ")
        city = input("New City (leave blank to keep current): ")
        stars = input("New Stars (leave blank to keep current): ")
        self.admin_manager.update_hotel(
            hotel_id,
            name if name else None,
            int(stars) if stars else None,
            city if city else None,
            address if address else None
        )

    def add_room_to_hotel(self):
        hotel_id = int(input("Hotel ID to add room to: "))
        room_id = int(input("Room ID: "))
        room_type = input("Room Type: ")
        max_guests = int(input("Max Guests: "))
        description = input("Description: ")
        amenities = input("Amenities (comma separated): ").split(',')
        price_per_night = float(input("Price per night: "))
        availability = input("Availability dates (comma separated): ").split(',')
        new_room = Room(room_id, hotel_id, room_type, max_guests, description, amenities, price_per_night, availability)
        self.admin_manager.add_room_to_hotel(hotel_id, new_room)

    def view_all_bookings(self):
        self.admin_manager.view_all_bookings(self.base_manager.bookings)

    def update_booking(self):
        print("Update a booking")
        booking_id = int(input("Enter booking ID: "))
        booking = self.booking_manager.get_booking_by_id(booking_id)
        if not booking:
            print("Invalid booking ID.")
            return
        new_start_date = input("Enter new start date (YYYY-MM-DD) or leave blank to keep current: ")
        new_end_date = input("Enter new end date (YYYY-MM-DD) or leave blank to keep current: ")
        if new_start_date:
            booking.start_date = new_start_date
        if new_end_date:
            booking.end_date = new_end_date
        self.booking_manager.update_booking(booking)
        print(f"Booking {booking_id} updated successfully.")

    def update_room_availability_and_price(self):
        hotel_id = int(input("Hotel ID: "))
        room_id = int(input("Room ID: "))
        availability = input("New Availability dates (comma separated): ").split(',')
        price_per_night = float(input("New Price per night: "))
        self.admin_manager.update_room_availability_and_price(hotel_id, room_id, availability, price_per_night)

    def register(self):
        print("Register a new user")
        email = input("Email: ")
        password = input("Password: ")
        user_id = len(self.base_manager.users) + 1
        self.user_manager.register_user(user_id, email, password)
        print(f"User {email} registered successfully.")

    def login(self):
        print("Login")
        email = input("Email: ")
        password = input("Password: ")
        user = self.user_manager.login_user(email, password)
        if user:
            self.current_user = user
            print(f"Logged in as {email}.")
        else:
            print("Login failed.")

    def search_hotels(self):
        city = input("Enter city to search hotels: ")
        stars = input("Enter stars to filter hotels (leave blank for no filter): ")
        if stars:
            hotels = self.search_manager.search_by_city_and_stars(city, int(stars))
        else:
            hotels = self.search_manager.search_by_city(city)
        print("Hotels found:")
        for hotel in hotels:
            print(f"{hotel.hotel_id}. {hotel.name}, {hotel.stars} stars, {hotel.city}")

    def view_booking_history(self):
        print("View booking history")
        bookings = self.booking_manager.get_bookings_by_user(self.current_user.user_id)
        for booking in bookings:
            print(f"Booking ID: {booking.booking_id}, Hotel: {booking.hotel_id}, Room: {booking.room_id}, Dates: {booking.start_date} to {booking.end_date}")

    def make_booking(self):
        print("Make a booking")
        city = input("Enter city: ")
        hotels = self.search_manager.search_by_city(city)
        print("Available hotels:")
        for hotel in hotels:
            print(f"{hotel.hotel_id}. {hotel.name}, {hotel.stars} stars, {hotel.city}")
        hotel_id = int(input("Enter hotel ID to book: "))
        hotel = next((h for h in hotels if h.hotel_id == hotel_id), None)
        if not hotel:
            print("Invalid hotel ID.")
            return
        room_id = int(input("Enter room ID to book: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        total_price = float(input("Enter total price: "))
        booking = self.booking_manager.make_booking(self.current_user.user_id, hotel_id, room_id, start_date, end_date, total_price)
        if booking:
            print(f"Booking successful. Booking ID: {booking.booking_id}")
        else:
            print("Booking failed.")

    def cancel_booking(self):
        print("Cancel a booking")
        booking_id = int(input("Enter booking ID: "))
        success = self.booking_manager.cancel_booking(booking_id)
        if success:
            print(f"Booking {booking_id} cancelled successfully.")
        else:
            print("Cancellation failed.")
