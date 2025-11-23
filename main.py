# Imports:
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

# Soft Input Config (for edge-to-edge displays on Android, must come before carbonkivy imports):
def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"
Window.on_restore(Clock.schedule_once(set_softinput, 0.1))

from carbonkivy.app import CarbonApp
from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.uix.notification import CNotificationInline

import requests
import time

# ---------------------------------------------------------------------------------
 # Firebase Auth Service URL:
FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

# ---------------------------------------------------------------------------------

class SignupScreen(Screen):
    def Signup(self, email_input, password_input):
        # Client Validation:
        if email_input == "" or password_input == "":
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Please Type In All Fields",
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
        
        # Server Request:
        url = f"{FIREBASE_URL}/signup"
        payload = {
            "email": email_input,
            "password": password_input
       }
        r = requests.post(url, json=payload)
        result = r.json() 

        # Success Notification:
        if r.status_code == 200:
            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully Signed Up",
                status="Success",
            ).open()
        )
            self.manager.current = "Setup"

        # Error Notifications:  
        elif r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "EMAIL_EXISTS":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="User Already Exists",
                    status="Error",
                ).open()
                )
                return
            
            elif error_code == "WEAK_PASSWORD":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Password Is Too Weak",
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
                subtitle="Please Type In All Fields",
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
        
        # Server Request:
        url = f"{FIREBASE_URL}/login"
        payload = {
            "email": email_input,
            "password": password_input
       }
        r = requests.post(url, json=payload)
        result = r.json()

        # Success Notification:
        if r.status_code == 200:
            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully Logged In",
                status="Success",
            ).open()
        )
            self.manager.current = "Setup"

        # Error Notifications:  
        elif r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "EMAIL_EXISTS":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="User Already Exists",
                    status="Error",
                ).open()
                )
                return
            
            elif error_code == "WEAK_PASSWORD":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Password Is Too Weak",
                    status="Error",
                ).open()
                )
                return

# ---------------------------------------------------------------------------------

class ForgotScreen(Screen):
    def Send_Forgot_Email(self, email_input):
        url = f"{FIREBASE_URL}/reset_password"
        payload = {"email": email_input}

        r = requests.post(url, json=payload)
        result = r.json()

        if r.status_code == 200:
            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully Sent Reset Email",
                status="Success",
            ).open()
        )
            self.manager.current = "Setup"

        # Error Notifications:  
        elif r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "INVALID_EMAIL":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Email Does Not Exist",
                    status="Error",
                ).open()
                )
                return

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

    # Fills in to textinput fild when address button is pressed:
    def on_address_button_press(self, text):
        # ignore if it's still the placeholder text
        if text == "Start typing" or text == "No results found.":
             return
        
        # otherwise, fill the text field
        self.ids.address_input.text = text

# ---------------------------------------------------------------------------------

class AppScreen(Screen):
    pass

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
        sm.add_widget(AppScreen(name='App'))
        return sm

if __name__ == "__main__":
    MainApp().run()