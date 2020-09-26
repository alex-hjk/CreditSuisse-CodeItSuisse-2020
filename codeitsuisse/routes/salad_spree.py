import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def salad_spree():
	data = request.get_json();

	logging.info(f"data sent for evaluation {data}")
	inputValue = data.get("input");

	result = inputValue * inputValue

	logging.info("My result :{}".format(result))

	print(data, file=sys.stdout)

	return json.dumps(result);
