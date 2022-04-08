import requests
import json

from api_key import *

with open('places.json') as f:
    with open('out.txt', 'a+') as out:
        places = json.load(f)
        output = []
        for place in places:
            place_id = place["place_id"]
            api_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}&fields=opening_hours"
            response = requests.get(api_url).json()
            if 'opening_hours' in response['result']:
                #print(json.dumps(response['result']['opening_hours']['weekday_text'], indent=4, sort_keys=True))
                text = ''
                for day in response['result']['opening_hours']['weekday_text']:
                    text += day + '\n'
                print(text)
                out.write(place['name'])
                out.write('\n')
                out.write(text)
                out.write('\n')
            else:
                out.write(place['name'])
                out.write('\n')
                out.write('error')
                out.write('\n')
                out.write('\n')

