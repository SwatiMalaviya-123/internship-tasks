import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city."
        elif not API_KEY:
            error = "Weather API key is missing. Add it to weather_web/.env."
        else:
            try:
                response = requests.get(
                    WEATHER_URL,
                    params={"q": city, "appid": API_KEY, "units": "metric"},
                    timeout=10,
                )

                if response.status_code == 404:
                    error = "City not found. Check the spelling and try again."
                else:
                    response.raise_for_status()
                    data = response.json()
                    weather = {
                        "city": data["name"],
                        "country": data.get("sys", {}).get("country", ""),
                        "description": data["weather"][0]["description"].title(),
                        "temperature": round(data["main"]["temp"]),
                        "feels_like": round(data["main"]["feels_like"]),
                        "humidity": data["main"]["humidity"],
                        "wind": data.get("wind", {}).get("speed", "—"),
                        "pressure": data["main"]["pressure"],
                    }

            except requests.RequestException:
                error = "Could not contact the weather service. Please try again."
            except (KeyError, IndexError):
                error = "The weather service returned an unexpected response."

    return render_template("index.html", weather=weather, error=error, city=city)


if __name__ == "__main__":
    app.run(debug=False)