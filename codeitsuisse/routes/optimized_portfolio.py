import logging
import json
import sys
import pprint as pp

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/optimizedportfolio', methods=['POST'])
def optimized_portfolio():
	req = request.get_json()
	res = {
		"outputs": []
		#list of dicts
	}
	testCases = req["inputs"] #testCases is a list of dicts
	for test in testCases:
		pfInfo = test["Portfolio"]
		print(pfInfo)
		idxInfo = test["IndexFutures"]
		print(idxInfo)
		res["outputs"].append(getOptimized(pfInfo,idxInfo))
	return json.dumps(res)

def getOptimized(pfDict, idxList):
	result = sorted(idxList, key = lambda x: (x["CoRelationCoefficient"]/x["FuturePrcVol"], 1/(x["IndexFuturePrice"]*x["Notional"])))
	print(result[0]["Name"])
	optRatio = round(result[0]["CoRelationCoefficient"]*pfDict["SpotPrcVol"]/result[0]["FuturePrcVol"],3)
	print(optRatio)
	numFtrs = round(optRatio*pfDict["Value"]/(result[0]["IndexFuturePrice"]*result[0]["Notional"]))
	print(numFtrs)

	return {
		"HedgePositionName": result[0]["Name"],
		"OptimalHedgeRatio": optRatio,
		"NumFuturesContract": numFtrs
	}