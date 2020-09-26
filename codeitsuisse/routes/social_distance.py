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

	pp.pprint(data)

	print(data)
	print(type(data))

	return json.dumps(data)
