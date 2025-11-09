# Imports:

from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

from carbonkivy.app import CarbonApp
from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager

import requests
import json
import time


# Screen Python Code:
class SignupScreen(Screen):
    def Signup(self):
        pass

class LoginScreen(Screen):
    def Login(self):
        pass

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

    def Setup(self, text):
        # Timer Config (again):
        if self._debounce_event:
            self._debounce_event.cancel()
        self._debounce_event = Clock.schedule_once(lambda dt: self.make_request_when_ready(text), 0.9)

    def make_request_when_ready(self, text):
        now = time.time()
        # Timer Config (again):
        if now - self._last_request_time < 4:
            return
        self._last_request_time = now
        self.Request_City(text)
        self.ids.address_button.disabled = False

    def Request_City(self, text): # Text is here for the text typing on textinput field
        # Variable for Search Query of city:
        search_query = text.strip() 

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
                self.ids.address_button.text = formatted_address
     
        # Error Handling:
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")

        except json.JSONDecodeError:
            print("Error decoding JSON response.")

    # Fills in to textinput fild when address button is pressed:
    def on_address_button_press(self, text):
        # ignore if it's still the placeholder text
        if text == "Start typing":
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
