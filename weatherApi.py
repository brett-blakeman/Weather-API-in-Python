import requests
from datetime import datetime, timezone, timedelta

API_KEY = "190b76c0d0f7414a0d0d1c49fa941775"


def dpoint(temp, humidity):
    temp_c = (temp - 32) * 5 / 9
    dew_point = temp_c - ((100 - humidity) / 5)
    temp_f = (dew_point * 9 / 5) + 32
    return temp_f


def coverage(cloudiness):
    if cloudiness < 10:
        return "Sunny"
    elif cloudiness < 50:
        return "Partly Cloudy"
    elif cloudiness < 80:
        return "Mostly Cloudy"
    else:
        return "Overcast"


def precip(is_raining, is_snowing):
    if is_raining > 0:
        return "It is currently raining."
    elif is_snowing > 0:
        return "It is currently snowing."
    else:
        return "There is no precipitation."


def get_weather_data(city):
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&appid={API_KEY}&units=imperial"
    )

    response = requests.get(url)
    return response.json()


def update_weather(city):
    data = get_weather_data(city)

    if "main" not in data:
        return "Error: Could not retrieve weather data."

    utc_time = datetime.now(timezone.utc)

    offset = data["timezone"]
    city_time = utc_time + timedelta(seconds=offset)
    local_time = city_time.strftime("%I:%M %p")

    #-----------------------------------
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    high = data["main"]["temp_max"]
    low = data["main"]["temp_min"]
    #-----------------------------------
    humidity = data["main"]["humidity"]
    dew_point = dpoint(temp, humidity)
    #-----------------------------------
    cloudiness = data["clouds"]["all"]
    cov = coverage(cloudiness)
    is_raining = data.get("rain", {}).get("1h", 0)
    is_snowing = data.get("snow", {}).get("1h", 0)
    precip_type = precip(is_raining, is_snowing)
    #-----------------------------------
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]

    output = f"""
-------------------------------------------------
Weather in {city} as of {local_time} local time:

-------------------Temperature-------------------
Current Temp:__________{temp:.1f}°F
Feels Like:____________{feels_like:.1f}°F
Today's High:__________{high:.1f}°F
Today's Low:___________{low:.1f}°F

--------------------Humidity---------------------
Current Humidity:______{humidity}%
Current Dew Point:_____{dew_point:.1f}°F

-------------Coverage/Precipitation--------------
Current Cloudiness:____{cov}, {cloudiness}% Coverage
Precipitation:_________{precip_type}

----------------Air Pressure/Wind----------------
Current Air pressure:__{pressure} hPa
Current Wind Speed:____{wind_speed:.1f} mph

-------------------------------------------------
"""
    return output

# RIP the old print statements when the program was a script o7
'''
print("-------------------------------------------------")
print(f"Weather in {CITY} as of {formatted_city_time} local time:")
print(" ")
print("-------------------Temperature-------------------")
print(f"Current Temp:__________{temp:.1f}°F")
print(f"Feels Like:____________{feels_like:.1f}°F")
print(f"Today's High:__________{high:.1f}°F")
print(f"Today's Low:___________{low:.1f}°F")
print(" ")
print("--------------------Humidity---------------------")
print(f"Current Humidity:______{humidity}%")
print(f"Current Dew Point:_____{dew_point:.1f}°F")
print(" ")
print("-------------Coverage/Precipitation--------------")
print(f"Current Cloudiness:____{cov}, {cloudiness}% Coverage")
print(f"Precipitation:_________{precip_type}")
print(" ")
print(f"Current Air pressure:__{pressure} hPa")  
print(f"Current Wind Speed:____{wind_speed:.1f} mph")
print("-------------------------------------------------")
'''