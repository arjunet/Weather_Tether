import requests

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def delete_request(self):
        url = f"{FIREBASE_URL}/delete_account"
        id_token = self.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}
        
        try:
            # We use POST because that's how we set up the FastAPI route
            r = requests.post(url, headers=headers, timeout=10)
            self.delete_r = r
            self.delete_result = r.json()
        except Exception as e:
            self.delete_r = "error"
            self.delete_result = {"detail": str(e)}