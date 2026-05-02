import requests
import json
import time
import pandas as pd

API_KEY = "0c450b7b3e5443e78fa175145261304"

api_url = "https://api.weatherapi.com/v1/forecast.json" # API endpoint for forecast weather

zip_codes = [
    "90045",  # Los Angeles, CA
    "10001",  # New York, NY
    "60601",  # Chicago, IL
    "98101",  # Seattle, WA
    "33101",  # Miami, FL
    "77001",  # Houston, TX
    "85001",  # Phoenix, AZ
    "19101",  # Philadelphia, PA
    "78201",  # San Antonio, TX
    "75201",  # Dallas, TX
    "95101",  # San Jose, CA
    "78701",  # Austin, TX
    "32099",  # Jacksonville, FL
    "28201",  # Charlotte, NC
    "43201",  # Columbus, OH
    "46201",  # Indianapolis, IN
    "94101",  # San Francisco, CA
    "80201",  # Denver, CO
    "73101",  # Oklahoma City, OK
    "37201",  # Nashville, TN
]

results = []

for zip_code in zip_codes:
    params = {
        "key": API_KEY,
        "q": zip_code,
        "days": 7
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    city = data["location"]["name"]

    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        max_temp = day["day"]["maxtemp_f"]
        min_temp = day["day"]["mintemp_f"]
        condition = day["day"]["condition"]["text"]

        results.append({
            "zip_code": zip_code,
            "city": city,
            "date": date,
            "max_temp_f": max_temp,
            "min_temp_f": min_temp,
            "condition": condition,
        })

        print(f"{city} ({date}): High {max_temp}°F, Low {min_temp}°F, {condition}")

    time.sleep(1)

df = pd.DataFrame(results)
print(df.to_string(index=False))
print(f"\nRows: {df.shape[0]}, Columns: {df.shape[1]}")

df.to_csv("weather_data.csv", index=False)
print("Saved to weather_data.csv")
