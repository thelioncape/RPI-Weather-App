import requests
import json
from time import sleep
import RPi.GPIO as GPIO

url = "http://api.openweathermap.org/data/2.5/weather?"


def setup_pins():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.OUT)  # North LED
    GPIO.setup(11, GPIO.OUT)  # North-East LED
    GPIO.setup(16, GPIO.OUT)  # East LED
    GPIO.setup(18, GPIO.OUT)  # South-East LED
    GPIO.setup(22, GPIO.OUT)  # South LED
    GPIO.setup(24, GPIO.OUT)  # South-West LED
    GPIO.setup(26, GPIO.OUT)  # West LED
    GPIO.setup(5, GPIO.OUT)   # North-West LED
    GPIO.setup(12, GPIO.OUT)  # VU Out


def round_to_compass_point(number):
    # Take degrees, devide by 45 and ronud to find direction in number
    # 0 is North and clockwise until 7 is North-West
    return round(int(number) / 45)


def get_weather():
    with open("data.txt", 'r') as f:
        datafile = f.readlines()

    appid = datafile[0].rstrip()  # API Key
    cityid = datafile[1].rstrip()  # City ID

    requesturl = url + "id=" + cityid + "&APPID=" + appid
    try:
        response = requests.get(requesturl).text
    except Exception as e:
        print(e)
        input("Press enter to exit")
        exit()

    return json.loads(response)


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
    GPIO.output(11, GPIO.LOW)  # North-East
    GPIO.output(16, GPIO.LOW)  # East
    GPIO.output(18, GPIO.LOW)  # South-East
    GPIO.output(22, GPIO.LOW)  # South
    GPIO.output(24, GPIO.LOW)  # South-West
    GPIO.output(26, GPIO.LOW)  # West
    GPIO.output(5, GPIO.LOW)  # North-West
    if direction == 0:  # North
        GPIO.output(10, GPIO.HIGH)
    elif direction == 1:  # North-East
        GPIO.output(11, GPIO.HIGH)
    elif direction == 2:  # East
        GPIO.output(16, GPIO.HIGH)
    elif direction == 3:  # South-East
        GPIO.output(18, GPIO.HIGH)
    elif direction == 4:  # South
        GPIO.output(22, GPIO.HIGH)
    elif direction == 5:  # South-West
        GPIO.output(24, GPIO.HIGH)
    elif direction == 6:  # West
        GPIO.output(26, GPIO.HIGH)
    elif direction == 7:  # North-West
        GPIO.output(5, GPIO.HIGH)

setup_pins()
pwm = GPIO.PWM(12, 100)
pwm.start(0)

try:
    while True:
        wind = get_wind()
        set_wind_direction(wind[1])
        pwm.ChangeDutyCycle(wind[0])
        sleep(60)
except KeyboardInterrupt:
    print("Ctrl-C Pressed. Exiting...")

pwm.stop()
GPIO.cleanup()
