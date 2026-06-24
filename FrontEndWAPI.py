import tkinter as tk
from weatherApi import update_weather

window = tk.Tk()
window.title("Weather App")
window.geometry("500x600")

title = tk.Label(window, text="Live Weather", font=("Arial", 16, "bold"))
title.pack(pady=10)

city_entry = tk.Entry(window, font=("Arial", 12))
city_entry.pack(pady=5)
city_entry.insert(0, "Sioux Falls")

result_label = tk.Label(
    window,
    text="Click Refresh",
    justify="left",
    font=("Courier New", 10)
)

result_label.pack(pady=10)

def refresh_weather():
    city = city_entry.get()
    result = update_weather(city)
    result_label.config(text=result)

refresh_button = tk.Button(
    window,
    text="Refresh Weather",
    command=refresh_weather
)

refresh_button.pack(pady=10)

refresh_weather()

window.mainloop()