import requests
import time
from token_management import load_refresh_token, save_refresh_token, refresh_login

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Send_Verification(screen_instance):
        url = f"{FIREBASE_URL}/resend_verification"
        id_token = screen_instance.manager.id_token

        payload = {"id_token": id_token}
    
        r = requests.post(url, json=payload, timeout=10)
        print(r.json())
        result = r.json()
        screen_instance.r = r
        screen_instance.result = result
        
        # Check the response
        if r.status_code == 200:
            print("Email resent successfully!")
            print(r.json())

def check_verification(screen_instance, *args):
    token = load_refresh_token()

    if token:
        result = refresh_login(token)

        if result:
            screen_instance.manager.id_token = result["idToken"]
            screen_instance.manager.refresh_token = result["refreshToken"]

            # save new token
            save_refresh_token(result["refreshToken"])

            if result.get("emailVerified") is True:
                screen_instance.email_verified = True

            else:
                screen_instance.email_verified = False

        time.sleep(2.0)

        result = refresh_login(token)

        if result and result.get("emailVerified") is True:
            screen_instance.email_verified = True
            screen_instance.manager.id_token = result["idToken"]
            screen_instance.manager.refresh_token = result["refreshToken"]
            screen_instance.done = True

        else:
            screen_instance.email_verified = False
            screen_instance.manager.id_token = result["idToken"]
            screen_instance.manager.refresh_token = result["refreshToken"]
            screen_instance.done = True