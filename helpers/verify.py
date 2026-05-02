import requests
import time
from helpers.token_management import load_refresh_token, save_refresh_token, refresh_login

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Send_Verification(self):
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

        time.sleep(2.0)

        result = refresh_login(token)

        if result and result.get("emailVerified") is True:
            self.email_verified = True
            self.manager.id_token = result["idToken"]
            self.manager.refresh_token = result["refreshToken"]
            self.done = True

        else:
            self.email_verified = False
            self.manager.id_token = result["idToken"]
            self.manager.refresh_token = result["refreshToken"]
            self.done = True