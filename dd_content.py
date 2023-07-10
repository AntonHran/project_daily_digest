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
        with open(quotes_file) as f_csv:
            quotes = [{'author': line[0],
                       'quote': line[1]} for line in csv.reader(f_csv, delimiter='|')]
    except Exception as e:
        quotes = [{'author': 'Eric Idle',
                   'quote': 'AlwaysLook on the Bright Side of Life.'}]
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


if __name__ == '__main__':
    '''quote = get_quote()
    print(f'- Random quote is "{quote["quote"]}" - {quote["author"]}')
    quote = get_quote(quotes_file='')
    print(f'- Default quote is "{quote["quote"]}" - {quote["author"]}')
    print()

    forecast = get_weather()
    # print(forecast)
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is ')
        for period in forecast['periods']:
            print(f'- {period["timestamp"]} | {period["temp"]}*C | {period["description"]}')

    forecast = get_weather('Kyiv')
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is ')
        for period in forecast['periods']:
            print(f'- {period["timestamp"]} | {period["temp"]}*C | {period["description"]}')

    forecast = get_weather('blahblah')
    if forecast is None:
        print('Weather forecast for invalid city name is NONE!')
    print()

    trends = get_trends('Kyiv', 'Ukraine')
    text = ''
    if trends:
        # print(trends)
        text += f'*~*~*  Top Ten Twitter Trends in {trends[1]}  *~*~*\n\n'
        for trend in trends[0][0:10]:
            text += f'- {trend["name"]}: {trend["url"]}\n'
        text += '\n'
    print(text)'''

    '''trends = get_trends(woeid=23424977)
    if trends:
        print('\nTop 10 Twitter trends in the USA are...')
        for trend in trends[0:10]:
            print(f'- {trend["name"]}: {trend["url"]}')

    trends = get_trends(woeid=-1)
    if trends is None:
        print('Twitter trends for invalid WOEID returned None.')

    article = get_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')'''

    '''tr = get_trends('Kyiv', 'Ukraine')
    print(tr)
    if tr:
        print(f'\nTop 10 Twitter trends in {tr[1]} are...')
        for trend in tr[0][0:10]:
            print(f'- {trend["name"]}: {trend["url"]}')'''

    '''forecast = get_weather('Den Haag')
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is ')
        for period in forecast['periods']:
            print(f'- {period["timestamp"]} | {period["temp"]}*C | {period["description"]}')
    with open('woeid.json', 'w') as file:
        json.dump(tr, file, indent=4)
    a = [location['name'] for location in tr if location['country'] == 'Netherlands']
    print(a)'''