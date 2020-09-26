import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def intelligent_farming():
    data = request.get_json()
    logging.info("My data :{}".format(data))

    runId = data["runId"]
    input_list = data["list"]

    output_list = []

    for _input in input_list:
        _id = _input['id']
        gene = _input['geneSequence']

        res = ""
        print(gene)
        a = gene.count("A")
        c = gene.count("C")
        g = gene.count("G")
        t = gene.count("T")
        print(a, c, g, t)

        c_pair = int(c / 2)  # Number of CC pairs
        c_indiv = c % 2  # Is there a single C left after pairing

        print("c", c_pair, c_indiv)

        if c_indiv == 1 and a >= 1 and c >= 1 and t >= 1:
            # Check if worth it to use ACGT or split up
            rem = a  # Remaining A's left if using ACGT combi
            rem -= 2  # Start new sequence with A|ACGT
            rem -= (c_pair + (g - 1) + (t - 1)) * 2  # Subtract AA|x triplets
            if rem < 6:  # Tolerance is <6. Above which not worth it to use ACGT
                if a >= 2:
                    res += "A"
                    a -= 1
                res += "ACGT"
                a -= 1
                c_indiv -= 1
                g -= 1
                t -= 1

        a_pair = int(a / 2)
        a_indiv = a % 2
        x = min(a_pair, c_pair)
        res += "AACC" * x
        a_pair -= x
        c_pair -= x
        print(a_pair, c_pair)

        x = min(a_pair, c_indiv)
        res += "AAC" * x
        a_pair -= x
        c_indiv -= x
        print(a_pair, c_pair)

        x = min(a_pair, g)
        res += "AAG" * x
        a_pair -= x
        g -= x
        print(a_pair, g)

        x = min(a_pair, t)
        res += "AAT" * x
        a_pair -= x
        t -= x
        print(a_pair, t)

        res += "AA" * a_pair + "A" * a_indiv
        res += "CC" * c_pair + "C" * c_indiv
        res += "G" * g
        res += "T" * t

        output_list.append({"id": _id, "geneSequence": res})

    result = {"runId": runId, "list": output_list}

    logging.info("My result :{}".format(result))

    return jsonify(result)


