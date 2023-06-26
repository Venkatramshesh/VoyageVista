from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import openai
from typing import Sequence
import os
import time
import io
import requests
import json
import random
import folium
from geopy.geocoders import Nominatim
import re

random_integer = random.randint(1, 20)  # Generates a random integer between 1 and 10



app = Flask(__name__)

static_folder_path = os.path.join(app.root_path, 'static')
@app.route('/')
def upload_file():
    city =["Charlotte", "Baltimore", "Charleston" , "DC", "Portland" , "Miami", "Nashville", "New York", "Philadelphia", "Savannah"]
    condition = ['Bicycle tour', 'Garden tour', 'Ghost tour','Happy Hour', 'Hiking','Pub crawl', 'Resturant run', 'Rickshaw ride','Walking tour' ]
    budget = ['0', '25', '50', '75', '100', '125','150', '175','200']
    time =  ['2', '3', '4', '5', '6', '7', '8']
    season = ['Fall', 'Spring','Summer', 'Winter']
    occasion = ['Anniversary', 'Bachelorette party', 'Bachelor party', 'Birthday' , 'Engagement', 'Graduation', 'Touristy']
    #type =  ['Indoor', 'Outdoor']

    return render_template('upload.html', city=city, condition=condition, budget=budget,time=time,season=season,occasion=occasion, type=type)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_image_file():
    if request.method == 'POST':
        city = request.form.get('city')
        condition = request.form.get('condition')
        budget = request.form.get('budget')
        time = request.form.get('time')
        season = request.form.get('season')
        occasion = request.form.get('occasion')


        credential_path = "C:\\Users\\venka\\googlecloud\\nimble-crane-389713-9afc3d3b7aff.json"

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


        input_text = []
        input_text.append(city)
        input_text.append(condition)
        #input_text.append(budget)
        #input_text.append(time)
        input_text.append(season)
        input_text.append(occasion)
        #input_text.append(gender)
        input_text.append(type)

        #print(input_text)

        import openai
        # Initialize OpenAI Chat model
        openai.api_key = 'xxxxx'
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The request for suggested activity contains: {input_text}. Given a budget of {budget}$ Create an itinerary based on time duration of {time} hours. Give address of each location in Address: fromat in itinerary"},
            #{"role": "user", "content": f"Can you give the coordinates of suggsted places in above itenary in an array called position "}
        ]

        # Use ChatGPT to generate advertising content
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # replace with gpt-4 or the latest version available
            messages=messages,
            temperature=0.65,
        )
        # print(response)
        #
        # addresses = re.findall(r'Address: (.*?)\\n', response)
        #
        #
        # for address in addresses:
        #     print(address)




        lines = response['choices'][0]['message']['content'].split('\n')  # splits the output into lines


        def search_images(search_term, api_key):
            base_url = "https://api.unsplash.com/search/photos"
            headers = {'Authorization': 'Client-ID ' + api_key}
            params = {
                'query': search_term,
                'per_page': 20,  # Number of results per request
            }
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()  # Raise exception if invalid response
            return response.json()

        api_key = "_bbvnXks0VwYSuaTp_BXSb_DM66RhwYonlwajXGHO1I"
        search_term = city  # Replace with the city you're interested in

        results = search_images(search_term, api_key)


        #print(results['results'][0]['description'])
        desc = results['results'][random_integer]['description']
        link = results['results'][random_integer]['urls']['small']

        # Create a Map instance



        geolocator = Nominatim(user_agent="vacationexecercise")

        location = geolocator.geocode(city)

        lat = location.latitude
        long = location.longitude
        m = folium.Map(location=[lat , long], zoom_start=12, width='40%', height='40%')

        # for address in addresses:
        #     location = geolocator.geocode(address)
        #     if location:
        #         folium.Marker(
        #             location=[location.latitude, location.longitude],
        #             popup=address,
        #         ).add_to(m)
        #
        # # Display the map
        m = m.get_root().render()

        #return render_template('home.html', lines=lines)
        return render_template('results.html',lines=lines, desc=desc,link=link, map=m)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
