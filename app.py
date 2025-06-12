from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)
API_KEY = os.getenv("API_KEY") # Replace with your key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    forecast_data = []

    if request.method == 'POST':
        city = request.form['city']
        current = get_weather(city)
        forecast = get_forecast(city)

        if current.get("cod") == 200:
            weather_data = {
                'city': current['name'],
                'temp': current['main']['temp'],
                'desc': current['weather'][0]['description'],
                'icon': current['weather'][0]['icon'],
                'lat': current['coord']['lat'],
                'lon': current['coord']['lon']
            }

            forecast_data = [
                {
                    'date': item['dt_txt'],
                    'temp': item['main']['temp'],
                    'desc': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                }
                for item in forecast['list'][::8]  # Every 24 hours (~5 days)
            ]
        else:
            weather_data['error'] = 'City not found or API limit reached.'

    return render_template("index.html", weather=weather_data, forecast=forecast_data)

if __name__ == '__main__':
    app.run(debug=True)
