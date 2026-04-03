import requests

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Login_request(screen_instance, email_input, password_input):  
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
        screen_instance.login_r = r
        screen_instance.login_result = result
        screen_instance.email_verified = email_verified
        screen_instance.email_input = email_input
        screen_instance.password_input = password_input