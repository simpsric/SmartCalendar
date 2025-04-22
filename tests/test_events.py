import unittest
import datetime
from src.events import Events, Month, DataController

class TestEvents(unittest.TestCase):
    def test_event_initialization(self):
        event = Events(
            event_id=1,
            event_name="Meeting",
            event_description="Team meeting",
            event_date=datetime.datetime(2023, 5, 10),
            event_time=datetime.datetime(2023, 5, 10, 14, 0),
            event_location="Office",
            event_type="Work",
            event_status="Confirmed",
            event_priority=1,
            event_notes="Bring slides",
            event_reminder=datetime.datetime(2023, 5, 9, 14, 0),
        )
        self.assertEqual(event.event_name, "Meeting")
        self.assertEqual(event.get_month(), 5)
        self.assertEqual(event.get_year(), 2023)

class TestMonth(unittest.TestCase):
    def setUp(self):
        self.month = Month(5, 2023)

    def test_add_event(self):
        event = Events(
            event_id=1,
            event_name="Meeting",
            event_description="Team meeting",
            event_date=datetime.datetime(2023, 5, 10),
        )
        self.month.add_event(event)
        self.assertIn(event, self.month.get_events())

    def test_remove_event(self):
        event = Events(
            event_id=1,
            event_name="Meeting",
            event_description="Team meeting",
            event_date=datetime.datetime(2023, 5, 10),
        )
        self.month.add_event(event)
        self.month.remove_event(event)
        self.assertNotIn(event, self.month.get_events())

    def test_add_event_invalid_date(self):
        event = Events(
            event_id=1,
            event_name="Meeting",
            event_description="Team meeting",
            event_date=datetime.datetime(2023, 6, 10),
        )
        with self.assertRaises(ValueError):
            self.month.add_event(event)

class TestDataController(unittest.TestCase):
    def setUp(self):
        self.controller = DataController()
        self.event = Events(
            event_id=1,
            event_name="Meeting",
            event_description="Team meeting",
            event_date=datetime.datetime(2023, 5, 10),
        )

    def test_add_event(self):
        self.controller.add_event(self.event)
        events = self.controller.get_events(5, 2023)
        self.assertIn(self.event, events)

    def test_remove_event(self):
        self.controller.add_event(self.event)
        self.controller.remove_event(self.event)
        events = self.controller.get_events(5, 2023)
        self.assertNotIn(self.event, events)

    def test_get_events_empty(self):
        events = self.controller.get_events(5, 2023)
        self.assertEqual(len(events), 0)

if __name__ == "__main__":
    unittest.main()