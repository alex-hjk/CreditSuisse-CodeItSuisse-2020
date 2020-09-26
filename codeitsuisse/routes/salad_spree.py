import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def salad_spree():
	data = request.get_json();

	number_of_salads = data["number_of_salads"]
	salad_prices_street_map = data["salad_prices_street_map"]

	print(number_of_salads, file=sys.stdout)
	print(salad_prices_street_map, file=sys.stdout)

	output = {"result": 1}

	return jsonify(output);
