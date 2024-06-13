from business.BaseManager import BaseManager
from business.SearchManager import SearchManager
from business.UserManager import UserManager
from business.BookingManager import BookingManager
from business.AdminManager import AdminManager
from datetime import datetime
import os


class ConsoleApp:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.base_manager = BaseManager()
        self.search_manager = SearchManager(
            os.path.join(self.data_dir, 'hotels.json'),
            os.path.join(self.data_dir, 'bookings.json')
        )
        self.user_manager = UserManager(os.path.join(self.data_dir, 'users.json'))
        self.booking_manager = BookingManager(
            os.path.join(self.data_dir, 'bookings.json'),
            os.path.join(self.data_dir, 'users.json'),
            os.path.join(self.data_dir, 'hotels.json')
        )
        self.admin_manager = AdminManager(os.path.join(self.data_dir, 'hotels.json'))
        self.current_user = None

    def run(self):
        while True:
            print("\nHotel Reservations System")
            if self.current_user:
                self.show_user_menu()
            else:
                self.show_guest_menu()

    def show_guest_menu(self):
        print("1. Register")
        print("2. Login")
        print("3. Search Hotel as Guest")
        print("4. Make a Booking as Guest")
        print("5. Admin Actions")
        print("6. Quit")
        choice = input("Choose an option: ")
        if choice == '1':
            self.register()
        elif choice == '2':
            self.login()
        elif choice == '3':
            self.search_hotels_as_guest()
        elif choice == '4':
            self.make_booking_as_guest()
        elif choice == '5':
            self.admin_actions()
        elif choice == '6':
            exit()

    def register(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user = self.user_manager.register(email, password)
        if user:
            print("Registration successful.")
        else:
            print("Registration failed. User might already exist.")

    def login(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        user = self.user_manager.login(email, password)
        if user:
            self.current_user = user
            print("Login successful.")
        else:
            print("Login failed. Check your credentials.")

    def show_user_menu(self):
        print(f"Logged in as: {self.current_user['email']}")
        print("1. Search Hotels")
        print("2. View Booking History")
        print("3. Make a Booking")
        print("4. Update a Booking")
        print("5. Cancel a Booking")
        print("6. Logout")
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

    def search_hotels(self):
        city = input("Enter city: ")
        stars = input("Enter number of stars (optional): ")
        guests = input("Enter number of guests (optional): ")
        start_date = input("Enter start date (YYYY-MM-DD, optional): ")
        end_date = input("Enter end date (YYYY-MM-DD, optional): ")

        if stars:
            stars = int(stars)
        if guests:
            guests = int(guests)

        hotels = self.search_manager.search(city, stars, guests, start_date, end_date)
        self.display_hotels(hotels)

    def search_hotels_as_guest(self):
        city = input("Enter city: ")
        stars = input("Enter number of stars (optional): ")
        guests = input("Enter number of guests (optional): ")
        start_date = input("Enter start date (YYYY-MM-DD, optional): ")
        end_date = input("Enter end date (YYYY-MM-DD, optional): ")

        if stars:
            stars = int(stars)
        if guests:
            guests = int(guests)

        hotels = self.search_manager.search(city, stars, guests, start_date, end_date)
        self.display_hotels(hotels)

    def display_hotels(self, hotels):
        print("Hotels found:")
        for hotel in hotels:
            print(
                f"Hotel ID: {hotel['hotel_id']}. {hotel['name']}, {hotel['stars']} stars, {hotel['address']}, {hotel['city']}")
            for room in hotel['rooms']:
                amenities = ', '.join(room['amenities'])
                print(
                    f"  Room ID: {room['room_id']}, Type: {room['room_type']}, Max Guests: {room['max_guests']}, Price: {room['price_per_night']}, Description: {room['description']}, Amenities: {amenities}")

    def make_booking(self):
        hotel_id = input("Enter hotel ID: ")
        room_id = input("Enter room ID: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        total_price = self.booking_manager.calculate_price(hotel_id, room_id, start_date, end_date)
        print(f"Total price: {total_price}")
        confirm = input("Confirm booking (yes/no): ")
        if confirm.lower() == 'yes':
            booking = self.booking_manager.make_booking(self.current_user['user_id'], hotel_id, room_id, start_date,
                                                        end_date, total_price)
            if booking:
                print("Booking successful.")
            else:
                print("Booking failed.")

    def make_booking_as_guest(self):
        hotel_id = input("Enter hotel ID: ")
        room_id = input("Enter room ID: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        total_price = self.booking_manager.calculate_price(hotel_id, room_id, start_date, end_date)
        print(f"Total price: {total_price}")
        confirm = input("Confirm booking (yes/no): ")
        if confirm.lower() == 'yes':
            booking = self.booking_manager.make_booking_as_guest(hotel_id, room_id, start_date, end_date, total_price)
            if booking:
                print("Booking successful. A booking confirmation has been generated.")
            else:
                print("Booking failed.")

    def view_booking_history(self):
        print("View booking history")
        bookings = self.booking_manager.get_bookings_by_user(self.current_user['user_id'])
        for booking in bookings:
            print(
                f"Booking ID: {booking['booking_id']}, Hotel: {booking['hotel_id']}, Room: {booking['room_id']}, Dates: {booking['start_date']} to {booking['end_date']}")

    def update_booking(self):
        print("Update a booking")
        booking_id = int(input("Enter booking ID: "))
        start_date = input("Enter new start date (YYYY-MM-DD): ")
        end_date = input("Enter new end date (YYYY-MM-DD): ")
        success = self.booking_manager.update_booking(booking_id, start_date, end_date)
        if success:
            print(f"Booking {booking_id} updated successfully.")
        else:
            print("Update failed.")

    def cancel_booking(self):
        print("Cancel a booking")
        booking_id = int(input("Enter booking ID: "))
        success = self.booking_manager.cancel_booking(booking_id)
        if success:
            print(f"Booking {booking_id} cancelled successfully.")
        else:
            print("Cancellation failed.")

    def admin_actions(self):
        password = input("Enter admin password: ")
        if password == 'Admin1':
            print("1. Add Hotel")
            print("2. Update Hotel")
            print("3. Delete Hotel")
            print("4. View All Bookings")
            print("5. Update Booking")
            print("6. Logout")
            choice = input("Choose an option: ")
            if choice == '1':
                self.admin_manager.add_hotel()
            elif choice == '2':
                self.admin_manager.update_hotel()
            elif choice == '3':
                self.admin_manager.delete_hotel()
            elif choice == '4':
                self.admin_manager.view_all_bookings()
            elif choice == '5':
                self.admin_manager.update_booking()
            elif choice == '6':
                return
        else:
            print("Invalid admin password.")
