
import flask
import json
import requests
from api_key import *

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def results():
    context={
        'results':[]
    }

    checkbox_fields = ["food", "open_now", "study_rooms"]

    with open('places.json') as f:
        places = json.load(f)
        for place in places:
            candidate = True
            for attr, val in flask.request.form.items():
                if attr not in checkbox_fields:
                    if val != place[attr]:
                        candidate = False 
                        break 
                else:
                    if attr == "open_now":
                        place_id = place["place_id"]
                        api_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}&fields=opening_hours"
                        response = requests.get(api_url).json()
                        if ('opening_hours' not in response['result'].keys()):
                            candidate = False
                        elif not response['result']['opening_hours']['open_now']:
                            candidate = False
                    else:
                        if not place[attr]:
                            candidate = False
            if candidate:
                context['results'].append(place)

    return flask.render_template("./index.html", **context)