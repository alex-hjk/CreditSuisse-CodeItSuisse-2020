import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)


# print(number_of_salads, file=sys.stdout)
# print(salad_prices_street_map, file=sys.stdout)

@app.route('/salad-spree', methods=['POST'])
def salad_spree():
	# Parsing input
	data = request.get_json();
	k = data["number_of_salads"]
	salad_prices_street_map = data["salad_prices_street_map"]

	street_length = len(salad_prices_street_map[0])

	min_price = float("inf")
	i = 0

	for street in salad_prices_street_map:
		consecutive = 0
		street_price = 0
		current_left = 0
		i = 0

		while i < street_length:

			if street[i] == 'X':
				print(f'i:{i} Encounter X')
				# Comparison of k against street_length - quit early if 'X' is found within last K elements
				if i >= street_length - k:
					print('Early break street')
					break
				current_left = i + 1

				# Reset consecutive stalls
				consecutive = 0
				street_price = 0

				i += 1
				continue

			if consecutive < k:
				street_price += int(street[i])

				consecutive += 1
				print(
					f"i:{i} -Building- street_price: {street_price}, consecutive: {consecutive}, curr_left: {current_left}")
				i += 1

			if consecutive == k:
				min_price = min(street_price, min_price)
				print(f'     - Saved price1: {street_price}')

				while i < street_length:
					# Terminate if window encounters X
					if street[i] == 'X':
						consecutive = 0
						print(f'   While break sliding window, i: {i}')
						break

					# Evaluate current consecutive streak
					street_price -= int(street[current_left])
					street_price += int(street[i])
					min_price = min(street_price, min_price)

					print(
						f"   While -- i:{i}, street_price: {street_price}, consecutive: {consecutive}, curr_left: {current_left}")
					print(f'     - Saved price2: {street_price}')
					current_left += 1
					i += 1
		print(f'END min_price: {min_price}\n')

	output = {"result": min_price, "stree": i}

	return jsonify(output);
