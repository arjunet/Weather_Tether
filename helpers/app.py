import requests
import re
import json

from carbonkivy.app import App

from kivy.storage.jsonstore import JsonStore

from helpers.menu_buttons import Delete_Day, Delete_Night, Edit_Day, Edit_Night
from helpers.sidepanel import SidePanel

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"
WEATHER_API_URL = "https://weather-backend-318359636878.us-central1.run.app"

def get_dat(self, city_number):
        # Get user dat:
        id_token = self.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}

        payload = {
            "city_number": str(city_number)
        }

        response = requests.post(f"{FIREBASE_URL}/get_location", json=payload, headers=headers)

        if response.status_code == 200:
                user_data = response.json()
                
                # Grab the Firestore location data:
                self.current_lat = user_data.get("lat")
                self.current_lon = user_data.get("lon")
                self.city = user_data.get("location")

                self.get_weather(self.current_lat, self.current_lon)

        else:
             self.get_r = "Fail"

        self.r = "weather_done"

def get_new_device_data(self):
    id_token = self.manager.id_token
    headers = {"Authorization": f"Bearer {id_token}"}
    store = JsonStore("session.json")

    try:
        # 1. Fetch all city data from our new bulk endpoint in 1 request
        response = requests.get(f"{FIREBASE_URL}/get_all_locations", headers=headers, timeout=10)
        
        if response.status_code == 200:
            server_data = response.json()
            remote_locations = server_data.get("locations", {})

            # 2. Update our local JsonStore for all 30 slots
            for i in range(1, 31):
                key = str(i)
                
                if key in remote_locations:
                    # City exists on server: save/update it locally
                    city_data = remote_locations[key]
                    
                    # Assuming your save_city function writes to JsonStore,
                    # pass it whatever payload structure save_city expects.
                    # If save_city just takes name and city_number, do:
                    save_city(city_data["name"], i)
                else:
                    # City doesn't exist on server: clean it up locally
                    if store.exists(key):
                        store.delete(key)
        else:
            print(f"Failed to sync device data. Status: {response.status_code}")
            
    except Exception as e:
        print(f"Error while syncing new device data: {e}")

def get_user_weather(self, lat, lon):
        if lat is None or lon is None:
            return True # Keep waiting

        if self.toggle_state == False:
            url = f"{WEATHER_API_URL}/weather?lat={lat}&lon={lon}&unit=imperial"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the weather data:
                self.current_temp = (f"{data['current_temp']}")
                self.feels_like = (f"{data['feels_like']}")
                self.is_daytime = (f"{data['is_daytime']}")
                self.min_temp = (f"{data['min_temp']}")
                self.max_temp = (f"{data['max_temp']}")
                self.precip_percent = (f"{data['precip_percent']}")
                self.precip_type = (f"{data['precip_type']}")
                self.snow_fall = (f"{data['snow_fall']}")
                self.weather_condition = (f"{data['weather_condition']}")
                self.wind_chill = (f"{data['wind_chill']}")

        elif self.toggle_state == True:
            url = f"{WEATHER_API_URL}/weather?lat={lat}&lon={lon}&unit=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the weather data:
                self.current_temp = (f"{data['current_temp']}")
                self.feels_like = (f"{data['feels_like']}")
                self.is_daytime = (f"{data['is_daytime']}")
                self.min_temp = (f"{data['min_temp']}")
                self.max_temp = (f"{data['max_temp']}")
                self.precip_percent = (f"{data['precip_percent']}")
                self.precip_type = (f"{data['precip_type']}")
                self.snow_fall = (f"{data['snow_fall']}")
                self.weather_condition = (f"{data['weather_condition']}")
                self.wind_chill = (f"{data['wind_chill']}")  

def update_ui_labels(self):
        # Sets the labels with the fetched weather data:
        # Precip_type check:
        if self.precip_type == "None":
            self.precip_type = "Rain"

        self.ids.city_label.text = f"{self.city}"
        self.ids.current_temp_label.text = self.current_temp
        self.ids.condition_label.text = self.weather_condition
    
        # Combined High/Low/feels like label:
        self.ids.min_max_label.text = f"{self.max_temp} / {self.min_temp}"   
        self.ids.feels_like_label.text = f"Feels Like: {self.feels_like}"
        self.ids.precip_label.text = f"{self.precip_percent} Chance Of {self.precip_type}"
        self.ids.snow_label.text = f"{self.snow_fall} Of Snow"
        self.ids.wind_chill_label.text = f"Wind Chill: {self.wind_chill}"

def update_ui_background(self):
    self.app = App.get_running_app()
    condition = (self.weather_condition or "").lower()
    
    # Update the background/icon based on weather condition:
    if "sun" in condition:
        self.bg_image = "images/sun_bg.jpg"
        self.icon_path = "images/sun_icon.png"
        self.app.theme = "White"
        self.transparency_color = [1, 1, 1, 0.7]

    elif self.is_daytime == "False":
        self.bg_image = "images/night.jpg"
        self.icon_path = "images/moon.png"
        self.transparency_color = [1, 1, 1, 0.35]

        self.app.theme = "Gray100"

        self.sidepanel = SidePanel()

    elif "clear" in condition and self.is_daytime != "False":
        self.bg_image = "images/sun_bg.jpg"
        self.icon_path = "images/sun_icon.png"
        self.transparency_color = [1, 1, 1, 0.7]

        self.app = App.get_running_app()
        self.app.theme = "White"

    elif "cloud" in condition or "fog" in condition:
        self.bg_image = "images/cloud_bg.jpg"
        self.icon_path = "images/cloud_icon.png"
        self.transparency_color = [1, 1, 1, 0.7]

        self.app = App.get_running_app()
        self.app.theme = "White"

    elif "rain" in condition or "drizzle" in condition or "storm" in condition or "thunder" in condition or "shower" in condition:
        self.bg_image = "images/rain_bg.jpg"
        self.icon_path = "images/rain_icon.png"
        self.transparency_color = [1, 1, 1, 0.7]

        self.app = App.get_running_app()
        self.app.theme = "White"

    elif "snow" in condition or "sleet" in condition or "blizzard" in condition:
        self.bg_image = "images/snow_bg.jpg"
        self.icon_path = "images/snow_icon.png"
        self.transparency_color = [1, 1, 1, 0.7]

        self.app = App.get_running_app()
        self.app.theme = "White"

    self.app.apply_styles(self)

    if hasattr(self, "ids") and hasattr(self.ids, "weather_icon"):
        self.ids.weather_icon.source = self.icon_path or ""
        self.ids.weather_icon.opacity = 1
        self.ids.weather_icon.reload()

def save_city(city_name, city_number):
    key = str(city_number)
    store = JsonStore('session.json')
    
    store.put(key, name=city_name)

def delete_city_request(self):
    payload = {
        "city_number": self.city_number
    }
    
    url = f"{FIREBASE_URL}/delete_location"
    id_token = self.manager.id_token
    headers = {"Authorization": f"Bearer {id_token}"}

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        self.delete_r = r
        self.delete_result = r.json()

        # --- LOCAL JSONSTORE SHIFTING ---
        if r.status_code in (200, 201):
            file = JsonStore("session.json")
            
            # 1. Extract all existing city entries into a temporary dict
            temp_cities = {}
            max_cities = 30
            
            for i in range(1, max_cities + 1):
                key = str(i)
                if file.exists(key):
                    temp_cities[i] = file.get(key)
            
            # 2. Re-index and shift items down locally
            shifted_cities = {}
            deleted_idx = int(self.city_number)
            
            for i in range(1, max_cities + 1):
                if i < deleted_idx:
                    # Keep cities before the deleted index exactly where they are
                    if i in temp_cities:
                        shifted_cities[i] = temp_cities[i]
                elif i > deleted_idx:
                    # Shift everything after the deleted index down by 1
                    if i in temp_cities:
                        shifted_cities[i - 1] = temp_cities[i]
            
            # 3. Clear out all old city keys from JsonStore so there's no leftover duplicates
            for i in range(1, max_cities + 1):
                key = str(i)
                if file.exists(key):
                    file.delete(key)
                    
            # 4. Write the newly shifted layout structure back to the file
            for new_idx, city_data in shifted_cities.items():
                file.put(str(new_idx), **city_data)
                
    except Exception as e:
        print(f"Error deleting city: {e}")
        self.delete_r = "error"

    self.delete_done = "done"

def is_valid_email(email):
    pattern = r'^[\w.+\-]+@[\w.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None

def add_option_buttons(self):
    self.edit_day = Edit_Day()
    self.edit_night = Edit_Night()
    self.delete_day = Delete_Day()
    self.delete_night = Delete_Night()

    self.ids.container.clear_widgets()

    if self.ids.shell_menu_btn.active:
        if self.is_daytime != "False":
            self.ids.container.add_widget(self.edit_day)
            if self.city1 != True: 
                self.ids.container.add_widget(self.delete_day)
        else:
            self.ids.container.add_widget(self.edit_night)
            if self.city1 != True: 
                self.ids.container.add_widget(self.delete_night)
    else:
        self.ids.container.clear_widgets()

    if self.is_daytime != "False":
        self.ids.shell_menu_btn.bg_color = (0, 0, 0, 1)
        self.ids.shell_menu_btn.text_color = (1, 1, 1, 1)
    else:
         self.ids.shell_menu_btn.bg_color = (1, 1, 1, 1)
         self.ids.shell_menu_btn.text_color = (0, 0, 0, 1)