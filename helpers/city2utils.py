import requests
from helpers.signup import FIREBASE_URL

def delete_city_2_request(screen_instance, app_instance):
        screen_instance.get_2 = False
        screen_instance.get_3 = False
        screen_instance.current_lat = 0.0
        screen_instance.current_lon = 0.0
        screen_instance.current_temp = None
        screen_instance.feels_like = None
        screen_instance.is_daytime = False
        screen_instance.min_temp = None
        screen_instance.max_temp = None
        screen_instance.precip_percent = None
        screen_instance.precip_type = None
        screen_instance.snow_fall = None
        screen_instance.thunderstorm_prob = None
        screen_instance.weather_condition = None
        screen_instance.wind_chill = None

        url = f"{FIREBASE_URL}/delete_location2"
        id_token = screen_instance.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}
        
        try:
            r = requests.post(url, headers=headers, timeout=10)
            screen_instance.delete_r = r
            screen_instance.delete_result = r.json()
        except Exception as e:
            screen_instance.delete_r = "error"

def delete_city_3_request(screen_instance, app_instance):
        screen_instance.get_2 = False
        screen_instance.get_3 = False
        screen_instance.current_lat = 0.0
        screen_instance.current_lon = 0.0
        screen_instance.current_temp = None
        screen_instance.feels_like = None
        screen_instance.is_daytime = False
        screen_instance.min_temp = None
        screen_instance.max_temp = None
        screen_instance.precip_percent = None
        screen_instance.precip_type = None
        screen_instance.snow_fall = None
        screen_instance.thunderstorm_prob = None
        screen_instance.weather_condition = None
        screen_instance.wind_chill = None

        url = f"{FIREBASE_URL}/delete_location3"
        id_token = screen_instance.manager.id_token
        headers = {"Authorization": f"Bearer {id_token}"}
        
        try:
            r = requests.post(url, headers=headers, timeout=10)
            screen_instance.delete_r = r
            screen_instance.delete_result = r.json()
        except Exception as e:
            screen_instance.delete_r = "error"
            screen_instance.delete_result = {"detail": str(e)}