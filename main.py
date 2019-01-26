import urllib.request
import json
import RPi.GPIO as GPIO



def round_to_compass_point(number):
    return round(int(number) / 45)

"""

0: North
1: North-East
2: East
3: South-East
4: South
5: South-West
6: West
7: North-West

"""

url = "http://api.openweathermap.org/data/2.5/weather?"

with open("data.txt", 'r') as f:
    datafile = f.readlines();

appid = datafile[0] # API Key
id = datafile[1] # City ID

requesturl = url + "id=" + id + "&APPID=" + appid
try:
    response = urllib.request.urlopen(requesturl)
except Exception as e:
    print(e)
    input("Press enter to exit")
    exit()

weather = json.load(response)

wind_speed = weather['wind']['speed']
wind_direction = round_to_compass_point(weather['wind']['deg'])


