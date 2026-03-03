import requests
from token_management import save_refresh_token

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Signup_request(screen_instance, email_input, password_input):
        # Server Request:
        url = f"{FIREBASE_URL}/signup"
        payload = {
            "email": email_input,
            "password": password_input
       }
        r = requests.post(url, json=payload)
        result = r.json() 

        # Declares results from signup for notifications:
        screen_instance.signup_r = r
        screen_instance.signup_result = result
        screen_instance.email_input = email_input
        screen_instance.password_input = password_input
        
        if r.status_code == 200:      
            login_after_signup(screen_instance, email_input, password_input)

def login_after_signup(screen_instance, email_input, password_input):
        # Login after signup for token retrieval:
            login_payload = {
                "email": email_input,
                "password": password_input
            }
            login_r = requests.post(f"{FIREBASE_URL}/login", json=login_payload)
            login_res = login_r.json()

            screen_instance.manager.id_token = login_res["data"]["idToken"]
            screen_instance.manager.local_id = login_res["data"]["localId"]
            screen_instance.manager.refresh_token = login_res["data"]["refreshToken"]

            # Saves refresh token to file for autologin on app start:
            save_refresh_token(screen_instance.manager.refresh_token)