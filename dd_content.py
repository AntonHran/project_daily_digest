import csv
import random
from urllib import request
import json
import datetime
import tweepy
import re


def get_keys_passwords(name: str) -> str:
    with open('api_keys.txt', 'r') as file:
        for line in file.readlines():
            if re.match(name, line):
                api_key: str = line.replace(name+' = ', '').strip()
                return api_key


def get_quote(quotes_file='quotes.csv'):
    try:
        with open(quotes_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=["quote", "author"], quoting=1)
            quotes = [row for row in reader]
    except Exception as e:
        quotes = [{'quote': 'AlwaysLook on the Bright Side of Life.',
                   'author': 'Eric Idle'}]
        print(e)
    return random.choice(quotes)


def get_weather(city_name):
    city_name = city_name.replace(' ', '+')
    if city_name:
        try:
            weather_api_key = get_keys_passwords('weather_api_key')
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={weather_api_key}'
            data = json.load(request.urlopen(url))
            forecast = {'city': data['city']['name'],
                        'country': data['city']['country'],
                        'periods': list()}
            for period in data['list'][0:9]:
                forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                            'temp': round(period['main']['temp'] - 273),
                                            'description': period['weather'][0]['description'].title(),
                                            'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}'})
            return forecast
        except Exception as e:
            print(e)


def get_trends(city, country) -> tuple:
    if city and country:
        try:
            tw_api_key = get_keys_passwords('tw_api_key')
            tw_api_secret_key = get_keys_passwords('tw_api_secret_key')
            auth = tweepy.AppAuthHandler(tw_api_key, tw_api_secret_key)
            geo = tweepy.API(auth).available_trends()
            trends = ''
            if woeid:=[location['woeid'] for location in geo if location['name'] == city]:
                trends = tweepy.API(auth).get_place_trends(woeid[0])[0]['trends']
            if trends:
                return trends, city
            else:
                woeid = [location['woeid'] for location in geo if location['name'] == country]
                return tweepy.API(auth).get_place_trends(woeid[0])[0]['trends'], country

        except Exception as e:
            print(e)


def get_article():
    try:
        data = json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {'title': data['title'],
                'extract': data['extract'],
                'url': data['content_urls']['desktop']['page']}
    except Exception as e:
        print(e)
