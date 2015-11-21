from flask import Flask, render_template, make_response
from flask_restful import Api, Resource
import pandas as pd

app = Flask(__name__)
api = Api(app)


hiv_testing = pd.read_csv("data/with_lat_lon/hiv_testing_centers.csv")
hiv_treatment = pd.read_csv("data/with_lat_lon/hiv_treatment_centers.csv")


class HivTesting(Resource):
    def get(self):
        data = hiv_testing
        return make_response(data.to_json(orient='records'))
api.add_resource(HivTesting, '/api/hivtesting')

class HelloWorld(Resource):
	def get(self):
		return {'Hello':'world'}
api.add_resource(HelloWorld, '/')

@app.route('/index')
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
