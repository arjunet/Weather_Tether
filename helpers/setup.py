import json
import requests
from kivy.storage.jsonstore import JsonStore

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"

def Request_City(screen_instance):
        # Variable for Search Query of city:
        search_query = screen_instance.ids.address_input.text.strip() 
        # Reset the city_found variable to False for each new search:
        screen_instance.city_found = False

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
            screen_instance.ids.address_button.disabled = False
            screen_instance.ids.address_button.text = formatted_address

            # Most Google Place results have geometry -> location -> lat/lng
            screen_instance.current_lat = location_data.get("lat")
            screen_instance.current_lon = location_data.get("lng")
            screen_instance.city_found = True

        else:
            screen_instance.ids.address_button.disabled = True
            screen_instance.ids.address_button.text = "No results found."

def save_location_request(screen_instance):
        # Countinue the loading until city is found (extra if-statement, just in-case):
        if screen_instance.city_found == False:
            return True # Keep waiting
        
        # Sends the location to Firestore:
        location_input = screen_instance.ids.address_input.text
        if screen_instance.add_other == True:
            id_token = screen_instance.city.manager.id_token

        else:
             id_token = screen_instance.manager.id_token
        payload = {
            "location": str(location_input), 
            "lat": float(screen_instance.current_lat), 
            "lon": float(screen_instance.current_lon)
        }
        headers = {"Authorization": f"Bearer {id_token}"}
        
        if screen_instance.add_3 == True:
             r = requests.post(f"{FIREBASE_URL}/save_location3", json=payload, headers=headers)
             print(r.json())

        elif screen_instance.add_2 == True:
             r = requests.post(f"{FIREBASE_URL}/save_location2", json=payload, headers=headers)
             print(r.json())
        else: 
            r = requests.post(f"{FIREBASE_URL}/save_location", json=payload, headers=headers)
            print(r.json())

def save_json(screen_instance, json_string):
    if isinstance(json_string, JsonStore):
        json_string = json.dumps({key: json_string.get(key) for key in json_string.keys()})
    elif not isinstance(json_string, str):
        json_string = json.dumps(json_string)

    id_token = screen_instance.manager.id_token

    payload = {"json_string": json_string}
    headers = {"Authorization": f"Bearer {id_token}"}
    
    r = requests.post(f"{FIREBASE_URL}/update_json", json=payload, headers=headers)
    print(r.json())