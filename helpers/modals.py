from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore

from carbonkivy.uix.modal import CModal

from .setup import Request_City, save_location_request, update_location_request
from .app import save_city
from .notification import notification_success

import time
import threading

class ChangeLocationModal(CModal):
    def __init__(self, city, update_type, **kwargs):
        super().__init__(**kwargs)
        self.suggestion_was_pressed = False
        self.city = city
        self.update_type = update_type
        # Timer setup
        self._last_request_time = 0
        self._debounce_event = None  

        # Reset location variables
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.city_found = False
        self.dismissed = False
        self.add_2 = False
        self.add_3 = False

    def Setup(self):
        # Stop duplicate requests
        if self.suggestion_was_pressed:
            return
        
        # Timer setup again
        if self._debounce_event:
            self._debounce_event.cancel()
        self._debounce_event = Clock.schedule_once(lambda dt: self.make_request_when_ready(), 0.9)

    def make_request_when_ready(self):
        now = time.time()
        # Timer setup again
        if now - self._last_request_time < 2.5:
            return
        self._last_request_time = now

        # Show loading spinner
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.City,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def City(self): # For text input typing
        Request_City(self)

    # Fill text input when address button is pressed
    def on_address_button_press(self, text):
        # Ignore placeholder text
        if text == "Start typing" or text == "No results found.":
             return
        
        # Fill the text field
        self.suggestion_was_pressed = True
        self.ids.address_input.text = text

    def countinue_pressed(self):
        # Only submit if city was found
        if not self.city_found == True:
            return 

        # Show loading spinner
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.save_location,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_firestore, 0.1)

    def save_location(self):
        self.add_other = True
        update_location_request(self, self.update_type)
        location_input = str(self.ids.address_input.text.strip())
        # Save city to local session
        save_city(location_input, self.update_type)
        # Schedule UI work on main thread to dismiss modal and refresh
        try:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.on_saved(), 0)
        except Exception:
            pass
        self.dismissed = True

    def stop_load(self, *args):
        # Check if background task finished
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0
        
    def stop_load_firestore(self, *args):
        # Check if background task finished
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_firestore)
        self.ids.loader.opacity = 0
        if self.dismissed == True:
            # For backward compatibility
            try:
                self.dismiss()
            except Exception:
                pass
            try:
                self.city.start_load_weather()
            except Exception:
                pass

    def on_saved(self, *args):
        self.dismiss()
        self.city.start_load_weather()
        self.dismissed = False

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

    def delete_confirmed(self):
        self.dismiss()
        self.settings.start_delete_account()

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
        self.suggestion_was_pressed = False
        self.city = city
        self.city_number = city_number
        # Timer setup
        self._last_request_time = 0
        self._debounce_event = None  

        # Reset location variables
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.city_found = False
        self.dismissed = False
        self.add_2 = False
        self.add_3 = False

        if self.city_number == 2:
            self.ids.header_title.text = "Would You Like To Add A Second City To Your Account?"
            self.ids.body.text = "Adding a second city to your account will allow you to easily switch between cities in the app without having to change your saved location."
        elif self.city_number == 3:
            self.ids.header_title.text = "Would You Like To Add A Third City To Your Account?"
            self.ids.body.text = "Adding a third city to your account will allow you to easily switch between cities in the app without having to change your saved location."

    def Setup(self):
        # Stop duplicate requests
        if self.suggestion_was_pressed:
            return
        
        # Timer setup again
        if self._debounce_event:
            self._debounce_event.cancel()
        self._debounce_event = Clock.schedule_once(lambda dt: self.make_request_when_ready(), 0.9)

    def make_request_when_ready(self):
        now = time.time()
        # Timer setup again
        if now - self._last_request_time < 2.5:
            return
        self._last_request_time = now

        # Show loading spinner
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.City,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def City(self): # For text input typing
        Request_City(self)

    # Fill text input when address button is pressed
    def on_address_button_press(self, text):
        # Ignore placeholder text
        if text == "Start typing" or text == "No results found.":
             return
        
        # Fill the text field
        self.suggestion_was_pressed = True
        self.ids.address_input.text = text

    def countinue_pressed(self):
        # Only submit if city was found
        if not self.city_found == True:
            return 

        # Show loading spinner
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.save_location,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_firestore, 0.1)

    def save_location(self):
        self.add_other = True

        if self.city_number == 2:
            self.add_2 = True
        elif self.city_number == 3:
            self.add_3 = True

        save_location_request(self)
        location_input = str(self.ids.address_input.text.strip())
        # Save city to local session
        save_city(location_input, self.city_number)
        # Schedule UI work on main thread to dismiss modal and refresh
        try:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.on_saved(), 0)
        except Exception:
            pass
        self.dismissed = True

    def stop_load(self, *args):
        # Check if background task finished
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0
        
    def stop_load_firestore(self, *args):
        # Check if background task finished
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_firestore)
        self.ids.loader.opacity = 0
        if self.dismissed == True:
            # For backward compatibility
            try:
                self.dismiss()
            except Exception:
                pass
            try:
                self.city.start_load_weather()
            except Exception:
                pass

    def on_saved(self, *args):
        self.dismiss()
        self.city.start_load_weather()
        self.dismissed = False