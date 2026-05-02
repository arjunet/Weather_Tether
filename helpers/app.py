import requests
import re

from carbonkivy.app import App

from kivy.storage.jsonstore import JsonStore

from helpers.sidepanel import SidePanel

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"
WEATHER_API_URL = "https://weather-backend-318359636878.us-central1.run.app"

def get_dat(self):
        # Get user dat:
        id_token = self.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}

        if self.get_3 == True:
             response = requests.get(f"{FIREBASE_URL}/get_location3", headers=headers)

        elif self.get_2 == True:
             response = requests.get(f"{FIREBASE_URL}/get_location2", headers=headers)

        else:
            response = requests.get(f"{FIREBASE_URL}/get_location", headers=headers)

        if response.status_code == 200:
                user_data = response.json()
                
                # Grab the Firestore location data:
                lat = user_data.get("lat")
                lon = user_data.get("lon")
                self.current_lat = lat
                self.current_lon = lon
                self.city = user_data.get("location")

                self.get_weather(lat, lon)

                self.r = "weather_done"

def get_new_device_data(self):
        # Get user dat:
        id_token = self.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}

        response = requests.get(f"{FIREBASE_URL}/get_location3", headers=headers)
        if response.status_code == 200:
                user_data = response.json()
                self.city3 = user_data.get("location")
                save_city(self.city3, 3)

        else:
            self.get3 = "Fail"

        response = requests.get(f"{FIREBASE_URL}/get_location2", headers=headers)

        if response.status_code == 200:
                user_data = response.json()
                self.city2 = user_data.get("location")
                save_city(self.city2, 2)

        else:
            self.get2 = "Fail"

        response = requests.get(f"{FIREBASE_URL}/get_location", headers=headers)
        if response.status_code == 200:
                user_data = response.json()
                self.city = user_data.get("location")
                save_city(self.city, 1)

        self.r = "weather_done"

def get_user_weather(self, lat, lon):
        if lat is None or lon is None:
            return True # Keep waiting

        if self.toggle_state == False:
            url = f"{WEATHER_API_URL}/weather?lat={lat}&lon={lon}&unit=imperial"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the weather data:
                self.current_temp = (f"{data['current_temp']}°F")
                self.feels_like = (f"{data['feels_like']}°F")
                self.is_daytime = (f"{data['is_daytime']}")
                self.min_temp = (f"{data['min_temp']}°F")
                self.max_temp = (f"{data['max_temp']}°F")
                self.precip_percent = (f"{data['precip_percent']}%")
                self.precip_type = (f"{data['precip_type']}")
                self.snow_fall = (f"{data['snow_fall']} Inches")
                self.thunderstorm_prob = (f"{data['thunderstorm_prob']}%")
                self.weather_condition = (f"{data['weather_condition']}")
                self.wind_chill = (f"{data['wind_chill']}°F")

        elif self.toggle_state == True:
            url = f"{WEATHER_API_URL}/weather?lat={lat}&lon={lon}&unit=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the weather data:
                self.current_temp = (f"{data['current_temp']}°C")
                self.feels_like = (f"{data['feels_like']}°C")
                self.is_daytime = (f"{data['is_daytime']}")
                self.min_temp = (f"{data['min_temp']}°C")
                self.max_temp = (f"{data['max_temp']}°C")
                self.precip_percent = (f"{data['precip_percent']}%")
                self.precip_type = (f"{data['precip_type']}")
                self.snow_fall = (f"{data['snow_fall']} Centimeters")
                self.thunderstorm_prob = (f"{data['thunderstorm_prob']}%")
                self.weather_condition = (f"{data['weather_condition']}")
                self.wind_chill = (f"{data['wind_chill']}°C")  

def update_ui_labels(self):
        # Sets the labels with the fetched weather data:
        self.ids.city_label.text = f"{self.city}"
        self.ids.current_temp_label.text = self.current_temp
        self.ids.condition_label.text = self.weather_condition
    
        # Combined High/Low/feels like label:
        self.ids.min_max_label.text = f"{self.max_temp} / {self.min_temp}\nFeels like: {self.feels_like}"   
        self.ids.precip_label.text = f"Precip: {self.precip_percent} Chance Of {self.precip_type}"
        self.ids.snow_label.text = f"Snow: {self.snow_fall}"
        self.ids.thunder_label.text = f"Thunder: {self.thunderstorm_prob}"
        self.ids.wind_chill_label.text = f"Wind Chill: {self.wind_chill}"

def update_ui_background(self):
    # Update the background/icon based on weather condition:
    if "sun" in self.weather_condition.lower():
        self.bg_image = "images/sun_bg.jpg"
        self.icon_path = "images/sun_icon.png"

    elif self.is_daytime == "False":
        self.bg_image = "images/night.jpg"
        self.icon_path = "images/moon.png"

        self.app = App.get_running_app()
        self.app.theme = "Gray100"

        self.sidepanel = SidePanel()

    elif "clear" in self.weather_condition.lower() and self.is_daytime != "False":
        self.bg_image = "images/sun_bg.jpg"
        self.icon_path = "images/sun_icon.png"

        self.app = App.get_running_app()
        self.app.theme = "White"

    elif "cloud" in self.weather_condition.lower():
        self.bg_image = "images/cloud_bg.jpg"
        self.icon_path = "images/cloud_icon.png"

        self.app = App.get_running_app()
        self.app.theme = "White"

    elif "rain" in self.weather_condition.lower() or "drizzle" in self.weather_condition.lower() or "storm" in self.weather_condition.lower() or "thunder" in self.weather_condition.lower() or "shower" in self.weather_condition.lower():
        self.bg_image = "images/rain_bg.png"
        self.icon_path = "images/rain_icon.png"

        self.app = App.get_running_app()
        self.app.theme = "White"

    elif "snow" in self.weather_condition.lower() or "sleet" in self.weather_condition.lower() or "blizzard" in self.weather_condition.lower():
        self.bg_image = "images/snow_bg.jpg"
        self.icon_path = "images/snow_icon.png"

        self.app = App.get_running_app()
        self.app.theme = "White"

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

def delete_city_request(self):
        self.get_2 = False
        self.get_3 = False
        self.current_lat = 0.0
        self.current_lon = 0.0
        self.current_temp = None
        self.feels_like = None
        self.is_daytime = False
        self.min_temp = None
        self.max_temp = None
        self.precip_percent = None
        self.precip_type = None
        self.snow_fall = None
        self.thunderstorm_prob = None
        self.weather_condition = None
        self.wind_chill = None

        if self.delete_2 == True:
            print("deleting city2")
            url = f"{FIREBASE_URL}/delete_location2"
            id_token = self.manager.id_token
            headers = {"Authorization": f"Bearer {id_token}"}

            try:
                r = requests.post(url, headers=headers, timeout=10)
                self.delete_r = r
                self.delete_result = r.json()
            except Exception as e:
                self.delete_r = "error"

            # Shift city3 to city2 if it exists
            store = JsonStore("session.json")

            self.deleted_2 = True

            if self.deleted_2 == True and store.exists("city3"):
                # Shift city3 to city2:

                # Get city3 data
                self.get_3 = True
                get_dat(self)

                # Delete city3 from Firestore
                url = f"{FIREBASE_URL}/delete_location3"
                id_token = self.manager.id_token
                headers = {"Authorization": f"Bearer {id_token}"}

                try:
                    r = requests.post(url, headers=headers, timeout=10)
                    self.delete_r = r
                    self.delete_result = r.json()
                except Exception as e:
                    self.delete_r = "error"


                # Save city3 data to city2 in Firestore
                self.city_found = True
                payload = {
                    "location": str(self.city), 
                    "lat": float(self.current_lat), 
                    "lon": float(self.current_lon)
                }
                headers_add2 = {"Authorization": f"Bearer {id_token}"}
                
                r = requests.post(f"{FIREBASE_URL}/save_location2", json=payload, headers=headers_add2)
                print(r.json())

                store.delete("city3")

                save_city(self.city, 2)

        elif self.delete_3 == True:
            url = f"{FIREBASE_URL}/delete_location3"
            id_token = self.manager.id_token
            headers = {"Authorization": f"Bearer {id_token}"}
        
            try:
                r = requests.post(url, headers=headers, timeout=10)
                self.delete_r = r
                self.delete_result = r.json()
            except Exception as e:
                self.delete_r = "error"

        self.delete_done = "done"

def is_valid_email(email):
        # This pattern checks for: characters + @ + characters + . + characters
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email.strip()) is not None