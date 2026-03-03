import requests
from kivy.app import App
from carbonkivy.app import App
import json
from kivy.properties import StringProperty

FIREBASE_URL = "https://firebase-auth-service-318359636878.us-central1.run.app"
WEATHER_API_URL = "https://weather-backend-318359636878.us-central1.run.app"

def get_dat(screen_instance):
        # Get user dat:
        id_token = screen_instance.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}

        if screen_instance.get_3 == True:
             response = requests.get(f"{FIREBASE_URL}/get_location3", headers=headers)

        elif screen_instance.get_2 == True:
             response = requests.get(f"{FIREBASE_URL}/get_location2", headers=headers)

        else:
            response = requests.get(f"{FIREBASE_URL}/get_location", headers=headers)

        if response.status_code == 200:
                user_data = response.json()
                
                # Grab the Firestore location data:
                lat = user_data.get("lat")
                lon = user_data.get("lon")
                screen_instance.city = user_data.get("location")

                screen_instance.get_weather(lat, lon)

                screen_instance.r = "weather_done"

def get_user_weather(screen_instance, lat, lon):
        if lat is None or lon is None:
            return True # Keep waiting

        if screen_instance.toggle_state == False:
            url = f"{WEATHER_API_URL}/weather?lat={lat}&lon={lon}&unit=imperial"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the weather data:
                screen_instance.current_temp = (f"{data['current_temp']}°F")
                screen_instance.feels_like = (f"{data['feels_like']}°F")
                screen_instance.is_daytime = (f"{data['is_daytime']}")
                screen_instance.min_temp = (f"{data['min_temp']}°F")
                screen_instance.max_temp = (f"{data['max_temp']}°F")
                screen_instance.precip_percent = (f"{data['precip_percent']}%")
                screen_instance.precip_type = (f"{data['precip_type']}")
                screen_instance.snow_fall = (f"{data['snow_fall']} Inches")
                screen_instance.thunderstorm_prob = (f"{data['thunderstorm_prob']}%")
                screen_instance.weather_condition = (f"{data['weather_condition']}")
                screen_instance.wind_chill = (f"{data['wind_chill']}°F")

        elif screen_instance.toggle_state == True:
            url = f"{WEATHER_API_URL}/weather?lat={lat}&lon={lon}&unit=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # Get the weather data:
                screen_instance.current_temp = (f"{data['current_temp']}°C")
                screen_instance.feels_like = (f"{data['feels_like']}°C")
                screen_instance.is_daytime = (f"{data['is_daytime']}")
                screen_instance.min_temp = (f"{data['min_temp']}°C")
                screen_instance.max_temp = (f"{data['max_temp']}°C")
                screen_instance.precip_percent = (f"{data['precip_percent']}%")
                screen_instance.precip_type = (f"{data['precip_type']}")
                screen_instance.snow_fall = (f"{data['snow_fall']} Centimeters")
                screen_instance.thunderstorm_prob = (f"{data['thunderstorm_prob']}%")
                screen_instance.weather_condition = (f"{data['weather_condition']}")
                screen_instance.wind_chill = (f"{data['wind_chill']}°C")  

def update_ui_labels(screen_instance):
        # Sets the labels with the fetched weather data:
        screen_instance.ids.city_label.text = f"{screen_instance.city}"
        screen_instance.ids.current_temp_label.text = screen_instance.current_temp
        screen_instance.ids.condition_label.text = screen_instance.weather_condition
    
        # Combined High/Low/feels like label:
        screen_instance.ids.min_max_label.text = f"{screen_instance.max_temp} / {screen_instance.min_temp}\nFeels like: {screen_instance.feels_like}"   
        screen_instance.ids.precip_label.text = f"Precip: {screen_instance.precip_percent} ({screen_instance.precip_type})"
        screen_instance.ids.snow_label.text = f"Snow: {screen_instance.snow_fall}"
        screen_instance.ids.thunder_label.text = f"Thunder: {screen_instance.thunderstorm_prob}"
        screen_instance.ids.wind_chill_label.text = f"Wind Chill: {screen_instance.wind_chill}"

def update_ui_background(screen_instance):
    # Update the background/icon based on weather condition:
    if "sun" in screen_instance.weather_condition.lower():
        screen_instance.bg_image = "images/sun_bg.jpg"
        screen_instance.icon_path = "images/sun_icon.png"

    elif screen_instance.is_daytime == "False":
        screen_instance.bg_image = "images/night.jpg"
        screen_instance.icon_path = "images/moon.png"

        screen_instance.app = App.get_running_app()
        screen_instance.app.theme = "Gray100" 
        screen_instance.ids.shell_header.bg_color = screen_instance.app.transparent

    elif "clear" in screen_instance.weather_condition.lower() and screen_instance.is_daytime != "False":
        screen_instance.bg_image = "images/sun_bg.jpg"
        screen_instance.icon_path = "images/sun_icon.png"

    elif "cloud" in screen_instance.weather_condition.lower():
        screen_instance.bg_image = "images/cloud_bg.jpg"
        screen_instance.icon_path = "images/cloud_icon.png"

    elif "rain" in screen_instance.weather_condition.lower() or "drizzle" in screen_instance.weather_condition.lower() or "storm" in screen_instance.weather_condition.lower() or "thunder" in screen_instance.weather_condition.lower() or "shower" in screen_instance.weather_condition.lower():
        screen_instance.bg_image = "images/rain_bg.png"
        screen_instance.icon_path = "images/rain_icon.png"

    elif "snow" in screen_instance.weather_condition.lower() or "sleet" in screen_instance.weather_condition.lower() or "blizzard" in screen_instance.weather_condition.lower():
        screen_instance.bg_image = "images/snow_bg.jpg"
        screen_instance.icon_path = "images/snow_icon.png"

def get_city_name(screen_instance):
      with open('session.json', 'r') as f:
            data = json.load(f)

            screen_instance.city1_panel_item = data.get("city1", {}).get("name", "City 1")
        
            try:
                screen_instance.city2_panel_item = data.get("city2", {}).get("name", "City 2")
                screen_instance.city3_panel_item = data.get("city3", {}).get("name", "City 3")

            except (FileNotFoundError, json.JSONDecodeError):
                 screen_instance.city2_panel_item = "City2"
                 screen_instance.city3_panel_item = "City3"
