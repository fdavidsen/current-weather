# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 11:05:13 2020

@author: Frederic Davidsen
"""


import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units={}&APPID=4f76a7813dc0be007057b3aa57f4414d'
    icon_url = 'http://openweathermap.org/img/w/{}.png'
    data = None
    units = {
        'metric': '°C',
        'imperial': '°F',
        'standard': ' K'
    }
    
    if request.method == 'POST':
        city_name = request.form.get('cityName')
        temperature_unit = request.form.get('temperatureUnits')
        
        r = requests.get(url.format(city_name, temperature_unit)).json()
        
        if r['cod'] == 200:
            data = {
                'status': r['cod'],
                'location': r['name'] + ', ' + r['sys']['country'],
                'temperature': str(r['main']['temp']) + units[temperature_unit],
                'description': r['weather'][0]['description'].capitalize(),
                'icon': icon_url.format(r['weather'][0]['icon']),
                'main': {
                    'feels_like': str(r['main']['feels_like']) + units[temperature_unit],
                    'timezone': str(r['timezone']) + ' seconds',
                    'humidity': str(r['main']['humidity']) + '%'
                },
                'coordinates': {
                    'latitude': r['coord']['lat'],
                    'longitude': r['coord']['lon']
                },
                'wind': {
                    'speed': str(r['wind']['speed']) + ' m/s',
                    'degree': str(r['wind']['deg']) + '°'
                }
            }
        else:
            data = {
                'status': r['cod'],
                'message': r['message'].capitalize()
            }
        
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()