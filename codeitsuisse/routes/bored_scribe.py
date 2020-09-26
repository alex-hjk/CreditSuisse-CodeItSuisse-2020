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

    result = []

    # Init infer space
    words = urllib.request.urlopen(
        "https://raw.githubusercontent.com/YeeeeeHan/SG-alexyhjs/master/codeitsuisse/routes/words.txt").read().decode(
        "utf-8").split()
    wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
    maxword = max(len(x) for x in words)

    for test in range(len(data)):

        _id = data[test]["id"]
        text = data[test]["encryptedText"]
        tries = 1

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

        def reverse_cipher(text):
            ans = ""
            for _ in text:
                ans += chr(((ord(_) + 26 - 1 - 97) % 26) + 97)

            return ans

        def cipher_shift(text, shift):
            ans = ""
            for _ in text:
                ans += chr(((ord(_) + shift - 97) % 26) + 97)

            return ans

        def encrypt(text):
            pals = palindromes(text)

            pals.sort(key=len, reverse=True)
            shift = len(pals)

            print("pals", pals)

            if pals:
                for char in pals[0]:
                    print(char, ord(char))
                    shift += ord(char)

                print("res", shift % 26)

                return cipher_shift(text, shift % 26)
            else:
                return cipher_shift(text, ord(text[0]) % 26)

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

        new = text
        for shifts in range(26):
            new = reverse_cipher(new)
            print(new)

            sentence = infer_spaces(new)
            longest_word = len(max(sentence.split(), key=len))
            print(sentence)
            if longest_word > 5:
                print(shifts)
                break

        print(new)
        tries = 1
        while new != text:
            if tries == 100:
                break
            new = encrypt(new)
            print("try", tries, new)
            tries += 1

            print(text)

        result.append({"id": _id, "encryptionCount": tries, "originalText": sentence})

    logging.info("My result :{}".format(result))
    return jsonify(result)

