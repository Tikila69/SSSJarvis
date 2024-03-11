import requests
import json


def weatherChecker(when):
    data = requests.get('https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Hønefoss,NO/'+when+'?key=LZXY8XB4SR6YC6RSFVVS952JG').json()


    description = data["days"][0]["description"]
    current = data["days"][0]["temp"]
    high = data["days"][0]["tempmax"]
    low = data["days"][0]["tempmin"]
    

    print("Description: ", description)
    print("High: ", high)
    print("Low: ", low)
    
    return description, high, low