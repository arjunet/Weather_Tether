# Imports:
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

# Soft Input Config (For keyboard issue on android 15+):
def set_softinput(*args) -> None:
    Window.keyboard_anim_args = {"d": 0.2, "t": "in_out_expo"}
    Window.softinput_mode = "below_target"
Window.on_restore(Clock.schedule_once(set_softinput, 0.1))

from carbonkivy.app import CarbonApp
from carbonkivy.app import CarbonApp
from carbonkivy.uix.screenmanager import CScreenManager
from carbonkivy.uix.notification import CNotificationInline
from carbonkivy.uix.notification import CNotificationToast

from token_management import save_refresh_token, load_refresh_token, clear_refresh_token, refresh_login
import requests
import time
import threading

# ---------------------------------------------------------------------------------
 # Firebase Auth Service URL (global):
FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"
# ---------------------------------------------------------------------------------
class SignupScreen(Screen):
    def start_load(self, email_input, password_input):
        # Make the loader visible:
        self.ids.loader.opacity = 1

        # Reset the result variables so that the waiter can check for them (overwrite them when the thread is done):
        self.signup_r = None
        self.signup_result = None

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.Signup_request, 
            args=(email_input, password_input), 
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def Signup_request(self, email_input, password_input):
        # Server Request:
        url = f"{FIREBASE_URL}/signup"
        payload = {
            "email": email_input,
            "password": password_input
       }
        r = requests.post(url, json=payload)
        result = r.json() 

        # Declares results from signup for notifications:
        self.signup_r = r
        self.signup_result = result
        self.email_input = email_input
        self.password_input = password_input

        # If successful signup, login to get the tokens and save them for later:
        if r.status_code == 200:
            # Login after signup for token retrieval:
            login_payload = {
                "email": email_input,
                "password": password_input
            }
            login_r = requests.post(f"{FIREBASE_URL}/login", json=login_payload)
            login_res = login_r.json()

            self.manager.id_token = login_res["data"]["idToken"]
            self.manager.local_id = login_res["data"]["localId"]
            self.manager.refresh_token = login_res["data"]["refreshToken"]

            # Saves refresh token to file for autologin on app start:
            save_refresh_token(self.manager.refresh_token)

    def stop_load(self, *args):
        # Stops thread once done:
        if self.signup_result is None:
            return True # Keep waiting
        
        # Once thread done, stop the loader and show the result:
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        # Declares results from signup for notifications:
        r = self.signup_r
        result = self.signup_result
        email_input = self.email_input
        password_input = self.password_input
    
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
        
        # Error Notifications:  
        if r.status_code == 400:
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
            
            elif "WEAK_PASSWORD" in error_code:
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Password Is Too Weak",
                    status="Error",
                ).open()
                )
                return
            
            elif error_code == "INVALID_EMAIL":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Invalid Email Format",
                    status="Error",
                ).open()
                )
                return
            
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
# ---------------------------------------------------------------------------------
class LoginScreen(Screen):
    def start_load(self, email_input, password_input):
        # Make the loader visible:
        self.ids.loader.opacity = 1

        # Reset the result variables so that the waiter can check for them (overwrite them when the thread is done):
        self.login_r = None
        self.login_result = None

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.Login_request, 
            args=(email_input, password_input), 
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def Login_request(self, email_input, password_input):  
        # Server Request:
        url = f"{FIREBASE_URL}/login"
        payload = {
            "email": email_input,
            "password": password_input
       }
        r = requests.post(url, json=payload)
        result = r.json()
        data = result.get("data", {})
        email_verified = data.get("emailVerified", False)

        # Declares results from login for notifications:
        self.login_r = r
        self.login_result = result
        self.email_verified = email_verified
        self.email_input = email_input
        self.password_input = password_input

    def stop_load(self, *args):
        # Stops thread once done:
        if self.login_result is None:
            return True # Keep waiting
        
        # Once thread done, stop the loader and show the result:
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        # Declares results from login for notifications:
        r = self.login_r
        result = self.login_result
        email_verified = self.email_verified
        email_input = self.email_input
        password_input = self.password_input

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

        # Error Notifications:  
        if r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "INVALID_LOGIN_CREDENTIALS":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Invalid Email Or Password",
                    status="Error",
                ).open()
                )
                return
            
            elif error_code == "INVALID_EMAIL":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Invalid Email Format",
                    status="Error",
                ).open()
                )
                return
            
        if not email_verified:
            self.notification = (
                CNotificationInline(
                    title="Error",
                    subtitle="Please Go to Your Email And Verify Your Account Before Logging In.",
                    status="Error",
                ).open()
            )
            return

        # Success Notification:
        if r.status_code == 200:
            self.manager.refresh_token = result["data"]["refreshToken"]
            self.manager.id_token = result["data"]["idToken"]

            self.notification = (
                CNotificationInline(
                title="Success",
                subtitle="Successfully Logged In",
                status="Success",
            ).open()
        ) 

            save_refresh_token(self.manager.refresh_token)
            # Go to the main app screen:
            self.manager.current = "App"

# ---------------------------------------------------------------------------------
class ForgotScreen(Screen):
    def start_load(self, email_input):
        # Make the loader visible:
        self.ids.loader.opacity = 1

        # Reset the result variables so that the waiter can check for them (overwrite them when the thread is done):
        self.forgot_r = None
        self.forgot_result = None

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.Send_Forgot_Email, 
            args=(email_input,), 
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def Send_Forgot_Email(self, email_input):   
        # Server Request:
        url = f"{FIREBASE_URL}/reset_password"
        payload = {"email": email_input}
        r = requests.post(url, json=payload)
        result = r.json()

        # Declares results from sending for notifications:
        self.forgot_r = r
        self.forgot_result = result
        self.email_input = email_input
            
    def stop_load(self, *args):
        # Stops thread once done:
        if self.forgot_result is None:
            return True # Keep waiting
        
        # Once thread done, stop the loader and show the result:
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        # Declares results from sending for notifications:
        r = self.forgot_r
        result = self.forgot_result
        email_input = self.email_input

        # Client Validation:
        if email_input == "":
            self.notification = (
                CNotificationInline(
                title="Error",
                subtitle="Please Type In All Fields",
                status="Error",
            ).open()
            )
            return
        
        # Error Notification:  
        if r.status_code == 400:
            error_code = result.get("detail", "")

            if error_code == "INVALID_EMAIL":
                self.notification = (
                    CNotificationInline(
                    title="Error",
                    subtitle="Invalid Email Format",
                    status="Error",
                ).open()
                )
                return
            
        # Success Notification:
        if r.status_code == 200:
            self.notification = (
                CNotificationToast(
                title="Success",
                subtitle="Successfully Sent Reset Email. If You Don't See It, Check Your Spam Folder. If You Still Don't See It, The Email May Not Be Registered.",
                status="Success",
                pos_hint={"center_x": 0.5, "y": 0.57},
            ).open()
        )
# ---------------------------------------------------------------------------------
class SetupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.suggestion_was_pressed = False
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

        # Make the loader visible:
        self.ids.loader.opacity = 1

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.Request_City,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

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

    # Button config for countinuing to app:
    def suggestion_pressed(self):
        self.suggestion_was_pressed = True

    def countinue_pressed(self):
        if not self.suggestion_was_pressed == True:
            return

        # Make the loader visible:
        self.ids.loader.opacity = 1

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.save_location,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_firestore, 0.1)

    def save_location(self):
        # Sends the location to Firestore:
        location_input = self.ids.address_input.text
        id_token = self.manager.id_token
        payload = {"location": location_input}
        headers = {"Authorization": f"Bearer {id_token}"}
        r = requests.post(f"{FIREBASE_URL}/save_location", json=payload, headers=headers)
        print(r.json())

    def stop_load(self, *args):
        # Stops thread once done:
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Once thread done, stop the loader and show the result:
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0
        
    def stop_load_firestore(self, *args):
        # Stops thread once done:
        if self.ids.address_button.text.strip() == "Start typing":
            return True # Keep waiting
        
        # Once thread done, stop the loader and show the result:
        Clock.unschedule(self.stop_load_firestore)
        self.ids.loader.opacity = 0

        self.manager.current = "App"
# ---------------------------------------------------------------------------------
class VerifyScreen(Screen):
    def start_load_send(self):
        # Make the loader visible:
        self.ids.loader.opacity = 1

        self.r = None
        self.result = None
        self.email_verified = None

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.Send_Verification_Email,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_send, 0.1)

    def start_load_check(self):
        # Make the loader visible:
        self.ids.loader.opacity = 1

        self.r = None
        self.result = None

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.check_verification,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load_check, 0.1)

    def Send_Verification_Email(self):
        url = f"{FIREBASE_URL}/resend_verification"
        id_token = self.manager.id_token

        payload = {"id_token": id_token}
    
        r = requests.post(url, json=payload, timeout=10)
        print(r.json())
        result = r.json()
        self.r = r
        self.result = result
        
        # Check the response
        if r.status_code == 200:
            print("Email resent successfully!")
            print(r.json())

    def check_verification(self, *args):
        token = load_refresh_token()

        self.email_verified = None

        if token:
            result = refresh_login(token)

            if result:
                self.manager.id_token = result["idToken"]
                self.manager.refresh_token = result["refreshToken"]

                # save new token
                save_refresh_token(result["refreshToken"])

                if result.get("emailVerified") is True:
                    self.email_verified = True

                else:
                    self.email_verified = False

    def stop_load_send(self, *args):
        if self.r is None:
            return True # Keep waiting
        
        # Stops thread once done:
        Clock.unschedule(self.stop_load_send)
        self.ids.loader.opacity = 0

        r = self.r
        result = self.result

        error_code = result.get("detail", "")
        print(error_code)

        if error_code == "TOO_MANY_ATTEMPTS_TRY_LATER":
            print("Too many attempts. Please try again later.")
            self.notification = (
                CNotificationToast( 
                title="Error",
                subtitle="Email verification email should already be in your email inbox. If you don't see it, check your spam folder.",
                status="Error",
                pos_hint={"center_x": 0.5, "y": 0.57},
                ).open()
            )

        elif r.status_code == 200:
            self.notification = (
                CNotificationToast(
                title="Success",
                subtitle="Verification Email Sent Successfully. Please Check Your Email And Click The Link To Verify Your Account.",
                status="Success",
                pos_hint={"center_x": 0.5, "y": 0.57},
                ).open()
            )
            
    def stop_load_check(self, *args):   
        if self.email_verified is None:
            return True # Keep waiting 
        
        # Stops thread once done:
        Clock.unschedule(self.stop_load_check)
        self.ids.loader.opacity = 0

        email_verified = self.email_verified

        if email_verified == True:
            self.notification = (
                    CNotificationToast(
                    title="Success",
                    subtitle="Email Verified Successfully",
                    status="Success",
                    pos_hint={"center_x": 0.5, "y": 0.57},
                    ).open()
                )
            self.manager.current = "App"

        elif email_verified == False:
            self.notification = (
                        CNotificationToast(
                        title="Error",
                        subtitle="Email Not Verified Yet. Please Check Your Email And Spam Email And Click The Link To Verify",
                        status="Error",
                        pos_hint={"center_x": 0.5, "y": 0.57},
                        ).open()
                    )
# ---------------------------------------------------------------------------------
class AppScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.r = None
        self.result = None
        self.go_to_verify = False

    def on_enter(self):
        # Make the loader visible:
        self.ids.loader.opacity = 1

        # Start the thread so ui can load while waiting for the server response:
        threading.Thread(
            target=self.login,
            daemon=True
        ).start()
        Clock.schedule_interval(self.stop_load, 0.1)

    def login(self):
        token = load_refresh_token()

        if token:
            result = refresh_login(token)

            if result:
                self.manager.id_token = result["idToken"]
                self.manager.refresh_token = result["refreshToken"]

                # save new token
                save_refresh_token(result["refreshToken"])

                if result.get("emailVerified") is True:
                    self.go_to_verify = False

                else:
                    self.go_to_verify = True

        self.r = "done"
            
    def stop_load(self, *args):
        if self.r is None:
            return True # Keep waiting
        
        # Stops thread once done:
        Clock.unschedule(self.stop_load)
        self.ids.loader.opacity = 0

        if self.go_to_verify==True:
            Clock.unschedule(self.stop_load)
            self.ids.loader.opacity = 0
            print ("if statement passed")

            self.manager.current = "Verify"
        
        self.r = None
        return False
# ---------------------------------------------------------------------------------
# Build And Run The App:
class MainApp(CarbonApp):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
    def build(self):
        # Light Mode:
        Window.clearcolor = (1, 1, 1, 1)

        # Screen Manager Config:
        self.sm = CScreenManager()
        self.sm.add_widget(SignupScreen(name='Signup'))
        self.sm.add_widget(LoginScreen(name='Login'))
        self.sm.add_widget(ForgotScreen(name='Forgot'))
        self.sm.add_widget(SetupScreen(name='Setup'))
        self.sm.add_widget(AppScreen(name='App'))
        self.sm.add_widget(VerifyScreen(name='Verify'))
        return self.sm

    def on_start(self):
        token = load_refresh_token()

        if token:
            result = refresh_login(token)

            if result:
                self.sm.id_token = result["idToken"]
                self.sm.refresh_token = result["refreshToken"]

                # save new token
                save_refresh_token(result["refreshToken"])

                if result.get("emailVerified") is True:
                    self.sm.current = "App"

                else:
                    self.sm.current = "Verify"
                return
            else:
                clear_refresh_token()

        self.sm.current = "Signup"

if __name__ == "__main__":
    MainApp().run()