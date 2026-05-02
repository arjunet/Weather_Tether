import json
import requests
from kivy.storage.jsonstore import JsonStore

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Request_City(self):
        # Variable for Search Query of city:
        search_query = self.ids.address_input.text.strip() 
        # Reset the city_found variable to False for each new search:
        self.city_found = False

        # Request for JSON and raise exceptions on errors:

        # Api url (google cloud run):
        url = f"https://maps-backend-318359636878.us-central1.run.app/places?query={search_query}"

        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        if data.get("results"):
            # Get coordinate/city data:
            result = data["results"][0]
            location_data = result.get("geometry", {}).get("location", {})

            formatted_address = data["results"][0].get("formatted_address")
            self.ids.address_button.disabled = False
            self.ids.address_button.text = formatted_address

            self.current_lat = location_data.get("lat")
            self.current_lon = location_data.get("lng")
            self.city_found = True

        else:
            self.ids.address_button.disabled = True
            self.ids.address_button.text = "No results found."

def save_location_request(self): 
        # Sends the location to Firestore:
        location_input = self.ids.address_input.text
        if self.add_other == True:
            id_token = self.city.manager.id_token

        else:
             id_token = self.manager.id_token
        payload = {
            "location": str(location_input), 
            "lat": float(self.current_lat), 
            "lon": float(self.current_lon)
        }
        headers = {"Authorization": f"Bearer {id_token}"}
        
        if self.add_3 == True:
             r = requests.post(f"{FIREBASE_URL}/save_location3", json=payload, headers=headers)
             print(r.json())

        elif self.add_2 == True:
             r = requests.post(f"{FIREBASE_URL}/save_location2", json=payload, headers=headers)
             print(r.json())
        else: 
             r = requests.post(f"{FIREBASE_URL}/save_location", json=payload, headers=headers)
             print(r.json())

        self.firestore_done = True

def update_location_request(self, update_type):
    if self.add_other == True:
        id_token = self.city.manager.id_token
    else:
        id_token = self.manager.id_token

    payload = {
        "location": str(self.ids.address_input.text.strip()),
        "lat": float(self.current_lat),
        "lon": float(self.current_lon)
    }
    headers = {"Authorization": f"Bearer {id_token}"}

    if update_type == 1:
        r = requests.patch(f"{FIREBASE_URL}/update_location", json=payload, headers=headers)
    elif update_type == 2:
        r = requests.patch(f"{FIREBASE_URL}/update_location2", json=payload, headers=headers)
    elif update_type == 3:
        r = requests.patch(f"{FIREBASE_URL}/update_location3", json=payload, headers=headers)
    else:
        # Default to updating city1 if invalid type
        r = requests.patch(f"{FIREBASE_URL}/update_location", json=payload, headers=headers)

    self.firestore_done = True

def save_json(self, json_string):
    if isinstance(json_string, JsonStore):
        json_string = json.dumps({key: json_string.get(key) for key in json_string.keys()})
    elif not isinstance(json_string, str):
        json_string = json.dumps(json_string)

    id_token = self.manager.id_token

    payload = {"json_string": json_string}
    headers = {"Authorization": f"Bearer {id_token}"}
    
    r = requests.post(f"{FIREBASE_URL}/update_json", json=payload, headers=headers)
    print(r.json())