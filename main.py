from sqlalchemy.orm import sessionmaker
from models import init_db, Hotel, Room, Booking
from config import Config
import datetime

def main():
    engine = init_db(Config.DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    while True:
        print("\n1. Hotels anzeigen")
        print("2. Zimmer buchen")
        print("3. Buchungen anzeigen")
        print("4. Programm beenden")
        choice = input("Wählen Sie eine Option: ")

        if choice == '1':
            hotels = session.query(Hotel).all()
            for hotel in hotels:
                print(f"{hotel.id}: {hotel.name}, {hotel.address}, {hotel.star_rating} Sterne")
        elif choice == '2':
            hotel_id = int(input("Hotel-ID eingeben: "))
            start_date = input("Anfangsdatum (YYYY-MM-DD): ")
            end_date = input("Enddatum (YYYY-MM-DD): ")
            room = session.query(Room).filter(Room.hotel_id == hotel_id).first()
            if room:
                booking = Booking(room_id=room.id, start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'), end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
                session.add(booking)
                session.commit()
                print("Zimmer gebucht!")
            else:
                print("Kein Zimmer verfügbar.")
        elif choice == '3':
            bookings = session.query(Booking).all()
            for booking in bookings:
                print(f"Buchung {booking.id} für Zimmer {booking.room_id} vom {booking.start_date} bis {booking.end_date}")
        elif choice == '4':
            break
        else:
            print("Ungültige Eingabe.")

if __name__ == '__main__':
    main()
