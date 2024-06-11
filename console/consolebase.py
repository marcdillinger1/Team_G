# console/consolebase.py

from business.BaseManager import BaseManager
from business.SearchManager import SearchManager
from business.UserManager import UserManager
from business.BookingManager import BookingManager
from business.AdminManager import AdminManager
from datetime import datetime

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
                print("4. Cancel a Booking")
                print("5. Logout")
                if self.user_manager.is_admin(self.current_user.email, self.current_user.password):
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
                elif choice == '6' and self.user_manager.is_admin(self.current_user.email, self.current_user.password):
                    self.admin_menu()
                else:
                    print("Invalid choice!")
            else:
                print("1. Register")
                print("2. Login")
                print("3. Search Hotels as Guest")
                print("4. Make a Booking as Guest")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    self.search_hotels_guest()
                elif choice == '4':
                    self.make_booking_guest()
                else:
                    print("Invalid choice!")

    def register(self):
        email = input("Email: ")
        password = input("Password: ")
        user = self.user_manager.register_user(email, password)
        self.base_manager.save_all()
        print(f"Registered successfully! User ID: {user.user_id}")

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        user = self.user_manager.login_user(email, password)
        if user:
            self.current_user = user
            print("Logged in successfully!")
        else:
            print("Invalid email or password!")

    def search_hotels_guest(self):
        print("Search Hotels:")
        print("1. By City")
        print("2. By City and Stars")
        print("3. By City and Guests")
        print("4. By City, Guests, and Dates")
        choice = input("Choose an option: ")
        if choice == '1':
            self.search_by_city()
        elif choice == '2':
            self.search_by_city_and_stars()
        elif choice == '3':
            self.search_by_city_and_guests()
        elif choice == '4':
            self.search_by_city_dates_and_guests()
        else:
            print("Invalid choice!")

    def search_by_city(self):
        city = input("City: ")
        hotels = self.search_manager.search_by_city(city)
        self.display_hotels(hotels)

    def search_by_city_and_stars(self):
        city = input("City: ")
        stars = int(input("Stars: "))
        hotels = self.search_manager.search_by_city_and_stars(city, stars)
        self.display_hotels(hotels)

    def search_by_city_and_guests(self):
        city = input("City: ")
        guests = int(input("Number of guests: "))
        hotels = self.search_manager.search_by_city_and_guests(city, guests)
        self.display_hotels(hotels)

    def search_by_city_dates_and_guests(self):
        city = input("City: ")
        guests = int(input("Number of guests: "))
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        stars = input("Stars (leave blank for any): ")
        stars = int(stars) if stars else None

        hotels = self.search_manager.search_by_city_dates_and_guests(city, guests, start_date, end_date, stars)
        self.display_hotels(hotels, guests, start_date, end_date)

    def display_hotels(self, hotels, guests=None, start_date=None, end_date=None):
        if hotels:
            for hotel in hotels:
                print(f"Hotel ID: {hotel.hotel_id}, Name: {hotel.name}, Address: {hotel.address}, Stars: {hotel.stars}")
                if guests and start_date and end_date:
                    self.view_hotel_details(hotel.hotel_id, guests, start_date, end_date)
                else:
                    for room in hotel.rooms:
                        print(f"  Room ID: {room.room_id}, Type: {room.room_type}, Max Guests: {room.max_guests}, Price: {room.price_per_night}")
        else:
            print("No hotels found.")

    def view_hotel_details(self, hotel_id: int, guests: int, start_date: str, end_date: str):
        available_rooms = self.search_manager.get_available_rooms(hotel_id, guests, start_date, end_date)
        if available_rooms:
            print("Available Rooms:")
            for room in available_rooms:
                total_price = room.price_per_night * (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days
                print(f"Room ID: {room.room_id}, Type: {room.room_type}, Max Guests: {room.max_guests}, Description: {room.description}, Amenities: {', '.join(room.amenities)}, Price per Night: {room.price_per_night}, Total Price: {total_price}")
        else:
            print("No available rooms for the selected dates.")

    def make_booking(self):
        hotel_id = int(input("Hotel ID: "))
        room_id = int(input("Room ID: "))
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        try:
            booking = self.booking_manager.create_booking(self.current_user.user_id, room_id, hotel_id, start_date, end_date)
            self.base_manager.save_all()
            print(f"Booking created successfully! Booking ID: {booking.booking_id}")
        except ValueError as e:
            print(f"Error: {e}. Please use the format YYYY-MM-DD for dates.")

    def make_booking_guest(self):
        hotel_id = int(input("Hotel ID: "))
        room_id = int(input("Room ID: "))
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        try:
            # For guest users, we can use a temporary user ID, e.g., -1
            booking = self.booking_manager.create_booking(-1, room_id, hotel_id, start_date, end_date)
            self.base_manager.save_all()
            print(f"Booking created successfully! Booking ID: {booking.booking_id}")
        except ValueError as e:
            print(f"Error: {e}. Please use the format YYYY-MM-DD for dates.")

    def cancel_booking(self):
        booking_id = int(input("Booking ID: "))
        if self.booking_manager.cancel_booking(booking_id):
            self.base_manager.save_all()
            print("Booking canceled successfully!")
        else:
            print("Booking not found!")

    def admin_menu(self):
        print("Admin Menu:")
        print("1. Add Hotel")
        print("2. Remove Hotel")
        print("3. Update Hotel")
        print("4. View All Bookings")
        choice = input("Choose an option: ")
        if choice == '1':
            self.add_hotel()
        elif choice == '2':
            self.remove_hotel()
        elif choice == '3':
            self.update_hotel()
        elif choice == '4':
            self.view_all_bookings()
        else:
            print("Invalid choice!")

    def add_hotel(self):
        name = input("Hotel name: ")
        address = input("Hotel address: ")
        city = input("Hotel city: ")
        stars = int(input("Hotel stars: "))
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

    def view_all_bookings(self):
        bookings = self.booking_manager.get_all_bookings()
        if bookings:
            print("All bookings:")
            for booking in bookings:
                print(f"Booking ID: {booking.booking_id}, User ID: {booking.user_id}, Hotel ID: {booking.hotel_id}, Room ID: {booking.room_id}, Dates: {booking.start_date} to {booking.end_date}, Total Price: {booking.total_price}")
        else:
            print("No bookings found.")
