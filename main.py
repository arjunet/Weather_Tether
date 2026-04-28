# Import all necessary system files
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# Kivy imports
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.lang import Builder
from kivy.core.window import Window

# Soft Input Config (For keyboard issue on android 15+):
def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"
Window.on_restore(Clock.schedule_once(set_softinput, 0.1))

# Carbon Kivy imports
from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.utils import _Dict, update_system_ui

# helper imports
from helpers.notification import notification_error, notification_success, forgot_notification
from helpers.token_management import save_refresh_token, load_refresh_token, clear_refresh_token, refresh_login, login_request_token
from helpers.signup import Signup_request
from helpers.login import Login_request
from helpers.forgot import Send_Forgot_Email
from helpers.setup import Request_City, save_location_request
from helpers.app import get_dat, get_user_weather, update_ui_labels, update_ui_background, save_city, get_new_device_data, delete_city_request, is_valid_email
from helpers.verify import Send_Verification, check_verification
from helpers.settings import delete_request, save_toggle_state, clear_json

from helpers.sidepanel import CityPanelItem
from helpers.modal_loader import ModalLoader
from helpers.modals import ChangeLocationModal, LogoutModal, DeleteModal, DeleteLocationModal, AddCityModal

# load other classes kv
Builder.load_file("helpers/sidepanel.kv")
Builder.load_file("helpers/modal_loader.kv")


# other imports
import time
import threading
import weakref
# ---------------------------------------------------------------------------------
class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Reset variables
        self.r = None

    # Check user input
    def start_load(self, email_input, password_input):
        if not email_input.strip() or not password_input.strip():
            notification_error(subtitle="Please type in all fields").open()
            return
        
        elif not is_valid_email(email_input):
            notification_error(subtitle="Please enter a valid email address").open()
            return
        
        # Show loading spinner
        self.ids.loader.opacity = 1

        # Reset variables
        self.signup_r = None
        self.signup_result = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.signup, 
            args=(email_input, password_input), 
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def signup(self, email_input, password_input):
        # Sign up the user
        Signup_request(self, email_input, password_input)

    def stop_load(self, *args):
        # Check if background task finished
        if self.signup_result is None:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        # Get signup results for notifications
        r = self.signup_r
        result = self.signup_result
        
        # Handle errors
        if r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "EMAIL_EXISTS":
                notification_error(subtitle="User Already Exists").open()
                return
            
            elif "WEAK_PASSWORD" in error_code:
                notification_error(subtitle="Please Choose A stronger Password").open()
                return
            
        # Handle success
        if r.status_code == 200:
            notification_success(subtitle="Successfully Signed Up").open()
            self.manager.current = "Setup"
# ---------------------------------------------------------------------------------
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Reset variables
        self.r = None

    def start_load(self, email_input, password_input):
        if not email_input.strip() or not password_input.strip():
            notification_error(subtitle="Please type in all fields").open()
            return
        
        elif not is_valid_email(email_input):
            notification_error(subtitle="Please enter a valid email address").open()
            return
        
        # Show loading spinner
        self.ids.loader.opacity = 1

        # Reset variables
        self.login_r = None
        self.login_result = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.Login, 
            args=(email_input, password_input), 
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def Login(self, email_input, password_input):  
        Login_request(self, email_input, password_input)

    def stop_load(self, *args):
        # Check if background task finished
        if self.login_result is None:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        # Get login results for notifications
        r = self.login_r
        result = self.login_result

        # Handle errors
        if r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "INVALID_LOGIN_CREDENTIALS":
                notification_error(subtitle="Invalid Email or Password").open()
                return

        # Handle success
        if r.status_code == 200:
            self.manager.refresh_token = result["data"]["refreshToken"]
            self.manager.id_token = result["data"]["idToken"]

            save_refresh_token(self.manager.refresh_token)
            # Go to the main app screen
            self.manager.current = "App"
# ---------------------------------------------------------------------------------
class ForgotScreen(Screen):
    def start_load(self, email_input):
        if not email_input.strip():
            notification_error(subtitle="Please type in all fields").open()
            return
        
        elif not is_valid_email(email_input):
            notification_error(subtitle="Please enter a valid email address").open()
            return
        
        # Show loading spinner
        self.ids.loader.opacity = 1

        # Reset result variables so that the waiter can check for them
        self.forgot_r = None
        self.forgot_result = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.forgot, 
            args=(email_input,), 
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def forgot(self, email_input):   
        Send_Forgot_Email(self, email_input)
            
    def stop_load(self, *args):
        # Check if background task finished
        if self.forgot_result is None:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        # Get results for notifications
        r = self.forgot_r
        result = self.forgot_result
        
        # Handle errors
        if r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "INVALID_EMAIL":
                notification_error(subtitle="User Does Not Exist").open()
                return
            
        # Handle success
        if r.status_code == 200:
            forgot_notification().open()
# ---------------------------------------------------------------------------------
class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.suggestion_was_pressed = False
        # Timer setup
        self._last_request_time = 0
        self._debounce_event = None  

        # Reset location variables
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.city_found = False
        self.add_other = False
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

    def City(self):
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
        save_location_request(self)

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

        location_input = self.ids.address_input.text.strip()
        save_city(location_input, 1)

        self.manager.current = "App"
# ---------------------------------------------------------------------------------
class VerifyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.r = None
        self.result = None
        self.email_verified = None
        self.done = False
        self.ids.resend_button.disabled = True

    def on_enter(self):
        Clock.schedule_once(self.show_button, 5)

    def show_button(self, dt):
        self.ids.resend_button.disabled = False
        self.ids.resend_button.opacity = 1

    def start_load_send(self):
        # Show loading spinner
        self.ids.loader.opacity = 1

        self.r = None
        self.result = None
        self.email_verified = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.Send_verification_Email,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_send, 0.1)

    def start_load_check(self):
        # Show loading spinner
        self.ids.loader.opacity = 1

        self.r = None
        self.result = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.check,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_check, 0.1)

    def Send_verification_Email(self):
        Send_Verification(self)

    def check(self):
        check_verification(self)
     
    def stop_load_send(self, *args):
        if self.r is None:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_send)
        self.ids.loader.opacity = 0

        r = self.r
        result = self.result

        error_code = result.get("detail", "")
        print(error_code)

        if error_code == "TOO_MANY_ATTEMPTS_TRY_LATER":
            notification_error(subtitle="Email should already be in your inbox. If you don't see it, try checking your spam").open()

        elif r.status_code == 200:
            notification_success(subtitle="Verification email successfully sent. If you dont see it try checking your spam. Click on the link to verify your email.").open()
            
    def stop_load_check(self, *args):  
        if self.email_verified is None:
            return True # Keep waiting
        
        if self.done != True:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_check)
        self.ids.loader.opacity = 0

        if self.email_verified == True:
            # Add a coming from verify so that the app screen will not malfunction
            self.manager.coming_from_verify = True
            self.manager.current = "App"
            notification_success(subtitle="Email verified successfully").open()

        # Handle errors
        elif self.email_verified == False:
            notification_error(subtitle="Email is not verified").open()
            
        self.email_verified = None
# ---------------------------------------------------------------------------------
class AppScreen(Screen):
    # Default background image
    bg_image = StringProperty("")
    icon_path = StringProperty("")

    def __init__(self, **kw):
        super().__init__(**kw)
        # Set default values to avoid Kivy warnings
        self.r = None
        self.result = None
        self.go_to_verify = False
        self.current_temp = None
        self.feels_like = None
        self.is_daytime = False
        self.min_temp = None
        self.max_temp = None
        self.precip_percent = None
        self.precip_type = None
        self.snow_fall = None
        self.thunderstorm_prob = None
        self.weather_condition = None
        self.wind_chill = None
        self.get_3 = False
        self.get_2 = False

    def on_enter(self):
        store = JsonStore('session.json')
        self.toggle_state = store.get('toggle')['active'] if store.exists('toggle') else False

        # Show loading spinner
        self.ids.loader.opacity = 1

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.login,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def login(self):
        login_request_token(self)

    def stop_load(self, *args):
        if self.r is None:
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        if self.go_to_verify==True:
            Clock.unschedule(self.stop_load)
            self.ids.loader.opacity = 0
            self.manager.current = "Verify"

        # If everything is good, load the weather data
        else:
            self.r = None
            self.start_load_weather()
    
    def start_load_weather(self):
        # Show loading spinner
        self.ids.loader.opacity = 1

        self.r = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.get_user_dat,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_weather, 0.1)

    def get_user_dat(self):
        get_dat(self)

    def get_weather(self, lat, lon):
        get_user_weather(self, lat, lon)
        store = JsonStore('session.json')

        if not store.exists("city1"):
            get_new_device_data(self)

    def stop_load_weather(self, *args):
        # Check if weather data loaded
        if self.r != "weather_done":
            return True # Keep waiting
        
        # Hide spinner and handle response
        Clock.unschedule(self.stop_load_weather)
        self.ids.loader.opacity = 0
        self.update_labels()
        self.update_background()

    def update_labels(self):
        update_ui_labels(self)

        file = JsonStore("session.json")
        sidepanel = self.ids.SidePanel
        widget_container = sidepanel.ids.widgets

        # Clear existing city widgets before adding new ones
        widget_container.clear_widgets()

        def add_city_item(city_key, target_screen):
            if file.exists(city_key):
                city_name = file.get(city_key)["name"]
                item = CityPanelItem(text=city_name, right_icon="location")
                item.bind(on_press=lambda instance, screen=target_screen: setattr(self.manager, "current", screen))
                widget_container.add_widget(item)

        add_city_item("city1", "App")
        add_city_item("city2", "City2")
        add_city_item("city3", "City3")

    def update_background(self):
        update_ui_background(self)

    def open_change_location_modal(self) -> None:
        modal = ChangeLocationModal(city=self, update_type=1)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None
# ---------------------------------------------------------------------------------
class City2Screen(Screen):
    icon_path = StringProperty("")
    bg_image = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.r = None
        self.result = None
        self.go_to_verify = False

        # Add null values so kivy will be quiet:
        self.current_temp = None
        self.feels_like = None
        self.is_daytime = False
        self.min_temp = None
        self.max_temp = None
        self.precip_percent = None
        self.precip_type = None
        self.snow_fall = None
        self.thunderstorm_prob = None
        self.weather_condition = None
        self.wind_chill = None
        self.delete_done = None
        self.delete_2 = False
        self.delete_3 = False

    # Runs every time you enter this screen
    def on_enter(self):
        store = JsonStore('session.json')
        self.toggle_state = store.get('toggle')['active'] if store.exists('toggle') else False

        if not store.exists("city2"):
            self.open_add_modal()

        else:
            self.start_load_weather()

    def start_load_weather(self):
        self.get_2 = True
        self.get_3 = False
        # Show loading spinner
        self.ids.loader.opacity = 1

        self.r = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.get_user_dat,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_weather, 0.1)

    def get_user_dat(self):
        get_dat(self)

    def get_weather(self, lat, lon):
        get_user_weather(self, lat, lon)  

    def stop_load_weather(self, *args):
        # If weather has not been fetched yet:
        if self.r != "weather_done":
            return True # Keep waiting
        
        # Stops thread once done:
        Clock.unschedule(self.stop_load_weather)
        self.ids.loader.opacity = 0
        self.update_labels()
        self.update_background()

    def update_labels(self):
        update_ui_labels(self)
        
        file = JsonStore("session.json")
        sidepanel = self.ids.SidePanel
        widget_container = sidepanel.ids.widgets

        # Remove any existing dynamic city widgets before adding fresh ones.
        widget_container.clear_widgets()

        def add_city_item(city_key, target_screen):
            if file.exists(city_key):
                city_name = file.get(city_key)["name"]
                item = CityPanelItem(text=city_name, right_icon="location")
                item.bind(on_press=lambda instance, screen=target_screen: setattr(self.manager, "current", screen))
                widget_container.add_widget(item)

        add_city_item("city1", "App")
        add_city_item("city2", "City2")
        add_city_item("city3", "City3")

    def update_background(self):
        update_ui_background(self)

    def open_add_modal(self) -> None:
        modal = AddCityModal(city=self, city_number=2)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None

    def open_change_location_modal(self) -> None:
        modal = ChangeLocationModal(city=self, update_type=2)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None

    def open_delete_location_modal(self) -> None:
        self.delete_modal = DeleteLocationModal(city_name="city2", screen_instance=self)
        self._modal_ref = weakref.ref(self.delete_modal)
        self.delete_modal.open()
        self._modal_ref = None

    def start_delete_city(self):
        self.modal_loader = ModalLoader()

        self.delete_2 = True
        self.delete_modal.add_widget(self.modal_loader)

        threading.Thread(
            target=self.delete_city_request,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_delete_city, 0.1)

    def delete_city_request(self):
        self.delete_2 = True
        delete_city_request(screen_instance=self, app_instance=self.manager)

    def stop_delete_city(self, *args):
        if self.delete_done != "done":
            return True
    
        Clock.unschedule(self.stop_delete_city)
        self.delete_modal.remove_widget(self.modal_loader)
        self.delete_modal.dismiss()

        self.manager.current = "App"
        notification_success(subtitle="Successfully Deleted City").open()
# ---------------------------------------------------------------------------------
class City3Screen(Screen):
    icon_path = StringProperty("")
    bg_image = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.r = None
        self.result = None
        self.go_to_verify = False

        # Add null values so kivy will be quiet:
        self.current_temp = None
        self.feels_like = None
        self.is_daytime = False
        self.min_temp = None
        self.max_temp = None
        self.precip_percent = None
        self.precip_type = None
        self.snow_fall = None
        self.thunderstorm_prob = None
        self.weather_condition = None
        self.wind_chill = None
        self.delete_2 = False
        self.delete_3 = False

    # Runs every time you enter this screen
    def on_enter(self):
        store = JsonStore('session.json')
        self.toggle_state = store.get('toggle')['active'] if store.exists('toggle') else False

        if not store.exists("city3"):
            self.open_add_modal()

        self.start_load_weather()

    def start_load_weather(self):
        self.get_2 = False
        self.get_3 = True
        # Show loading spinner
        self.ids.loader.opacity = 1

        self.r = None

        # Run in background to keep UI responsive
        threading.Thread(
            target=self.get_user_dat,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_weather, 0.1)

    def get_user_dat(self):
        get_dat(self)

    def get_weather(self, lat, lon):
        get_user_weather(self, lat, lon) 

    def stop_load_weather(self, *args):
        # If weather has not been fetched yet:
        if self.r != "weather_done":
            return True # Keep waiting
        
        # Stops thread once done:
        Clock.unschedule(self.stop_load_weather)
        self.ids.loader.opacity = 0
        self.update_labels()
        self.update_background()

    def update_labels(self):
        update_ui_labels(self)
        
        file = JsonStore("session.json")
        sidepanel = self.ids.SidePanel
        widget_container = sidepanel.ids.widgets

        # Remove any existing dynamic city widgets before adding fresh ones.
        widget_container.clear_widgets()

        def add_city_item(city_key, target_screen):
            if file.exists(city_key):
                city_name = file.get(city_key)["name"]
                item = CityPanelItem(text=city_name, right_icon="location")
                item.bind(on_press=lambda instance, screen=target_screen: setattr(self.manager, "current", screen))
                widget_container.add_widget(item)

        add_city_item("city1", "App")
        add_city_item("city2", "City2")
        add_city_item("city3", "City3")

    def update_background(self):
        update_ui_background(self)

    def open_add_modal(self) -> None:
        modal = AddCityModal(city=self, city_number=3)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None

    def open_change_location_modal(self) -> None:
        modal = ChangeLocationModal(city=self, update_type=3)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None

    def open_delete_location_modal(self) -> None:
        modal = DeleteLocationModal(city_name="city3", screen_instance=self)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None

    def start_delete_city(self):
        self.delete_3 = True
        delete_city_request(screen_instance=self, app_instance=self.manager)
# ---------------------------------------------------------------------------------
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response = None
        self.login_result = None

    def on_enter(self, *args):
        # Load toggle state from session file
        store = JsonStore('session.json')
        toggle_state = store.get('toggle')['active'] if store.exists('toggle') else False
        self.ids.unit_toggle.active = toggle_state

    def logout(self):
        clear_refresh_token()
        store = JsonStore("session.json")
        store.clear()
        self.manager.current = "Signup"
        notification_success(subtitle="Successfully Logged out").open()

    def start_delete_account(self, email_input, password_input):
        self.email_input = email_input
        self.password_input = password_input
        self.ids.loader.opacity = 1
        
        # Reset result variables
        self.delete_r = None
        self.delete_result = None

        # Run in background
        threading.Thread(
            target=self.delete_user_dat, 
            daemon=True
        ).start()
        
        # Check for completion
        Clock.schedule_interval(self.stop_delete_load, 0.1)

    def delete_user_dat(self):
        Login_request(self, self.email_input, self.password_input)
        delete_request(self)

    def stop_delete_load(self, *args):
        if self.delete_result is None or self.login_result is None:
            return True  # Keep waiting

        Clock.unschedule(self.stop_delete_load)
        self.ids.loader.opacity = 0

        # Get login results for notifications
        r = self.login_r
        result = self.login_result

        # Check user input
        if not self.email_input.strip() or not self.password_input.strip():
            self.ids.loader.opacity = 0
            notification_error(subtitle="Please type in all fields").open()
            return

        # Handle errors
        if r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "INVALID_LOGIN_CREDENTIALS":
                notification_error(subtitle="Invalid Email or Password").open()
                return
            
            elif error_code == "INVALID_EMAIL":
                notification_error(subtitle="Invalid Email Format").open()
                return

        else:
            clear_json()
            self.manager.id_token = None
            self.manager.refresh_token = None
            
            # Go back to signup
            self.manager.current = "Signup"
            
            notification_success(subtitle="Successfully Deleted Account").open()

    def toggle_pressed(self):
        toggle_state = self.ids.unit_toggle.active
        save_toggle_state(toggle_state)

    def open_add_city_modal(self):
        file = JsonStore("session.json")

        if not file.exists("city2"):
            self.manager.current = "City2"

        elif not file.exists("city3"):
            self.manager.current = "City3"

    def open_logout_modal(self) -> None:
        modal = LogoutModal(settings=self)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None

    def open_delete_modal(self) -> None:
        modal = DeleteModal(settings=self)
        self._modal_ref = weakref.ref(modal)
        modal.open()
        self._modal_ref = None
        modal = None
# ---------------------------------------------------------------------------------
# Build and run the app
class MainApp(CarbonApp):
    Window = Window
    def __init__(self, *args, **kwargs) -> None:
        self.defaults = False
        super().__init__(*args, **kwargs)
        
    def build(self):
        # Set light mode
        Window.clearcolor = (1, 1, 1, 1)

        # Set up screen manager
        self.sm = CScreenManager()
        self.sm.add_widget(SignupScreen(name='Signup'))
        self.sm.add_widget(LoginScreen(name='Login'))
        self.sm.add_widget(ForgotScreen(name='Forgot'))
        self.sm.add_widget(SetupScreen(name='Setup'))
        self.sm.add_widget(AppScreen(name='App'))
        self.sm.add_widget(VerifyScreen(name='Verify'))
        self.sm.add_widget(SettingsScreen(name='Settings'))
        self.sm.add_widget(City2Screen(name='City2'))
        self.sm.add_widget(City3Screen(name='City3'))
        return self.sm

    def on_start(self):
        token = load_refresh_token()

        if token:
            result = refresh_login(token)

            if result:
                self.sm.id_token = result["idToken"]
                self.sm.refresh_token = result["refreshToken"]

                # Save new token
                save_refresh_token(result["refreshToken"])

                if result.get("emailVerified") is True:
                    self.sm.current = "App"

                else:
                    self.sm.current = "Verify"
                return
            else:
                clear_refresh_token()

        self.sm.current = "Signup"

    def on_theme(self, *args) -> None:
        super(CarbonApp, self).on_theme(*args)
        self.apply_styles()

    def apply_styles(self, *args) -> None:
        Window.clearcolor = self.background
        icon_style = "Dark" if self.theme in ["Gray100"] else "White"
        update_system_ui(self.background, self.background, icon_style=icon_style, pad_nav=True)

if __name__ == "__main__":
    MainApp().run()