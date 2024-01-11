import requests

class TellWeather():
    def __init__(self):
        api_key = "4ada04c83a698d58b93d04f507b3097f"
        location = requests.get("https://ipinfo.io/loc").text.strip().split(',')
        open_weather_url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lat={location[0]}&lon={location[1]}&appid={api_key}"
        self.weather_data = requests.get(open_weather_url).json()

    def run(self):
        message =  f"In {self.weather_data['name']}, "
        message += f"there is currently {self.weather_data['weather'][0]['description']}\n"
        message += f"with a temperature of {round(float(self.weather_data['main']['temp']))}°C, wind speed of {self.weather_data['wind']['speed']} m/s,\n"
        message += f"and a minimum and maximum temperature of {round(float(self.weather_data['main']['temp_min']))}°C and {round(float(self.weather_data['main']['temp_max']))}°C."
        return message

def setup():
    return TellWeather()