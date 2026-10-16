# Python Internship Projects

A collection of Python projects completed during my Coding Samurai internship.

## Projects

### Web Scraper
Uses `requests` and Beautiful Soup to collect book titles, authors, and ratings from a Goodreads list page and save them to a CSV file.

Run:
`python web_scraper.py`

### Calculator
A desktop calculator built with Tkinter for basic arithmetic and percentage calculations.

Run:
`python calculator.py`

### Number Guessing Game
A Tkinter game where the player guesses a random number from 1 to 100.

Run:
`python number_guessing_game.py`

### To-Do List
A Tkinter app for adding, updating, and deleting tasks. Tasks are saved locally in `todo_tasks.txt`.

Run:
`python todo_list.py`

### Weather Application — Desktop
A Tkinter weather app that gets current conditions for a city from OpenWeather.

Run:
`python weather_app.py`

### Weather Application — Web
A Flask web app with an HTML and CSS interface. The Python backend retrieves weather data from OpenWeather.

Run:
`python weather_web/app.py`

## Setup

Install the dependencies:

`python -m pip install -r requirements.txt`

The weather apps need an OpenWeather API key in a local `.env` file. Keep that file private and do not commit it.

The scraper needs an internet connection. The source website may change its page layout, which can affect scraping.