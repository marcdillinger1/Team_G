from sqlalchemy.orm import sessionmaker
from models import init_db, Hotel, Room, Guest, Booking, Address
import datetime

def main():
    # Initialisiert die Datenbank und erstellt eine Session
    engine = init_db('sqlite:///hotel.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Hauptmenü der Konsolenanwendung
    while True:
        print("\n1. Hotels anzeigen")
        print("2. Zimmer buchen")
        print("3. Buchungen anzeigen")
        print("4. Hotel hinzufügen")
        print("5. Programm beenden")
        choice = input("Wählen Sie eine Option: ")

        # Logik für die verschiedenen Menüoptionen
        if choice == '1':
            hotels = session.query(Hotel).all()
            for hotel in hotels:
                print(f"{hotel.id}: {hotel.name}, Adresse: {hotel.address.city}, {hotel.stars} Sterne")
        # Weitere Optionen folgen ...

if __name__ == '__main__':
    main()
