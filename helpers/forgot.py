import requests

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Send_Forgot_Email(screen_instance, email_input):   
        # Server Request:
        url = f"{FIREBASE_URL}/reset_password"
        payload = {"email": email_input}
        r = requests.post(url, json=payload)
        result = r.json()

        # Declares results from sending for notifications:
        screen_instance.forgot_r = r
        screen_instance.forgot_result = result
        screen_instance.email_input = email_input