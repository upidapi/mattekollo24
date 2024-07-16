from ship import Ship
from powerup import Powerup
import constants
import math
import random

current_index: int = 0
def get_new_ship_id() -> int:
    global current_index
    current_index += 1
    return current_index

def map_1():
    ships = []
    for y in range(100, constants.BOARD_WIDTH, 100):
        ships.append(Ship(700, y + random.random() * 10 - 5, 0, 0, constants.MAX_ENERGY, 1, get_new_ship_id(), 0))
        ships.append(Ship(constants.BOARD_WIDTH - 700, y, math.pi, 0, constants.MAX_ENERGY, 2, get_new_ship_id(), 0))
    ships = {sh.shipId : sh for sh in ships}

    powerups = [Powerup(constants.BOARD_WIDTH / 2, 100, 30, 100, 150),
                Powerup(constants.BOARD_WIDTH / 2, constants.BOARD_HEIGHT / 2, 15, 50, 150),
                Powerup(constants.BOARD_WIDTH / 2, constants.BOARD_HEIGHT - 100, 30, 75, 150),
                ]

    return (ships, powerups)

def map_2():
    ships = []
    for i in range(50):
        x = random.random() * 150
        y = random.random() * 750
        x += 100
        y += 125
        ships.append(Ship(x, y, 0, -constants.MAX_SPEED, constants.MAX_ENERGY, 1, get_new_ship_id(), 0))

    for i in range(50):
        x = random.random() * 150
        y = random.random() * 750
        x += constants.BOARD_WIDTH - 200
        y += 125
        ships.append(Ship(x, y, math.pi, -constants.MAX_SPEED, constants.MAX_ENERGY, 2, get_new_ship_id(), 0))

    ships = {sh.shipId : sh for sh in ships}

    powerups = [Powerup(constants.BOARD_WIDTH / 2, 100, 10, 100, 150),
                Powerup(constants.BOARD_WIDTH / 2, constants.BOARD_HEIGHT / 2, 10, 50, 150),
                Powerup(constants.BOARD_WIDTH / 2, constants.BOARD_HEIGHT - 100, 10, 75, 150),
                ]

    return (ships, powerups)
    


def generate_map(map_id: int):
    map_functions = [None, map_1, map_2]
    return map_functions[map_id]()