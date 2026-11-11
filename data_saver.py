import json
from settings import *

def save_score(data):
    print("save score")
    scoreboard = load_data(SCOREBOARD_ROUTE)
    scoreboard.append(data)
    save_data(scoreboard, SCOREBOARD_ROUTE)


def get_scoreboard():
    scoreboard = load_data(SCOREBOARD_ROUTE)
    scoreboard = sorted(scoreboard, key=lambda data: -data['score'])
    return scoreboard[:5]


def save_data(data, route):
    with open(route, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def load_data(route):
    with open(route, 'r') as file:
        return json.load(file)


def sort(data):
    return data.score