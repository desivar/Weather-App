import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime

API_KEY = 'YOUR_API_KEY'  # Replace with your OpenWeatherMap API key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def update_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city or country.")
        return

    weather_data = get_weather(city)
forecast_data = get_forecast(city)

if weather_data['cod'] != 200:
        messagebox.showerror("Error", "City not found.")
        return

    # Current weather
current_temp = weather_data['main']['temp']
weather_desc = weather_data['weather'][0]['description']
weather_icon = weather_data['weather'][0]['icon']
icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"

    # Update current weather display
    current_weather_label.config(text=f"Current Weather in {city}: {current_temp}°C, {weather_desc.capitalize()}")
    weather_icon_label.config(image=weather_icon_img(icon_url))

    # Update forecast
    forecast_text = "5-Day Forecast:\n"
    for i in range(0, 40, 8):  # Every 8th entry is a new day
        day_temp = forecast_data['list'][i]['main']['temp']
        day_desc = forecast_data['list'][i]['weather'][0]['description']
        forecast_text += f"Day {i//8 + 1}: {day_temp}°C, {day_desc.capitalize()}\n"

    forecast_label.config(text=forecast_text)

    # Suggest activities based on weather
    suggest_activities(weather_desc)

def weather_icon_img(icon_url):
    response = requests.get(icon_url)
    img_data = response.content
    with open('weather_icon.png', 'wb') as handler:
        handler.write(img_data)
    return tk.PhotoImage(file='weather_icon.png')

def suggest_activities(weather_desc):
    activities = {
        "clear sky": "Great day for a picnic!",
        "few clouds": "Perfect for a walk in the park!",
        "scattered clouds": "How about a bike ride?",
        "broken clouds": "A good day for reading indoors.",
        "shower rain": "Time for a movie marathon!",
        "rain": "Best to stay indoors and enjoy a hot drink.",
         "thunderstorm": "Stay safe! Maybe read a book.",
        "snow": "Perfect for building a snowman!",
        "mist": "A cozy day for indoor activities."
    }
    activity = activities.get(weather_desc, "Enjoy your day!")
    activity_label.config(text=activity)

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x600")
root.configure(bg="#87CEEB")  # Light blue background
# Create input frame
input_frame = ttk.Frame(root)
input_frame.pack(pady=20)

# Create input field
city_entry = ttk.Entry(input_frame, width=30, font=("Helvetica", 14))
city_entry.pack(side=tk.LEFT, padx=10)

# Create button
get_weather_button = ttk.Button(input_frame, text="Get Weather", command=update_weather)
get_weather_button.pack(side=tk.LEFT)

# Create labels for displaying weather
current_weather_label = ttk.Label(root, text="", font=("Helvetica", 14), background="#87CEEB")
current_weather_label.pack(pady=10)

weather_icon_label = ttk.Label(root, background="#87CEEB")
weather_icon_label.pack(pady=10)

forecast_label = ttk.Label(root, text="", font=("Helvetica", 12), background="#87CEEB")
forecast_label.pack(pady=10)

activity_label = ttk.Label(root, text="", font=("Helvetica", 12), background="#87CEEB")
activity_label.pack(pady=10)
# Start the GUI loop
root.mainloop()