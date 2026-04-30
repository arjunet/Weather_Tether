from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

from carbonkivy.uix.modal import CModal

from .setup import Request_City, save_location_request, update_location_request
from .app import save_city
from .modal_loader import ModalLoader

import threading

class ChangeLocationModal(CModal):
    def __init__(self, city, update_type, **kwargs):
        super().__init__(**kwargs)
        self.suggestion_was_pressed = False
        self.city = city
        self.update_type = update_type
        # Timer setup
        self.pending_search = None
        self.countinue = False
        self.suggestion_was_pressed = False
        self.firestore_done = False 

        # Reset location variables
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.city_found = False
        self.dismissed = False
        self.add_2 = False
        self.add_3 = False
        self.add_other = True

    def start_lookup(self, *args):
        self.city_found = False
        # Kill any existing timer
        if self.pending_search:
            Clock.unschedule(self.pending_search)

        # Run the actual search after 0.5s of silence
        if self.countinue == False:
            self.pending_search = Clock.schedule_once(self.request, 0.5)

    def request(self, dt):
        # 3. THE LOCK: Now we start the thread
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.City,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_lookup, 0.1)

    def City(self):
        Request_City(self)

    def stop_lookup(self, *args):
        # Check if background task finished
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_lookup)
        self.ids.loader.opacity = 0

    def on_address_button_press(self, text):
        # Ignore placeholder text
        if text == "Start typing" or text == "No results found":
             return
        
        # Fill the text field
        self.countinue = True
        self.suggestion_was_pressed = True
        self.ids.address_input.text = text

    def countinue_pressed(self):
        # Only submit if city was found
        if self.suggestion_was_pressed == False:
            return 

        # Show loading spinner
        self.modal_loader = ModalLoader()
        self.add_widget(self.modal_loader)

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.save_location,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_firestore, 0.1)

    def save_location(self):
        update_location_request(self, self.update_type)
        location_input = str(self.ids.address_input.text.strip())
        # Save city to local session
        save_city(location_input, self.update_type)
        # Schedule UI work on main thread to dismiss modal and refresh

    def stop_load_firestore(self, *args):
        # Check if background task finished
        if self.firestore_done != True:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_firestore)
        self.remove_widget(self.modal_loader)

        location_input = self.ids.address_input.text.strip()
        save_city(location_input, 1)

        self.dismiss()
        self.city.start_load_weather()
# ---------------------------------------------------------------------------------
class LogoutModal(CModal):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings

    def logout_confirmed(self):
        self.dismiss()
        self.settings.logout()
# ---------------------------------------------------------------------------------
class DeleteModal(CModal):
    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings

    def delete_confirmed(self, email_input, password_input):
        self.dismiss()
        self.settings.start_delete_account(email_input, password_input)
# ---------------------------------------------------------------------------------
class DeleteLocationModal(CModal):
    def __init__(self, city_name, screen_instance, **kwargs):
        super().__init__(**kwargs)
        self.city_name = city_name
        self.screen_instance = screen_instance

    def delete_confirmed(self):
        store = JsonStore("session.json")

        if self.city_name == "city2":
            store.delete("city2")

            self.screen_instance.start_delete_city()

        elif self.city_name == "city3":
            store.delete("city3")

            self.screen_instance.start_delete_city()
# ---------------------------------------------------------------------------------
class AddCityModal(CModal):
    def __init__(self, city, city_number, **kwargs):
        super().__init__(**kwargs)
        self.city = city
        self.city_number = city_number
        # Timer setup
        self.pending_search = None
        self.countinue = False
        self.suggestion_was_pressed = False
        self.firestore_done = False

        # Reset location variables
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.city_found = False
        self.dismissed = False
        self.add_2 = False
        self.add_3 = False
        self.add_other = True

        if self.city_number == 2:
            self.ids.header_title.text = "Would You Like To Add A Second City To Your Account?"
            self.ids.body.text = "Adding a second city to your account will allow you to easily switch between cities in the app without having to change your saved location."
            self.add_2 = True

        elif self.city_number == 3:
            self.ids.header_title.text = "Would You Like To Add A Third City To Your Account?"
            self.ids.body.text = "Adding a third city to your account will allow you to easily switch between cities in the app without having to change your saved location."
            self.add_3 = True

    def start_lookup(self, *args):
        self.city_found = False
        # Kill any existing timer
        if self.pending_search:
            Clock.unschedule(self.pending_search)

        # Run the actual search after 0.5s of silence
        if self.countinue == False:
            self.pending_search = Clock.schedule_once(self.request, 0.5)

    def request(self, dt):
        # 3. THE LOCK: Now we start the thread
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.City,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_lookup, 0.1)

    def City(self):
        Request_City(self)

    def stop_lookup(self, *args):
        # Check if background task finished
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_lookup)
        self.ids.loader.opacity = 0

    def on_address_button_press(self, text):
        # Ignore placeholder text
        if text == "Start typing" or text == "No results found":
             return
        
        # Fill the text field
        self.countinue = True
        self.suggestion_was_pressed = True
        self.ids.address_input.text = text

    def countinue_pressed(self):
        # Only submit if city was found
        if self.suggestion_was_pressed == False:
            return 

        # Show loading spinner
        self.modal_loader = ModalLoader()
        self.add_widget(self.modal_loader)

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.save_location,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_firestore, 0.1)

    def save_location(self):
        save_location_request(self)

    def stop_load_firestore(self, *args):
        # Check if background task finished
        if self.firestore_done != True:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_firestore)
        self.remove_widget(self.modal_loader)

        location_input = self.ids.address_input.text.strip()
        save_city(location_input, 1)

        self.dismiss()
        self.city.start_load_weather()