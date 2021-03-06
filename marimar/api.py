from flask import Flask, render_template, make_response
from flask_restful import Api, Resource
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import math

app = Flask(__name__)
api = Api(app)

"""
Loading of data
"""
hosp_data = pd.read_csv("data/processed/hospitals_complete.csv")

def haversine(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

"""
API for topfive nearby hospitals
"""
class TopFive(Resource):
    def get(self, facility, pt1_lon, pt1_lat):
        filtered = hosp_data[hosp_data[facility]==1].reset_index()
        filtered['dist'] = 0.0

        for i in range(filtered.shape[0]):
            filtered['dist'][i] = haversine((pt1_lat, pt1_lon), (filtered['lat'][i], filtered['lon'][i]))
        return make_response(filtered.sort(columns='dist', ascending=True)[0:5].to_json(orient='records'))
api.add_resource(TopFive, '/topfive/<string:facility>/<float:pt1_lon>/<float:pt1_lat>')

"""
API for Health Center info
"""
class HospInfo(Resource):
    hospInfo = pd.DataFrame()

    def get(self):
        hospInfo = hosp_data[['FacilityName', 'Type', 'Classification', 'StreetNameAndNo', 'BarangayName', 'City', 'lon', 'lat', 'LandlineNumber']]
        return make_response(hospInfo.to_json(orient='records'))
api.add_resource(HospInfo, '/hospinfo')


"""
API for cityCount per facility per city
"""
class CityCount(Resource):
    def get(self, facility):
        cityCount = pd.DataFrame()
        city = np.array([])
        count = np.array([])

        filtered = hosp_data[hosp_data[facility]==1]

        for i in filtered['City'].unique():
            city = np.append(city, i)
            count = np.append(count, filtered[filtered['City'] == i]['City'].size)

        cityCount['City'] = city
        cityCount['Count'] = count

        return make_response(cityCount.to_json(orient='records'))
api.add_resource(CityCount, '/citycount/<string:facility>')



@app.route('/')
def index():
    user = {'nickname': 'Je'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8000)
