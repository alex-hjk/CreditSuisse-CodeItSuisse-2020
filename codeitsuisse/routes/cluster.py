import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/cluster', methods=['POST'])
def cluster():
	# Parsing input
	byte_value = request.data

	# Decode UTF-8 bytes to Unicode, and convert single quotes
	# to double quotes to make it valid JSON
	my_json = byte_value.decode('utf8').replace("'", '"')

	# Load the JSON to a Python list & dump it back out as formatted JSON
	grid = json.loads(my_json)

	print(grid)


	# Start of function
	res = 0
	for row in range(0, len(grid)):
		for col in range(0, len(grid[row])):
			if grid[row][col] == '1':
				res += 1
				dfs(grid, row, col)
			# print(DataFrame(grid))

	output = {"answer": res}
	return jsonify(output);


def dfs(grid, row, col):
	grid[row][col] = 'X'
	bottom = row + 1
	top = row - 1
	right = col + 1
	left = col - 1

	# Top left
	if top >= 0 and left >= 0:
		if grid[top][left] == '0' or grid[top][left] == '1':
			dfs(grid, top, left)

	# Top
	if top >= 0:
		if grid[top][col] == '0' or grid[top][col] == '1':
			dfs(grid, top, col)

	# Top right
	if top >= 0 and right != len(grid[0]):
		if grid[top][right] == '0' or grid[top][right] == '1':
			dfs(grid, top, right)

	# Right
	if right != len(grid[0]):
		if grid[row][right] == '0' or grid[row][right] == '1':
			dfs(grid, row, right)

	# Bottom Right
	if bottom != len(grid) and right != len(grid[0]):
		if grid[bottom][right] == '0' or grid[bottom][right] == '1':
			dfs(grid, bottom, right)

	# Bottom
	if bottom != len(grid):
		if grid[bottom][col] == '0' or grid[bottom][col] == '1':
			dfs(grid, bottom, col)

	# Bottom Left
	if bottom != len(grid) and left >= 0:
		if grid[bottom][left] == '0' or grid[bottom][left] == '1':
			dfs(grid, bottom, left)

	# Left
	if left >= 0:
		if grid[row][left] == '0' or grid[row][left] == '1':
			dfs(grid, row, left)
