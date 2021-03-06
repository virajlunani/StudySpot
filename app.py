
import flask
import json
import requests
from api_key import *
from indexer import search_index, index_documents

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def results():
    if 'query' not in flask.request.form:
        index_documents()
    context={
        'results':[]
    }
    search_box_results = []
    checkbox_results = []

    checkbox_fields = ["food", "open_now", "study_rooms"]

    with open('places.json') as f:
        places = json.load(f)
        for place in places:
            candidate = True
            for attr, val in flask.request.form.items():
                if attr not in checkbox_fields and attr != 'query':
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
                        if attr != 'query' and not place[attr]:
                            candidate = False
            if candidate:
                checkbox_results.append(place)

    if 'query' not in flask.request.form or flask.request.form['query'] == '':
        search_box_results = checkbox_results
    else:
        search_box_results = search_index(flask.request.form['query'])
    for r in search_box_results:
        if r in checkbox_results:
            context['results'].append(r)

    # find which are favorited
    
    for place in context['results']:
        place['favorite'] = False
    if (flask.request.cookies.get('favs') != None):
        for place_id in flask.request.cookies.get('favs').split(',')[:-1]:
            for place in context['results']:
                if place['place_id'] == place_id:
                    place['favorite'] = True

    sorted_results = []
    for place in context['results']:
        if place['favorite']:
            sorted_results.append(place)
    for place in context['results']:
        if not place['favorite']:
            sorted_results.append(place)
    context['results'] = sorted_results

    
    context['no_results'] = True if len(context['results']) == 0 else False

    return flask.render_template("./index.html", **context)


@app.route('/favorites/', methods=['GET', 'POST'])
def favorites():
    context={
        'results':[]
    }

    with open('places.json') as f:
        places = json.load(f)
        for place in places:
            if (flask.request.cookies.get('favs') != None) and place['place_id'] in flask.request.cookies.get('favs').split(',')[:-1]:
                place['favorite'] = True
                context['results'].append(place)
    context['no_results'] = True if len(context['results']) == 0 else False
    return flask.render_template("./favorites.html", **context)