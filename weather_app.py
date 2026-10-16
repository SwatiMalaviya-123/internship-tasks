import os
import tkinter as tk
from tkinter import messagebox

import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    if not API_KEY:
        raise ValueError("Set OPENWEATHER_API_KEY in your local .env file.")

    response = requests.get(
        WEATHER_URL,
        params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def show_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Missing city", "Enter a city name.")
        return

    try:
        data = get_weather(city)
        details = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        result_label.config(
            text=(
                f"{data['name']}\n"
                f"{details}\n"
                f"Temperature: {temperature} °C\n"
                f"Feels like: {feels_like} °C\n"
                f"Humidity: {humidity}%\n"
                f"Wind speed: {wind_speed} m/s"
            )
        )

    except ValueError as error:
        messagebox.showerror("API key needed", str(error))
    except requests.HTTPError as error:
        if error.response is not None and error.response.status_code == 404:
            messagebox.showerror("City not found", "Check the city name and try again.")
        else:
            messagebox.showerror("Weather service error", "Check your API key and try again.")
    except requests.RequestException:
        messagebox.showerror("Connection error", "Could not reach the weather service.")
    except (KeyError, IndexError):
        messagebox.showerror("Unexpected response", "The weather service returned unexpected data.")


window = tk.Tk()
window.title("Weather Application")
window.geometry("380x360")
window.resizable(False, False)

tk.Label(window, text="Weather Application", font=("Arial", 18, "bold")).pack(pady=18)
tk.Label(window, text="Enter a city:").pack()

city_entry = tk.Entry(window, font=("Arial", 13), justify="center")
city_entry.pack(pady=8)
city_entry.bind("<Return>", lambda event: show_weather())

tk.Button(window, text="Get Weather", command=show_weather).pack(pady=8)

result_label = tk.Label(window, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=14)

window.mainloop()