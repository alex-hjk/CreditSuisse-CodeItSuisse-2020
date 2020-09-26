import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/contact_trace', methods=['POST'])
def contact_trace():
	# Parsing input
	data = request.get_json();

	print(data)
	print(type(data))

	return json.dumps(data)
