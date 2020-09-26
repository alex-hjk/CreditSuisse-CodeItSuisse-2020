import logging
import json
import sys
import pprint as pp

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/social_distancing', methods=['POST'])
def social_distancing():
	# Parsing input
	data = request.get_json();

	test_dict = data['tests']

	output = {"answers": {}}

	for key, val in test_dict.items():
		seats = val["seats"]
		people = val["people"]
		spaces = val["spaces"]

		output["answers"][key] = SD(seats, people, spaces, (seats, people, spaces))

	return json.dumps(output)


def SD(seats, people, spaces, pas):
	print(f"input: {seats, people, spaces, pas}")

	# Base case - single person left
	if people == 1 and seats:
		return seats

	# Impossible case - not enough seats to accomodate people and spaces
	if seats < people + spaces:
		return 0

	# When you fill, have to pad spaces
	fill = SD(seats - spaces - 1, people - 1, spaces)
	print(f"  from fill {fill}")

	no_fill = SD(seats - 1, people, spaces)
	print(f"  from no_fill {no_fill}")

	return fill + no_fill
