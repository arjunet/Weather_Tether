import requests

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

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
        self.manager.id_token = result.get("data", {}).get("idToken")
        self.email_input = email_input
        self.password_input = password_input