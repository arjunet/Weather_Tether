import requests
from helpers.token_management import save_refresh_token

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

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
        
        if r.status_code == 200:      
            login_after_signup(self, email_input, password_input)

def login_after_signup(self, email_input, password_input):
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