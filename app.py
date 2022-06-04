from math import sqrt

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():  # put application's code here
	return 'send location name requests to /location?lat=LV95_latitude&lng=LV95_longitude'


class Location(Resource):
	def __init__(self):
		self.all_locs = pd.read_csv('locations_ch.csv')
		self.example_locs = self.all_locs.iloc[:5]

	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('lat', required=True)
		parser.add_argument('lng', required=True)
		args = parser.parse_args()
		closest = self.get_closest(args['lat'], args['lng'])
		return {'data': closest.to_dict()}

	def get_closest(self, lat, lng):
		locs_of_interest = self.all_locs[
			self.all_locs['N'].between(float(lng) - 1000, float(lng) + 1000) &
			self.all_locs['E'].between(float(lat) - 1000, float(lat) + 1000)
			]
		for loc_i, location in locs_of_interest.iterrows():
			locs_of_interest.loc[loc_i, 'dist'] = sqrt((float(location['N']) - float(lng)) ** 2 + (
					float(location['E']) - float(lat)) ** 2)
		locs_of_interest.sort_values(by='dist', ascending=True, inplace=True)
		return locs_of_interest.iloc[0]


api.add_resource(Location, '/location')

if __name__ == '__main__':
	app.run()
