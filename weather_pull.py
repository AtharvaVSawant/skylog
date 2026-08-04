"""
weather_pull.py
Pulls current weather for a list of cities from OpenWeatherMap
and logs each reading as a new row in a SQLite database.

Run once manually to test, or schedule it (cron / Task Scheduler)
to build up a historical log over time.
"""

import os
import sqlite3
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

# ---------- Config ----------

load_dotenv()  # reads .env into environment variables

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DB_PATH = "weather_data.db"

CITIES = [
    "Mumbai,IN",
    "Delhi,IN",
    "Bangalore,IN",
    "Chennai,IN",
    "Kolkata,IN",
    "Pune,IN",
    "New York,US",
    "London,GB",
    "Tokyo,JP",
    "Sydney,AU",
]

# ---------- Database ----------

def init_db(conn: sqlite3.Connection) -> None:
    """Create the weather_log table if it doesn't already exist."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT,
            latitude REAL,
            longitude REAL,
            temperature REAL,
            feels_like REAL,
            humidity INTEGER,
            wind_speed REAL,
            weather_condition TEXT,
            weather_description TEXT,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()


def insert_reading(conn: sqlite3.Connection, row: dict) -> None:
    conn.execute(
        """
        INSERT INTO weather_log (
            city, country, latitude, longitude,
            temperature, feels_like, humidity, wind_speed,
            weather_condition, weather_description, timestamp
        ) VALUES (:city, :country, :latitude, :longitude,
                   :temperature, :feels_like, :humidity, :wind_speed,
                   :weather_condition, :weather_description, :timestamp)
        """,
        row,
    )
    conn.commit()


# ---------- API ----------

def fetch_weather(city: str) -> dict | None:
    """Call the OpenWeatherMap current-weather endpoint for one city."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # Celsius, m/s wind
    }
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"  [HTTP ERROR] {city}: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  [NETWORK ERROR] {city}: {e}")
        return None

    return {
        "city": data["name"],
        "country": data["sys"].get("country"),
        "latitude": data["coord"]["lat"],
        "longitude": data["coord"]["lon"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "weather_condition": data["weather"][0]["main"],
        "weather_description": data["weather"][0]["description"],
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


# ---------- Main ----------

def run_once() -> None:
    if not API_KEY:
        raise SystemExit(
            "No API key found. Copy .env.example to .env and add your "
            "OpenWeatherMap key."
        )

    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    print(f"Pulling weather for {len(CITIES)} cities...")
    success, failed = 0, 0

    for city in CITIES:
        reading = fetch_weather(city)
        if reading:
            insert_reading(conn, reading)
            print(f"  [OK] {reading['city']}: {reading['temperature']}°C, "
                  f"{reading['weather_condition']}")
            success += 1
        else:
            failed += 1

    conn.close()
    print(f"Done. {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    run_once()
