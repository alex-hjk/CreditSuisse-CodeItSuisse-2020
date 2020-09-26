import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def inventory_management():
	data = request.get_json()
	print(type(data))
	print(data)
	searchItem = data["searchItemName"]
	items = data["items"]
	result = topTenMatches(items,searchItem)
	resp = {
		"searchItemName": searchItem,
		"searchResult": result
	}
	return json.dumps(resp)

def levenshteinDistance(startStr, endStr):
	result = ""
	startSize = len(startStr)
	endSize = len(endStr)
	distGrid = [[0]*(endSize+1)]*(startSize+1)
	for i in range(endSize+1):
		distGrid[0][i] = i
	for i in range(startSize):
		distGrid[i+1][0] = i+1
		for j in range(endSize):
			if startStr[i].lower()==endStr[j].lower():
				distGrid[i+1][j+1] = distGrid[i][j]
			else:
				distGrid[i+1][j+1] = min(distGrid[i+1][j],distGrid[i][j],distGrid[i][j+1])+1

	row = startSize
	col = endSize

	while row>0 and col>0:
		if startStr[row-1].lower()==endStr[col-1].lower():
			result = startStr[row-1]+result
			row-=1
			col-=1
		else:
			if row==col:
				if distGrid[row-1][col-1]<distGrid[row][col]:
					result=endStr[row-1]+result
					row-=1
					col-=1
				elif distGrid[row][col-1]<distGrid[row][col]:
					result='+'+endStr[col-1]+result
					col-=1
				else:
					result='-'+startStr[row-1]+result
			elif row<col:
				if distGrid[row][col-1]<distGrid[row][col]:
					result='+'+endStr[col-1]+result
					col-=1
				else:
					result=endStr[col-1]+result
					row-=1
					col-=1
			else:
				if distGrid[row-1][col]<distGrid[row][col]:
					result='-'+startStr[row-1]+result
					row-=1
				else:
					result=endStr[col-1]+result
					row-=1
					col-=1
	
	while row>0:
		result='-'+startStr[row-1]+result
		row-=1
	
	while col>0:
		result='+'+endStr[col-1]+result
		col-=1

	return distGrid[startSize][endSize],result

def cmp(item1, item2):
	if item1[0]==item2[0]:
		if item1[1]<item2[1]:
			return -1
		elif item1[1]>item2[1]:
			return 1
		else:
			return 0
	elif item1[0]<item2[0]:
		return -1
	else:
		return 1

def topTenMatches(searches, target):
	targetTokens = target.split()
	matchOrder = []
	for search in searches:
		searchTokens = search.split()
		totalEdits = 0
		editedStr = ""
		for i in range(len(searchTokens)):
			edits,subStr = levenshteinDistance(targetTokens[i],searchTokens[i])
			totalEdits += edits
			editedStr += subStr+" "
		editedStr=editedStr[:-1]
		currList = [totalEdits,search,editedStr]
		matchOrder.append(currList)

	sortedOrder = sorted(matchOrder, key=cmp)
	if len(sortedOrder)>10:
		sortedOrder=sortedOrder[:10]

	finalOrder = []
	for item in sortedOrder:
		finalOrder.append(item[2])

	return finalOrder