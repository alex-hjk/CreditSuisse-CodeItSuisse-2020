import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

from queue import Queue

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluate():
    req = request.get_json()
    res = {
        "answers": {}
    }
    testCases = req["tests"]
    for test in testCases:
        res["answers"][test] = numSteps(test["maze"],test["start"],test["end"])
    
    return json.dumps(res)


def numSteps(maze, start, end):
    q = Queue()
    q.put([start,1])
    while q.empty()==False:
        curr = q.get()
        maze[curr[0][0]][curr[0][1]]==1
        if curr[0]==end:
            return curr[1]
        if curr[0][0]>0 and maze[curr[0][1]][curr[0][0]-1]!=1:
            q.put([[curr[0][0]-1,curr[0][1]],curr[1]+1])
        if curr[0][0]<len(maze[0])-1 and maze[curr[0][1]][curr[0][0]+1]!=1:
            q.put([[curr[0][0]+1,curr[0][1]],curr[1]+1])
        if curr[0][1]>0 and maze[curr[0][1]-1][curr[0][0]]!=1:
            q.put([[curr[0][0],curr[0][1]-1],curr[1]+1])
        if curr[0][1]<len(maze)-1 and maze[curr[0][1]+1][curr[0][0]]!=1:
            q.put([[curr[0][0],curr[0][1]+1],curr[1]+1]) 
    return -1