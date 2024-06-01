from sqlalchemy.orm import sessionmaker
from models import init_db, Hotel, Room, Guest, Booking, Address
import datetime

def main():
    engine = init_db('sqlite:///hotel.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n1. Hotels anzeigen")
        print("2. Zimmer buchen")
        print("3. Buchungen anzeigen")
        print("4. Hotel hinzufügen")
        print("5. Programm beenden")
        choice = input("Wählen Sie eine Option: ")

        if choice == '1':
            hotels = session.query(Hotel).all()
            for hotel in hotels:
                print(f"{hotel.id}: {hotel.name}, Adresse: {hotel.address.city}, {hotel.stars} Sterne")
        elif choice == '2':
            guest_id = int(input("Gast-ID eingeben: "))
            guest = session.query(Guest).filter(Guest.id == guest_id).one_or_none()
            if guest:
                hotel_id = int(input("Hotel-ID eingeben: "))
                room_id = int(input("Zimmer-ID eingeben: "))
                start_date = input("Anfangsdatum (YYYY-MM-DD): ")
                end_date = input("Enddatum (YYYY-MM-DD): ")
                booking = Booking(room_id=room_id, guest_id=guest_id, start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'), end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                session.add(booking)
                session.commit()
                print("Zimmer gebucht!")
            else:
                print("Gast nicht gefunden.")
        elif choice == '3':
            bookings = session.query(Booking).all()
            for booking in bookings:
                print(f"Buchung {booking.id} für Gast {booking.guest.firstname} {booking.guest.lastname}, Zimmer {booking.room.number} vom {booking.start_date} bis {booking.end_date}")
        elif choice == '4':
            name = input("Hotelname: ")
            stars = int(input("Sterne: "))
            street = input("Straße: ")
            zip_code = input("PLZ: ")
            city = input("Stadt: ")
            address = Address(street=street, zip=zip_code, city=city)
            session.add(address)
            session.commit()
            hotel = Hotel(name=name, stars=stars, address_id=address.id)
            session.add(hotel)
            session.commit()
            print("Hotel hinzugefügt.")
        elif choice == '5':
            print("Programm wird beendet.")
            break
        else:
            print("Ungültige Eingabe.")

if __name__ == '__main__':
    main()
