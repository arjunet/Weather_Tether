# Imports:
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

# Soft Input Config (for edge-to-edge displays on Android):
def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"
Window.on_restore(Clock.schedule_once(set_softinput, 0.1))

from carbonkivy.app import CarbonApp
from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.uix.notification import CNotificationInline

import requests
import json
import time

# ---------------------------------------------------------------------------------

# Firebase Cofig:
class FirebaseAuth:
    def __init__(self, api_key):
        self.api_key = api_key
        self.signup_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
        self.login_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
firebase = FirebaseAuth("AIzaSyDpMQo5r4gHxQHMAy9niIUjs9kgerBf5pI")

# ---------------------------------------------------------------------------------

class SignupScreen(Screen):
    def Signup(self, email_input, password_input):
        # Client Validation:
        if email_input == "" or password_input == "":
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Please type in all fields",
                status="Error",
            ).open()
            )
            return
        
        elif "@" not in email_input:
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Invalid Email Format",
                status="Error",
            ).open()
            )
            return
        
        payload = {
            "email": email_input,
            "password": password_input,
        }
        r = requests.post(firebase.signup_url, json=payload)
        result = r.json()

        if "idToken" in result:
            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully signed up",
                status="Success",
            ).open()
        )
            self.manager.current = "Setup"

        # Error Notifications:  
        elif "EMAIL_EXISTS" in result.get("error", {}).get("message", ""):
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="User already exists",
                status="Error",
            ).open()
            )
            return
        
        else:
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Server Error, please try again later",
                status="Error",
            ).open()
            )
            return
        

# ---------------------------------------------------------------------------------

class LoginScreen(Screen):
    def Login(self, email_input, password_input):
        # Client Validation:
        if email_input == "" or password_input == "":
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Please type in all fields",
                status="Error",
            ).open()
            )
            return
        
        elif "@" not in email_input:
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Invalid Email Format",
                status="Error",
            ).open()
            )
            return
        
        payload = {
            "email": email_input,
            "password": password_input,
        }
        r = requests.post(firebase.login_url, json=payload)
        result = r.json()

        if "idToken" in result:
            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully logged in",
                status="Success",
            ).open()
        )

        # Error Notification:  
        elif r.status_code == 400:
                self.notification = CNotificationInline(
                    title="Error",
                    subtitle="Invalid password or server error",
                    status="Error",
                ).open()

# ---------------------------------------------------------------------------------

class ForgotScreen(Screen):
    def Send_Forgot_Email(self):
        pass

# ---------------------------------------------------------------------------------

class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Timer Config:
        self._last_request_time = 0
        self._debounce_event = None  

    def Setup(self):
        # Timer Config (again):
        if self._debounce_event:
            self._debounce_event.cancel()
        self._debounce_event = Clock.schedule_once(lambda dt: self.make_request_when_ready(), 0.9)

    def make_request_when_ready(self):
        now = time.time()
        # Timer Config (again):
        if now - self._last_request_time < 2.5:
            return
        self._last_request_time = now
        self.Request_City()

    def Request_City(self): # Text is here for the text typing on textinput field
        # Variable for Search Query of city:
        search_query = self.ids.address_input.text.strip() 

        # Request for JSON and raise exceptions on errors:

        # Api url (google cloud run):
        url = f"https://maps-backend-318359636878.us-central1.run.app/places?query={search_query}"

        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            if data.get("results"):
                formatted_address = data["results"][0].get("formatted_address")
                self.ids.address_button.disabled = False
                self.ids.address_button.text = formatted_address

            else:
                self.ids.address_button.disabled = True
                self.ids.address_button.text = "No results found."
     
        # Error Handling:
        except requests.exceptions.RequestException:
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Network error occurred",
                status="Error",
            ).open()
            )
            return

        except json.JSONDecodeError:
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Error reading server responce",
                status="Error",
            ).open()
            )
            return

    # Fills in to textinput fild when address button is pressed:
    def on_address_button_press(self, text):
        # ignore if it's still the placeholder text
        if text == "Start typing" or text == "No results found.":
             return
    
        # otherwise, fill the text field
        self.ids.address_input.text = text

# ---------------------------------------------------------------------------------

# Build And Run The App:
class MainApp(CarbonApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def build(self):
        # Light Mode:
        Window.clearcolor = (1, 1, 1, 1)

        # Screen Manager Config:
        sm = CScreenManager()
        sm.add_widget(SignupScreen(name='Signup'))
        sm.add_widget(LoginScreen(name='Login'))
        sm.add_widget(ForgotScreen(name='Forgot'))
        sm.add_widget(SetupScreen(name='Setup'))
        return sm

if __name__ == "__main__":
    MainApp().run()