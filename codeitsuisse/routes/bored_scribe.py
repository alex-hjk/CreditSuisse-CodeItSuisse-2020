import logging
import json
import urllib
from math import log
import os

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/bored-scribe', methods=['POST'])
def bored_scribe():
    data = request.get_json()
    logging.info("My data :{}".format(data))

    def palindromes(text):
        results = set()
        text_length = len(text)
        for idx, char in enumerate(text):

            # Check for longest odd palindrome(s)
            start, end = idx - 1, idx + 1
            while start >= 0 and end < text_length and text[start] == text[end]:
                results.add(text[start:end + 1])
                start -= 1
                end += 1

            # Check for longest even palindrome(s)
            start, end = idx, idx + 1
            while start >= 0 and end < text_length and text[start] == text[end]:
                results.add(text[start:end + 1])
                start -= 1
                end += 1

        return list(results)

    def reverse_cipher(text, shift):
        ans = ""
        for _ in text:
            ans += chr(((ord(_) + 26 - shift - 97) % 26) + 97)

        return ans

    def infer_spaces(s):
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
            return min((c + wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1, len(s) + 1):
            c, k = best_match(i)
            cost.append(c)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i > 0:
            c, k = best_match(i)
            assert c == cost[i]
            out.append(s[i - k:i])
            i -= k

        return " ".join(reversed(out))

    print(data)

    _id = data[0]["id"]
    text = data[0]["encryptedText"]

    # Init infer space
    # words = open(os.path.join(os.getcwd(), "words.txt")).read().split()
    words = urllib.request.urlopen("https://raw.githubusercontent.com/YeeeeeHan/SG-alexyhjs/master/codeitsuisse/routes"
                               "/words.txt").read().decode("utf-8").split()
    print(words)
    wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
    maxword = max(len(x) for x in words)

    pals = palindromes(text)

    pals.sort(key=len, reverse=True)
    res = len(pals)

    print("pals", pals)

    if pals:

        for char in pals[0]:
            print(char, ord(char))
            res += ord(char)

        print(res, res % 26)
        print()

        alpha = pals[0]
        # alpha = "oxzbzxo"
        # alpha = "abcdefghijklmnopqrstuvwxyz"

        for i in range(26):
            diff = 0
            for char in alpha:
                x = ord(char)
                split = 97 + i
                if x < split:
                    tmp = 26 - i
                else:
                    tmp = -i
                diff += tmp

            print(diff, (res + diff) % 26, i)
            if (res + diff) % 26 == i:
                print(i)
                orig = reverse_cipher(text, i)
                print(orig)
                # break

    else:
        orig = reverse_cipher(text, ord(text[0]) % 26)

    sentence = infer_spaces(orig)
    print(sentence)

    result = [{"id": _id, "encryptionCount": 1, "originalText": sentence}]

    logging.info("My result :{}".format(result))
    return jsonify(result)


