import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/geometry', methods=['POST'])
def evaluateGeometry():
    data = request.get_json()

    lineCoordinates = data["lineCoordinates"]
    shapeCoordinates = data["shapeCoordinates"]

    result = []

    A, B = lineCoordinates[0], lineCoordinates[1]
    a = B["y"] - A["y"]
    b = A["x"] - B["x"]
    c = B["x"] * A["y"] - A["x"] * B["y"]
    m = -a / b
    d = A["y"] - m * A["x"]

    sign = []

    for shapeCoordinate in shapeCoordinates:
        tmp = False if ((shapeCoordinate["y"] - m * shapeCoordinate["x"] - d) < 0) else True
        sign.append(tmp)

    n = len(shapeCoordinates)

    for i in range(n):
        if sign[i] == sign[(i + 1) % n]:
            continue
        p, q = shapeCoordinates[i], shapeCoordinates[(i + 1) % n]
        u = abs(a * p["x"] + b * p["y"] + c)
        v = abs(a * q["x"] + b * q["y"] + c)
        x, y = (p["x"] * v + q["x"] * u) / (u + v), (p["y"] * v + q["y"] * u) / (u + v)
        result.append({"x": x, "y": y})
        
    logging.info("My result :{}".format(result))
    return jsonify(result)


