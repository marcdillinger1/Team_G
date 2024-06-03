import unittest
from models import Hotel, init_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestHotelFunctions(unittest.TestCase):
    def setUp(self):
        # Einrichten einer Testdatenbank im Speicher
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def test_add_hotel(self):
        # Testet das Hinzufügen eines Hotels
        hotel = Hotel(name="Test Hotel", stars=4)
        self.session.add(hotel)
        self.session.commit()
        retrieved = self.session.query(Hotel).one()
        self.assertEqual(retrieved.name, "Test Hotel")
        self.assertEqual(retrieved.stars, 4)

if __name__ == '__main__':
    unittest.main()
