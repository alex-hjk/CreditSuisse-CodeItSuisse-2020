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
	req = request.get_json()
	res = {
		"answers": {}
	}
	testCases = req["tests"]
	for test in testCases:
		print(test)
		info = testCases[test]
		res["answers"][test] = numWays(info)
	return json.dumps(res)
	
factorials = [1]

def numWays(info):
	numPeople = info["people"]
	numSpaces = info["spaces"]
	numSeats = info["seats"]
	minSeats = numPeople+(numPeople-1)*numSpaces
	if numSeats<minSeats:
		return 0
	elif numSeats==minSeats:
		return 1
	else:
		r = numPeople
		n = r+numSeats-minSeats
		return int(getFactorial(n)/(getFactorial(r)*getFactorial(n-r)))
	

def getFactorial(num):
	size=len(factorials)
	if size>num:
		return factorials[num]
	else:
		while size<=num:
			factorials.append(factorials[size-1]*size)
			size+=1
		return factorials[num]