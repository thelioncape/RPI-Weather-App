import urllib.request
import json

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
data = response.read()
text = data.decode('utf-8')

print(text)
