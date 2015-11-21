from flask import Flask, render_template, make_response
from flask_restful import Api, Resource
from math import radians, cos, sin, asin, sqrt
import pandas as pd

app = Flask(__name__)
api = Api(app)

"""
Loading of data
"""

hosp_data = pd.read_csv("data/processed/hiv_testing_centers.csv")

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

hosp_data['dist'] = 0.0
class TopFive(Resource):
    def get(self, pt1_lon, pt1_lat):
        for i in range(hosp_data.shape[0]):
            hosp_data['dist'][i] = haversine(pt1_lon, pt1_lat, hosp_data['lon'][i], hosp_data['lat'][i])
        return make_response(hosp_data.sort(columns='dist')[:5].to_json(orient='records'))
api.add_resource(TopFive, '/topFive/<float:pt1_lon>/<float:pt1_lat>')


class CityCount(Resource):
    def get(self, level):
        return make_response(hosp_data[hosp_data['level']==level].size)
api.add_resource(CityCount, '/cityCount/<string:level>')



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
