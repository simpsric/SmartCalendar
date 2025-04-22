import datetime
import yaml
import os, sys

class Events:
    def __init__(self,
                event_id: int,
                event_name: str,
                event_description: str,
                event_date: datetime,
                event_time: datetime = None,
                event_location: str = None,
                event_type: str = None,
                event_status: str = None,
                event_priority: int = None,
                event_notes: str = None,
                event_reminder: datetime = None,
                ):
        '''
        Initialize an event with the given parameters.
        :param event_id: Unique identifier for the event
        :param event_name: Name of the event
        :param event_description: Description of the event
        :param event_date: Date of the event
        :param event_time: Time of the event
        :param event_location: Location of the event
        :param event_type: Type of the event (e.g., meeting, conference)
        :param event_status: Status of the event (e.g., confirmed, tentative)
        :param event_priority: Priority of the event (e.g., high, medium, low)
        :param event_notes: Additional notes for the event
        :param event_reminder: Reminder for the event
        '''
        self.event_id = event_id
        self.event_name = event_name
        self.event_description = event_description
        self.event_date = event_date
        self.event_time = event_time
        self.event_location = event_location
        self.event_type = event_type
        self.event_status = event_status
        self.event_priority = event_priority
        self.event_notes = event_notes
        self.event_reminder = event_reminder
        
    def get_month(self):
        '''
        Get the month of the event date.
        :return: Month number (1-12)
        '''
        return self.event_date.month
    def get_year(self):
        '''
        Get the year of the event date.
        :return: Year number
        '''
        return self.event_date.year
    def print_date(self):
        '''
        Print the event date in a readable format.
        :return: Formatted date string
        '''
        return self.event_date.strftime("%Y-%m-%d")
    def print_time(self):
        '''
        Print the event time in a readable format.
        :return: Formatted time string
        '''
        return self.event_time.strftime("%H:%M") if self.event_time else None
    def print_event(self):
        '''
        Print the event details in a readable format.
        :return: Formatted event string
        '''
        return f"Event: {self.event_name}, Description: {self.event_description}, Date: {self.print_date()}, Time: {self.print_time()}, Location: {self.event_location}, Notes: {self.event_notes}"
    def __str__(self):
        '''
        String representation of the event.
        :return: Formatted event string
        '''
        return self.print_event()
    def __repr__(self):
        '''
        String representation of the event for debugging.
        :return: Formatted event string
        '''
        return self.__str__()
    
class Month:
    def __init__(self,
                month: int,
                year: int,
                events: list[Events] = None,  # Use None as the default value
                ):
        '''
        Initialize a month with the given parameters.
        :param month: Month number (1-12)
        :param year: Year number
        :param events: List of events for the month
        '''
        self._month = month
        self._year = year
        self._events = events if events is not None else []  # Initialize a new list if None
    
    def get_month(self):
        '''
        Get the month number.
        :return: Month number
        '''
        return self._month
    def get_year(self):
        '''
        Get the year number.
        :return: Year number
        '''
        return self._year
    def get_events(self):
        '''
        Get the list of events for the month.
        :return: List of events
        '''
        return self._events
    def add_event(self, event: Events):
        '''
        Add an event to the month.
        :param event: Event to be added
        '''
        if type(event) is not Events:
            raise TypeError("event must be of type Events")
        if event.get_month() != self._month or event.get_year() != self._year:
            raise ValueError("event month and year must match month and year of the Month object")
        # Check if the event already exists
        for e in self._events:
            if e.event_id == event.event_id:
                raise ValueError("event already exists in the month")
        # Add the event to the month
        self._events.append(event)
    def remove_event(self, event: Events):
        '''
        Remove an event from the month.
        :param event: Event to be removed
        '''
        if type(event) is not Events:
            raise TypeError("event must be of type Events")
        if event not in self._events:
            raise ValueError("event not found in the month")
        self._events.remove(event)
    def update_event(self, event: Events):
        '''
        Update an event in the month.
        :param event: Event to be updated
        '''
        if type(event) is not Events:
            raise TypeError("event must be of type Events")
        if event not in self._events:
            raise ValueError("event not found in the month")
        index = self._events.index(event)
        self._events[index] = event
        
class DataController:
    def __init__(self):
        '''
        Initialize the DataController with an empty list of months.
        '''
        self._months = []
        self._start_up()
    
    def _start_up(self):
        '''
        Start up the DataController by loading data from the database.
        '''
        # load data from the 'data_storage' directory
        # For each month, load the events from the database
        file_list = os.listdir("data_storage")
        current_date = datetime.datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        # Calculate the range of months to include
        start_month = (current_month - 2) % 12 or 12
        start_year = current_year if current_month > 2 else current_year - 1
        end_month = (current_month + 2) % 12 or 12
        end_year = current_year if current_month <= 10 else current_year + 1

        #print the month ranges to console
        print(f"Loading events from {start_month}/{start_year} to {end_month}/{end_year}")
                    
        for file_name in file_list:
            # check if the file is a yaml file
            if file_name.endswith(".yaml"):
                # load the events from the yaml file, using the yaml module
                with open(f"data_storage/{file_name}", 'r') as file:
                    data = yaml.safe_load(file)
                    
                    
                    # Skip months outside the range
                    if not data or \
                       (data['year'] < start_year or (data['year'] == start_year and data['month'] < start_month)) or \
                       (data['year'] > end_year or (data['year'] == end_year and data['month'] > end_month)):
                        continue
                    month = Month(data['month'], data['year'])
                    for event_data in data["events"]:
                        event = Events(
                            event_id=event_data["event_id"],
                            event_name=event_data["event_name"],
                            event_description=event_data["event_description"],
                            event_date=datetime.datetime.strptime(event_data["event_date"], "%Y-%m-%d"),
                            event_time=datetime.datetime.strptime(event_data["event_time"], "%H:%M") if event_data["event_time"] else None,
                            event_location=event_data["event_location"],
                            event_type=event_data["event_type"],
                            event_status=event_data["event_status"],
                            event_priority=event_data["event_priority"],
                            event_notes=event_data["event_notes"],
                            event_reminder=datetime.datetime.strptime(event_data["event_reminder"], "%Y-%m-%d %H:%M") if event_data["event_reminder"] else None,
                        )
                        month.add_event(event)
                    self._months.append(month)
    
    def shut_down(self):
        '''
        Shut down the DataController by saving data to the database.
        '''
        # For each month, save the events to the database
        for month in self._months:
            # create a yaml file name based on month and year
            file_name = f"data_storage/{datetime.date(1900, month.get_month(), 1).strftime('%B').lower()}{month.get_year()}.yaml"
            # save the events to the yaml file, using the yaml module
            with open(file_name, 'w') as file:
                data = {
                    "month": month.get_month(),
                    "year": month.get_year(),
                    "events": [
                        {
                            "event_id": event.event_id,
                            "event_name": event.event_name,
                            "event_description": event.event_description,
                            "event_date": event.print_date(),
                            "event_time": event.print_time(),
                            "event_location": event.event_location,
                            "event_type": event.event_type,
                            "event_status": event.event_status,
                            "event_priority": event.event_priority,
                            "event_notes": event.event_notes,
                            "event_reminder": event.event_reminder.strftime("%Y-%m-%d %H:%M") if event.event_reminder else None,
                        }
                        for event in month.get_events()
                    ],
                }
                yaml.dump(data, file, default_flow_style=False)
    
    def demo_start_up(self):
        '''
        Start up the DataController with demo data.
        '''
        # Create some Demo data
        # Create some months
        month1 = Month(1, 2023)
        month2 = Month(2, 2023)
        month3 = Month(3, 2023)
        
        # Create some events
        # Create a soccer event
        event1 = Events(1, "Soccer", "Soccer game", datetime.datetime(2023, 1, 15), datetime.datetime(2023, 1, 15, 10, 0), "Stadium", "Sport", "Confirmed", 1, "Bring water", datetime.datetime(2023, 1, 14))
        event4 = Events(4, "Yoga Class", "Morning yoga session", datetime.datetime(2023, 1, 22), datetime.datetime(2023, 1, 22, 7, 0), "Gym", "Health", "Confirmed", 2, "Bring yoga mat", datetime.datetime(2023, 1, 21))
        
        event2 = Events(2, "Basketball", "Basketball game", datetime.datetime(2023, 2, 20), datetime.datetime(2023, 2, 20, 18, 0), "Arena", "Sport", "Confirmed", 1, "Bring water", datetime.datetime(2023, 2, 19))
        event5 = Events(5, "Team Meeting", "Monthly team meeting", datetime.datetime(2023, 2, 10), datetime.datetime(2023, 2, 10, 14, 0), "Office", "Work", "Confirmed", 3, "Prepare slides", datetime.datetime(2023, 2, 9))
        
        event3 = Events(3, "Doc Appointment", "Doctor appointment", datetime.datetime(2023, 3, 25), datetime.datetime(2023, 3, 25, 9, 0), "Clinic", "Health", "Confirmed", 1, "Bring insurance card", datetime.datetime(2023, 3, 24))
        event6 = Events(6, "Birthday Party", "Friend's birthday celebration", datetime.datetime(2023, 3, 18), datetime.datetime(2023, 3, 18, 19, 0), "Restaurant", "Social", "Confirmed", 2, "Buy a gift", datetime.datetime(2023, 3, 17))
        
        # Add events to months
        month1.add_event(event1)
        month1.add_event(event4)
        
        month2.add_event(event2)
        month2.add_event(event5)
        
        month3.add_event(event3)
        month3.add_event(event6)
        
        # Add months to the DataController
        self._months.append(month1)
        self._months.append(month2)
        self._months.append(month3)
        
    def add_event(self, event: Events):
        '''
        Add an event to the DataController.
        :param event: Event to be added
        '''
        if type(event) is not Events:
            raise TypeError("event must be of type Events")
        # Check if the event already exists
        for month in self._months:
            if month.get_month() == event.event_date.month and month.get_year() == event.event_date.year:
                if event in month.get_events():
                    raise ValueError("event already exists in the month")
                # Add the event to the appropriate month
                month.add_event(event)
                return
        # Month and Year not found; create a new one
        new_month = Month(event.event_date.month, event.event_date.year)
        new_month.add_event(event)
        self._months.append(new_month)
    
    def remove_event(self, event: Events):
        '''
        Remove an event from the DataController.
        :param event: Event to be removed
        '''
        if type(event) is not Events:
            raise TypeError("event must be of type Events")
        # Check if the event exists
        for month in self._months:
            if month.get_month() == event.event_date.month and month.get_year() == event.event_date.year:
                if event in month.get_events():
                    # Remove the event from the appropriate month
                    month.remove_event(event)
                    return
        raise ValueError("event not found in the DataController")
    
    def update_event(self, event: Events):
        '''
        Update an event in the DataController.
        :param event: Event to be updated
        '''
        if type(event) is not Events:
            raise TypeError("event must be of type Events")
        # Check if the event exists
        for month in self._months:
            if month.get_month() == event.event_date.month and month.get_year() == event.event_date.year:
                if event in month.get_events():
                    # Update the event in the appropriate month
                    month.update_event(event)
                    return
        raise ValueError("event not found in the DataController")
    
    def get_events(self, month: int, year: int):
        '''
        Get the list of events for a specific month and year.
        :param month: Month number (1-12)
        :param year: Year number
        :return: List of events for the specified month and year
        '''
        for m in self._months:
            if m.get_month() == month and m.get_year() == year:
                return m.get_events()
        return []
    
if __name__ == "__main__":
    # Create a DataController instance
    controller = DataController()
    
    # Print the events that it was started with
    for month in controller._months:
        print(f"Month: {month.get_month()}, Year: {month.get_year()}")
        for event in month.get_events():
            print(event)
            
    controller.shut_down()