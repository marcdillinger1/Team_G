# Projekt: Hotelreservierungssystem

Marc Dillinger, Umut Can Özcelik, Dewa Dörflinger und Mario Lenzin

## Überblick

Dieses Projekt ist Teil des Kurses "Anwendungsentwicklung mit Python" und umfasst die Entwicklung eines einfachen Hotelreservierungssystems, das über die Konsole bedient wird. Wir haben die User Stories auf Manager aufgeteilt. SearchManager wurde von Mario bearbeitet. Booking Manager wurde von Marc bearbeitet. Hotel Manager wurde von Dewa bearbeitet. UserManager wurde von Umut bearbeitet. BaseManager wurde von Marc bearbeitet. An der ConsoleBase und den restlichen Files haben wir alle zusammen daran gearbeitet. 

## Projektbeschreibung

Das Hotelreservierungssystem ermöglicht Benutzern, sich zu registrieren, anzumelden, Hotels zu durchsuchen und Buchungen vorzunehmen. Registrierte Nutzer können ausserdem ihre Buchungen einsehen und verwalten. Administratoren haben erweiterte Funktionen zum Verwalten von Hotelinformationen, Zimmern und Buchungen. Hier sind die relevanten Dateien und deren Funktionen im Detail:

## Ausführung des Projekts

##### Stelle sicher, dass die JSON-Dateien (bookings.json, hotels.json, users.json) im data-Verzeichnis vorhanden sind.
##### Starte das Projekt, indem du main.py ausführst.
##### Verwende das Hauptmenü, um dich zu registrieren, anzumelden, Hotels zu durchsuchen und Buchungen vorzunehmen.
##### Administratoren können sich mit dem Passwort Admin1 anmelden, um auf die erweiterten Verwaltungsfunktionen zuzugreifen.

## UserStories

### 1. Als Gastnutzer (nicht eingeloggt/registriert):

#### 1.1. Als Gastnutzer möchte ich die verfügbaren Hotels durchsuchen, damit ich dasjenige auswählen kann, welches meinen Wünschen entspricht.
###### Beschreibung zur Ausführung: wählen sie im Hauptmenü "2. Search Hotel as Guest"

#### 1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.

#### 1.1.2. Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.

#### 1.1.3. Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.

#### 1.1.4. Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes ("von" (start_date) und "bis" (end_date)) Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne, damit ich nur relevante Ergebnisse sehe.

#### 1.1.5. Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.

#### 1.1.6. Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B. verfügbare Zimmer [siehe 1.2])

... alle UserStories

## Projektstruktur

### Models 

#### models.py: Definiert die Datenmodelle für das System.

###### Hotel: Repräsentiert ein Hotel mit Attributen wie hotel_id, name, address, city, stars und rooms.
###### Room: Repräsentiert ein Zimmer mit Attributen wie room_id, hotel_id, room_type, max_guests, description, amenities, price_per_night und availability.
###### Booking: Repräsentiert eine Buchung mit Attributen wie booking_id, user_id, room_id, hotel_id, start_date, end_date und total_price.
###### User: Repräsentiert einen Benutzer mit Attributen wie user_id, email, password und booking_history.

### Datenzugriff

#### data_access/data_loader.py: Lädt die Daten aus den JSON-Dateien.

###### load_hotels(file_path): Lädt die Hoteldaten aus der angegebenen JSON-Datei.
###### load_users(file_path): Lädt die Benutzerdaten aus der angegebenen JSON-Datei.
###### load_bookings(file_path): Lädt die Buchungsdaten aus der angegebenen JSON-Datei.

### Geschäftslogik

#### business/AdminManager.py: Bietet Verwaltungsfunktionen für Administratoren.

###### add_hotel(hotel): Fügt ein neues Hotel hinzu.
###### remove_hotel(hotel_id): Entfernt ein Hotel anhand seiner ID.
###### update_hotel(hotel_id, name, stars, city, address): Aktualisiert die Informationen eines Hotels.
###### add_room_to_hotel(hotel_id, room): Fügt ein Zimmer zu einem Hotel hinzu.
###### view_all_bookings(bookings): Zeigt alle Buchungen an.
###### update_booking(bookings, booking_id, phone): Aktualisiert eine Buchung.
###### update_room_availability_and_price(hotel_id, room_id, availability, price_per_night): Aktualisiert die Verfügbarkeit und den Preis eines Zimmers.
###### save_hotels(): Speichert die Hoteldaten in der JSON-Datei.

#### business/BaseManager.py: Lädt die Basisdaten für das System.

###### __init__(): Lädt die Hotels, Benutzer und Buchungen aus den entsprechenden JSON-Dateien.

#### business/BookingManager.py: Verwaltet Buchungen.

###### get_bookings_by_user(user_id): Gibt alle Buchungen eines Benutzers zurück.
###### make_booking(user_id, hotel_id, room_id, start_date, end_date, total_price): Erstellt eine neue Buchung.
###### update_booking(booking): Aktualisiert eine bestehende Buchung.
###### cancel_booking(booking_id): Storniert eine Buchung anhand ihrer ID.
###### get_booking_by_id(booking_id): Gibt eine Buchung anhand ihrer ID zurück.

#### business/SearchManager.py: Ermöglicht die Suche nach Hotels.

###### search_by_city(city): Sucht nach Hotels in einer bestimmten Stadt.
###### search_by_city_and_stars(city, stars): Sucht nach Hotels in einer bestimmten Stadt und mit einer bestimmten Sternebewertung.

#### business/UserManager.py: Verwaltet Benutzerinformationen.

###### register_user(user_id, email, password): Registriert einen neuen Benutzer.
###### login_user(email, password): Meldet einen Benutzer an und gibt dessen Informationen zurück.
###### is_admin(email, password): Überprüft, ob ein Benutzer ein Administrator ist.

### Benutzeroberfläche

#### console/consolebase.py: Bietet eine textbasierte Benutzeroberfläche für das System.

###### run(): Startet die Hauptschleife des Programms und zeigt das Hauptmenü an.
###### admin_actions(): Führt die Authentifizierung des Administrators durch und zeigt das Admin-Menü an.
###### admin_menu(): Zeigt das Admin-Menü mit den Verwaltungsfunktionen an.
###### add_hotel(): Ermöglicht das Hinzufügen eines neuen Hotels.
###### remove_hotel(): Ermöglicht das Entfernen eines Hotels.
###### update_hotel(): Ermöglicht das Aktualisieren der Hotelinformationen.
###### add_room_to_hotel(): Ermöglicht das Hinzufügen eines Zimmers zu einem Hotel.
###### view_all_bookings(): Zeigt alle Buchungen an.
###### update_booking(): Ermöglicht das Aktualisieren einer Buchung.
###### update_room_availability_and_price(): Ermöglicht das Aktualisieren der Verfügbarkeit und des Preises eines Zimmers.
###### register(): Ermöglicht die Registrierung eines neuen Benutzers.
###### login(): Ermöglicht die Anmeldung eines Benutzers.
###### search_hotels(): Ermöglicht die Suche nach Hotels.
###### view_booking_history(): Zeigt die Buchungshistorie des angemeldeten Benutzers an.
###### make_booking(): Ermöglicht das Erstellen einer neuen Buchung.
###### cancel_booking(): Ermöglicht das Stornieren einer Buchung.

### JSON-Dateien

#### data/bookings.json: Enthält die Buchungsdaten.

###### booking_id: Eindeutige Kennung der Buchung.
###### user_id: Kennung des Benutzers, der die Buchung vorgenommen hat (verweist auf users.json).
###### room_id: Kennung des gebuchten Zimmers (verweist auf hotels.json).
###### hotel_id: Kennung des Hotels, in dem das Zimmer gebucht wurde (verweist auf hotels.json).
###### start_date: Beginn der Buchung (Format YYYY-MM-DD).
###### end_date: Ende der Buchung (Format YYYY-MM-DD).
###### total_price: Gesamtkosten der Buchung.

#### data/hotels.json: Enthält die Hoteldaten inklusive Zimmerinformationen.

###### hotel_id: Eindeutige Kennung des Hotels.
###### name: Name des Hotels.
###### address: Adresse des Hotels.
###### city: Stadt, in der sich das Hotel befindet.
###### stars: Sternebewertung des Hotels.
###### rooms: Liste der Zimmer im Hotel. Jedes Zimmer enthält folgende Felder:

###### room_id: Eindeutige Kennung des Zimmers.
###### hotel_id: Kennung des Hotels, zu dem das Zimmer gehört.
###### room_type: Zimmertyp (z.B. Einzelzimmer, Doppelzimmer).
###### max_guests: Maximale Anzahl der Gäste im Zimmer.
###### description: Beschreibung des Zimmers.
###### amenities: Liste der Annehmlichkeiten im Zimmer.
###### price_per_night: Preis pro Nacht.
###### availability: Liste der verfügbaren Daten (Format YYYY-MM-DD).

#### data/users.json: Enthält die Benutzerdaten.

###### user_id: Eindeutige Kennung des Benutzers.
###### email: E-Mail-Adresse des Benutzers (Anmeldeinformation).
###### password: Passwort des Benutzers (sollte verschlüsselt gespeichert werden).
###### booking_history: Liste der Buchungen des Benutzers (verweist auf bookings.json).


## Quellen

### ChatGPT

#### Für die Bearbeitung dieser Projektarbeit haben wir sehr eng mit ChatGPT zusammengearbeitet.
#### Nachfolgend alle links zu den Interaktionen mit ChatGPT um nachzuvollziehen und aufzuzeigen wie die Anwendung des Tools aussah.

https://chatgpt.com/share/0580e43b-bfbd-4f13-aaf9-422c03405154

https://chatgpt.com/share/83d9a5ec-106f-47af-a863-ea8105b54168

https://chatgpt.com/share/e2e10479-83a5-46ee-b0ad-6d428485f1b2

https://chatgpt.com/share/f588e5ee-c61a-4964-867c-d9d1bd5b7eae

https://chatgpt.com/share/412816aa-8092-4e08-a724-9471195628ae

https://chatgpt.com/share/595048ff-eea1-4dd9-8d96-25a2feac64c2

https://chatgpt.com/share/3c02ea42-a753-42d4-8a31-208a16f030c6

https://chatgpt.com/share/a253426c-2e00-4c0a-88ce-7d6d71e2fc01

https://chatgpt.com/share/b7f6a72e-0274-4de6-90cf-daa32da4344c

https://chatgpt.com/share/7966086a-d099-4f40-8fe4-753d4510c6be
