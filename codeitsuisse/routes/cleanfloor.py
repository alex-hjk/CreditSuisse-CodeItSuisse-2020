import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/clean_floor', methods=['POST'])
def clean_floor():
	req = request.get_json()
	print(type(req))
	print(req)
	res = {
		"answers": {}
	}
	for test in req["tests"]:
		res["answers"][test] = getMinMoves(req["tests"][test])

	return json.dumps(res)

def getMinMoves(floorArray):
	return 0