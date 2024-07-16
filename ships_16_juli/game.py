import math
import threading
import constants
from typing import Optional
from client import Player
import copy
from maps import generate_map
from ship import Ship, ShipMoveInstruction
from powerup import Powerup
# from typing import List as list, Tuple as tuple, Dict as dict


# Is a shooting b.
def is_hitting(a: Ship, b: Ship) -> bool:
    # Function to calculate the distance between a point (px, py) and a line segment (x1, y1) - (x2, y2)
    px, py, x1, y1 = b.posx, b.posy, a.posx, a.posy
    x2 = a.posx + constants.SHOT_LENGTH * math.cos(a.direction)
    y2 = a.posy + constants.SHOT_LENGTH * math.sin(a.direction)
    # Vector from point 1 to point 2
    dx = x2 - x1
    dy = y2 - y1
    
    # Handle the case where the segment is a point
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    
    # Calculate the projection of the point onto the line segment
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    
    # Clamp t to the range [0, 1] to ensure the projection is on the segment
    t = max(0, min(1, t))
    
    # Find the closest point on the segment to the point (px, py)
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    
    # Calculate the distance from the point to the closest point on the segment
    distance = math.hypot(px - closest_x, py - closest_y)
    
    return distance < constants.SHIP_RADIUS

class Game:
    def __init__(self, player_1: Player, player_2: Player, map_number: int = 1, frames_per_match: int = 800) -> None:
        self.player_1: Player = player_1
        self.player_2: Player = player_2
        temp = generate_map(map_number)
        self.ships: dict[int, Ship] = temp[0]
        self.powerups: list[Powerup] = temp[1]

        self.score_1 = 0
        self.score_2 = 0

        self.frames_left = frames_per_match

    def get_player_actions(self, player: Player, ret_value: list) -> None:
        try:
            ships = copy.deepcopy(list(self.ships.values()))
            powerups = copy.deepcopy(self.powerups)
            ret_value.append(player.update(ships, powerups))
        except Exception as e:
            print(e)

    def is_ok_actions(self, player_id: int, actions) -> bool:
        
        for action in actions:
            # muse be an actuall ship
            if action.shipId not in self.ships:
                return False
            # all in your team
            if self.ships[action.shipId].teamId != player_id:
                return False
            # only bools
            for var in [action.rotateLeft, action.rotateRight, action.accelerateForwards, action.accelerateBackwards, action.shoot]:
                if not isinstance(var, bool):
                    return False
        return True

    def is_running(self) -> bool:
        return self.frames_left > 0

    def update(self) -> None:
        self.frames_left -= 1
        ret_value_1 = []
        ret_value_2 = []
        thread_1 = threading.Thread(target=self.get_player_actions, args=(self.player_1, ret_value_1,))
        thread_2 = threading.Thread(target=self.get_player_actions, args=(self.player_2, ret_value_2,))
        thread_1.start()
        thread_2.start()

        thread_1.join()
        thread_2.join()
        # thread_1.join(timeout=100)
        # thread_2.join(timeout=100)
        # thread_1.join(timeout=0.1)
        # thread_2.join(timeout=0.1)

        actions: list[ShipMoveInstruction] = []
        
        if self.is_ok_actions(1, ret_value_1[0]):
            actions += ret_value_1[0]
        else:
            print("Player 1 is trying to mess up the system")
        if self.is_ok_actions(2, ret_value_2[0]):
            actions += ret_value_2[0]
        else:
            print("Player 2 is trying to mess up the system")

        for sh in self.ships.values():
            sh.isShooting = False
        

        # Update ships with user actions.
        to_delete = set()
        for action in actions:
            sh = self.ships[action.shipId]
            # do actions
            if action.rotateLeft:
                sh.direction -= constants.ROTATION_SPEED
                sh.energy -= constants.ENERGY_ROTATION
            if action.rotateRight:
                sh.direction += constants.ROTATION_SPEED
                sh.energy -= constants.ENERGY_ROTATION
            if action.accelerateForwards:
                sh.speed += constants.ACCELERATION
                sh.energy -= constants.ENERGY_ACCELERATION
            if action.accelerateBackwards:
                sh.speed -= constants.ACCELERATION
                sh.energy -= constants.ENERGY_ACCELERATION
            if action.shoot:
                sh.isShooting = True
                sh.energy -= constants.ENERGY_SHOOT
            else:
                sh.isShooting = False
            if sh.energy <= 0:
                to_delete.add(action.shipId)

        # Move ships, crop to screen.
        for sh in self.ships.values():
            # cant go backwards
            sh.speed = max(0, sh.speed)
            sh.speed = min(sh.speed, constants.MAX_SPEED)

            sh.posx += sh.speed * math.cos(sh.direction)
            sh.posy += sh.speed * math.sin(sh.direction)

            sh.posx = max(0, sh.posx)
            sh.posx = min(sh.posx, constants.BOARD_WIDTH)
            sh.posy = max(0, sh.posy)
            sh.posy = min(sh.posy, constants.BOARD_HEIGHT)

        # Regen some health.
        for sh in self.ships.values():
            sh.energy = min(sh.energy + constants.ENERGY_REGEN, constants.MAX_ENERGY)

        # Check damage
        for a in self.ships.values():
            if not a.isShooting:
                continue
            for b in self.ships.values():
                if a.teamId == b.teamId:
                    continue
                if is_hitting(a, b):
                    b.energy -= constants.SHOT_DAMAGE
                    if b.energy <= 0:
                        to_delete.add(b.shipId)

        # Update all powerups and give points to each ship that collected it.        
        for powerup in self.powerups:
            if powerup.timeTillActive != 0:
                powerup.timeTillActive -= 1
                continue
            for sh in self.ships.values():
                dx = sh.posx - powerup.posx
                dy = sh.posy - powerup.posy
                dist_squared = dx ** 2 + dy ** 2
                if dist_squared <= powerup.radius ** 2:
                    if sh.teamId == 1:
                        self.score_1 += constants.SCORE_POWERUP
                    else:
                        self.score_2 += constants.SCORE_POWERUP
                    powerup.timeTillActive = powerup.rechargeTime

        for id in to_delete:
            if self.ships[id].teamId == 1:
                self.score_2 += 1
            else:
                self.score_1 += 1
            del self.ships[id]

                

    def winner(self) -> bool:
        if self.score_1 > self.score_2:
            return 1
        if self.score_1 < self.score_2:
            return 2
        return 0
