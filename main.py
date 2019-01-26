import urllib.request
import json
from time import sleep
import RPi.GPIO as GPIO

url = "http://api.openweathermap.org/data/2.5/weather?"


def setup_pins():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.OUT)  # North LED
    GPIO.setup(12, GPIO.OUT)  # North-East LED
    GPIO.setup(16, GPIO.OUT)  # East LED
    GPIO.setup(18, GPIO.OUT)  # South-East LED
    GPIO.setup(22, GPIO.OUT)  # South LED
    GPIO.setup(24, GPIO.OUT)  # South-West LED
    GPIO.setup(26, GPIO.OUT)  # West LED
    GPIO.setup(28, GPIO.OUT)  # North-West LED


def round_to_compass_point(number):
    # Take degrees, devide by 45 and ronud to find direction in number
    # 0 is North and clockwise until 7 is North-West
    return round(int(number) / 45)


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
    wind_speed = int(int(weather['wind']['speed'])*2.236936)
    if wind_speed > 100:
        wind_speed = 100
    wind_direction = round_to_compass_point(weather['wind']['deg'])
    return [wind_speed, wind_direction]


def set_wind_direction(direction):
    GPIO.output(10, GPIO.LOW)  # North
    GPIO.output(12, GPIO.LOW)  # North-East
    GPIO.output(16, GPIO.LOW)  # East
    GPIO.output(18, GPIO.LOW)  # South-East
    GPIO.output(22, GPIO.LOW)  # South
    GPIO.output(24, GPIO.LOW)  # South-West
    GPIO.output(26, GPIO.LOW)  # West
    GPIO.output(28, GPIO.LOW)  # North-West
    if direction == 0:
        GPIO.output(10, GPIO.HIGH)
    elif direction == 1:
        GPIO.output(12, GPIO.HIGH)
    elif direction == 2:
        GPIO.output(16, GPIO.HIGH)
    elif direction == 3:
        GPIO.output(18, GPIO.HIGH)
    elif direction == 4:
        GPIO.output(22, GPIO.HIGH)
    elif direction == 5:
        GPIO.output(24, GPIO.HIGH)
    elif direction == 6:
        GPIO.output(26, GPIO.HIGH)
    elif direction == 7:
        GPIO.output(28, GPIO.HIGH)


def set_wind_speed(speed):
    # take speed and divide by 100. Times result by total time in one iteration
    # one iteration should last 0.01 seconds
    ontime = (speed / 100) * 0.01
    offtime = 0.01 - ontime
    for i in range(5000):
        GPIO.output(32, GPIO.HIGH)
        sleep(ontime)
        GPIO.output(32, GPIO.LOW)
        sleep(offtime)

while True:
    wind = get_wind()
    set_wind_direction(wind[1])
    set_wind_speed(wind[0])
