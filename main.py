# Imports:
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

from carbonkivy.app import CarbonApp
from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.uix.notification import CNotificationInline, CNotificationToast

import requests
import json
import time

# ---------------------------------------------------------------------------------

class SignupScreen(Screen):
    def Signup(self, email_input, password_input):
        url = "https://firebase-hash-service-318359636878.us-central1.run.app/register"
        data = {"email": email_input, "password": password_input}
        r = requests.post(url, json=data)
        print(r.json())

# ---------------------------------------------------------------------------------

class LoginScreen(Screen):
    def Login(self, email_input, password_input):
        # API Request to login user:
        url = "https://firebase-hash-service-318359636878.us-central1.run.app/login"
        data = {"email": email_input, "password": password_input}
        r = requests.post(url, json=data)
        print(r.json())

        # Success Notification:
        result = r.json()
        if result.get("success"):
            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully signed in",
                status="Success",
            ).open()
        )

        # Error Notification:   
        else:
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Invalid email or password",
                status="Error",
            ).open()
        )

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
                print(formatted_address)
                self.ids.address_button.disabled = False
                self.ids.address_button.text = formatted_address

            else:
                self.ids.address_button.disabled = True
                self.ids.address_button.text = "No results found."
     
        # Error Handling:
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")

        except json.JSONDecodeError:
            print("Error decoding JSON response.")

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
