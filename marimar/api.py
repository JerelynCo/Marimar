from flask import Flask, render_template, make_response
from flask_restful import Api, Resource
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np

app = Flask(__name__)
api = Api(app)

"""
Loading of data
"""
hosp_data = pd.read_csv("data/processed/hospitals_with_facilities.csv")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

"""
API for topfive nearby hospitals
"""
class TopFive(Resource):
    hosp_data['dist'] = 0.0
    def get(self, pt1_lon, pt1_lat):
        for i in range(hosp_data.shape[0]):
            hosp_data['dist'][i] = haversine(pt1_lon, pt1_lat, hosp_data['lon'][i], hosp_data['lat'][i])
        return make_response(hosp_data.sort(columns='dist')[:5].to_json(orient='records'))
api.add_resource(TopFive, '/topfive/<float:pt1_lon>/<float:pt1_lat>')

"""
API for Health Center info
"""
class HospInfo(Resource):
    hospInfo = pd.DataFrame()

    def get(self):
        hospInfo = hosp_data[['Facility Name', 'Type', 'Classification', 'Street Name and #', 'Barangay Name', 'city', 'lon', 'lat', 'Landline Number']]
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

        for i in filtered['city'].unique():
            city = np.append(city, i)
            count = np.append(count, filtered[filtered['city'] == i]['city'].size)

        cityCount['city'] = city
        cityCount['count'] = count

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
