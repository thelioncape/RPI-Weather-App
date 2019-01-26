import urllib.request
import json
import time
# import RPi.GPIO as GPIO

url = "http://api.openweathermap.org/data/2.5/weather?"


def round_to_compass_point(number):
    # Take degrees, devide by 45 and ronud to find direction from table below
    return round(int(number) / 45)

# 0: North
# 1: North-East
# 2: East
# 3: South-East
# 4: South
# 5: South-West
# 6: West
# 7: North-West


def get_weather():
    with open("data.txt", 'r') as f:
        datafile = f.readlines()

    appid = datafile[0]  # API Key
    id = datafile[1]  # City ID

    requesturl = url + "id=" + id + "&APPID=" + appid
    try:
        response = urllib.request.urlopen(requesturl)
    except Exception as e:
        print(e)
        input("Press enter to exit")
        exit()

    return json.load(response)


def get_wind():
    # Gets wind speed and direction and outputs in mph and compass point
    # Returns list as [speed, direction]
    weather = get_weather()
    wind_speed = weather['wind']['speed']
    # Convert meter per second to miles per hour
    wind_speed = float(weather['wind']['speed'])*2.236936
    wind_direction = round_to_compass_point(weather['wind']['deg'])
    return [wind_speed, wind_direction]


while True:
    print(get_wind())
    time.sleep(60)

