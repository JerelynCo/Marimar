from flask import Flask, render_template
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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
