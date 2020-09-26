import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/olympiad-of-babylon', methods=['POST'])
def olympiad_of_babylon():
	# Parsing input
	byte_value = request.data

	# Decode UTF-8 bytes to Unicode, and convert single quotes
	# to double quotes to make it valid JSON
	my_json = byte_value.decode('utf8').replace("'", '"')

	# Load the JSON to a Python list & dump it back out as formatted JSON
	data = json.loads(my_json)

	print(data)

	return json.dumps(data)
