import requests
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('cred.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mini-c75f8-default-rtdb.firebaseio.com/'
})

ref = db.reference('/weather')

api_key = 'a50e68b94a85cc2c4125ef549fce41be'
latitude = input("Enter latitude: ")  # User input for latitude
longitude = input("Enter longitude: ")  # User input for longitude

# Construct the URL for fetching weather data based on latitude and longitude
url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&APPID={api_key}"

# Function to convert latitude and longitude to human-readable location 11.101628 76.965769
import requests

def get_location(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data['address']
        # Extract the relevant address components
        area = address.get('road', '')  # Area or street name
        city = address.get('city', '')  # City or village
        district = address.get('county', '')  # District
        # Construct the location string
        location = f"{area}, {city}, {district}"
        # Remove any trailing commas and spaces
        location = location.rstrip(', ')
        return location
    else:
        return "Location not found"

while True:
    weather_data = requests.get(url)
    if weather_data.status_code == 200:
        weather_json = weather_data.json()
        weather = weather_json['weather'][0]['main']
        temp_fahrenheit = weather_json['main']['temp']
        temp_celsius = round((temp_fahrenheit - 32) * 5 / 9)  
        humidity = weather_json['main']['humidity']
        location = get_location(latitude, longitude)
        print(f"The weather at {location} is: {weather};")
        print(f"The temperature at {location} is: {temp_celsius}°C;")
        print(f"The humidity at {location} is: {humidity}%")
        try:
            ref.set({
                'location': location,
                'weather': weather,
                'temperature':  temp_celsius,
                'humidity': humidity
            })
            print("Data written to Firebase successfully!")
        except Exception as e:
            print("Error writing data to Firebase:", str(e))
    else:
        print("Failed to fetch weather data. Status Code:", weather_data.status_code)

    time.sleep(1)  # Sleep for 1800 seconds (30 minutes)
