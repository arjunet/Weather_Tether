# Imports:

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

def save_toggle_state(toggle_state):
    store = JsonStore('session.json')
    store.put('toggle', active=toggle_state)
def save_city(city_name, city_number):
    # Normalize the city key
    if city_number is None:
        key = 'city1'
    else:
        if isinstance(city_number, int):
            key = f"city{city_number}"
        else:
            s = str(city_number)
            key = s if s.startswith('city') else f"city{s}"

    store = JsonStore('session.json')
    store.put(key, name=city_name)


