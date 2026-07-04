"""
Weather Dashboard
Creator : Aarav Bansal

This program gets live weather data from the Open-Metro API and displays a weather report
with recommendations.

"""


import requests
from datetime import datetime


# This list all the cities and its coordinates. 
cities = {
    "mckinney": (33.20, -96.64),
    "dallas": (32.78, -96.81),
    "austin": (30.27, -97.74),
    "houston": (29.76, -95.37),
    "new york": (40.71, -74.01)
}


# This function gets the city from the user, checks to see if it exists, and returns it.
def get_city():
    print("This weather dashboard includes the following cities : Mckinney, Dallas, Austin, Houston, and New York")
    city = input("Enter a city: ").lower()

    if city not in cities:
        print("Sorry, that city isn't available. ")
        exit()

    return city


# This function gets the weather data, uses a try and except for handling API request errors, and then returns the data. 
def fetch_weather(city):
    latitude, longitude = cities[city]

    url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}"
    f"&longitude={longitude}"
    f"&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m"
    f"&temperature_unit=fahrenheit"
    f"&wind_speed_unit=mph"
    f"&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch weather data:", e)
        exit()

    return data


# This function defines all weather information, and determines which advice to give to the user, and returns all information. 
def analyze_weather(data):
    current = data.get("current", {})

    temperature = current.get("temperature_2m")
    wind_speed = current.get("wind_speed_10m")

    api_time = current.get("time")

    if api_time is None:
        print("Missing time data. ")
        exit()

    dt = datetime.fromisoformat(api_time)
    formatted_time = dt.strftime("%Y-%m-%d %I:%M %p")

    feels_like = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")

    if temperature is None or wind_speed is None:
        print("Incomplete weather data received. ")
        exit()

    if temperature >= 90:
        advice = "Stay hydrated and try to limit time spent outside."
    elif temperature >= 75:
        advice = "Great weather to go outside."
    elif temperature >= 60:
        advice = "A light jacket would be more comfortable."
    else:
        advice = "Dress warmly."

    if wind_speed < 5:
        wind_description = "Calm"
    elif wind_speed < 15:
        wind_description = "Breezy"
    else:
        wind_description = "Windy"

    

    return {
    "temperature": temperature,
    "feels_like": feels_like,
    "humidity": humidity,
    "wind_speed": wind_speed,
    "wind_description": wind_description,
    "advice": advice,
    "time": formatted_time
    }


# This function prints out a weather report, containing all information, to the user. 
def print_report(city, weather):
    print()
    print("Weather Report for", city.title())
    print("Time:", weather["time"])
    print("Temperature:", weather["temperature"], "°F")
    print("Feels like:", weather["feels_like"], "°F")
    print("Humidity:", weather["humidity"], "%")
    print("Wind Speed:", weather["wind_speed"], "mph (", weather["wind_description"], ")")

    print()
    print("Advice:", weather["advice"])
    print()


# This function controls the overall program by calling all of the functions. 
def main():
    city = get_city()
    data = fetch_weather(city)
    weather = analyze_weather(data)
    print_report(city, weather)


# This condition makes sure that the main() function only runs when it is called directly. 
if __name__ == "__main__":
    main()
