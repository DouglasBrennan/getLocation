from math import sqrt

from flask import Flask, request
from flask_restful import Resource, Api
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
		lat = float(request.args.get("lat", None))
		lng = float(request.args.get("lng", None))
		closest = self.get_closest(lat, lng)
		return {'data': closest.to_dict()}

	def get_closest(self, lat, lng):
		locs_of_interest = self.all_locs[
			self.all_locs['N'].between(lng - 1000, lng + 1000) &
			self.all_locs['E'].between(lat - 1000, lat + 1000)
			]
		locs_of_interest['dist'] = None
		for loc_i, location in locs_of_interest.iterrows():
			locs_of_interest.loc[loc_i, 'dist'] = sqrt((float(location['N']) - lng) ** 2 + (
					float(location['E']) - lat) ** 2)
		locs_of_interest.sort_values(by='dist', ascending=True, inplace=True)
		return locs_of_interest.iloc[0]


api.add_resource(Location, '/location')

if __name__ == '__main__':
	app.run()
	app.run(debug=True)
