from kivy.storage.jsonstore import JsonStore
import requests
# ---------------------------------------------------------------------------------
def save_refresh_token(refresh_token):
                store = JsonStore('session.json')
                store.put('auth', refresh_token=refresh_token)

# ---------------------------------------------------------------------------------
def load_refresh_token():
    store = JsonStore('session.json')

    if store.exists('auth'):
        return store.get('auth').get('refresh_token')

    return None
# ---------------------------------------------------------------------------------
def clear_refresh_token():
    store = JsonStore('session.json')

    if store.exists('auth'):
        store.delete('auth')
# ---------------------------------------------------------------------------------
def refresh_login(refresh_token):
    try:
        FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"
        r = requests.post(
            f"{FIREBASE_URL}/refresh_session",
            json={"refresh_token": refresh_token},
            timeout=10
        )

        if r.status_code != 200:
            return None

        return r.json()

    except requests.RequestException:
        return None
# ---------------------------------------------------------------------------------
def login_request_token(self):
        # If its coming from verify screen, skip going back to verify screen & prevent duplicate login:
        if getattr(self.manager, 'coming_from_verify', False):
            self.go_to_verify = False
            # Reset the flag so it doesn't stay True forever
            self.manager.coming_from_verify = False 
            self.r = "done"
            return # Exit early, we're good!
        
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