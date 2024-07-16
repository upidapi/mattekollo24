from ship import Ship, ShipMoveInstruction
from powerup import Powerup
from typing import List as list, Tuple as tuple, Dict as dict


class Player:
    def __init__(self, teamId: int, map_number: int):
        self.thisTeamId = teamId
        self.map_number = map_number
        self.frames_since_start = 0

    def update(self, ships: list[Ship], powerups: list[Powerup]) -> list[ShipMoveInstruction]:
        """
        @param List of all the ships that are alive (see ship.py).
        @param List of all the powerups that will regenerate (see powerup.py).
        @return A list of actions that you want to do this frame.
        """
        self.frames_since_start += 1
        moves = []
        for ship in ships:
            if ship.energy < 500:
                continue
            if ship.teamId == self.thisTeamId:
                moves.append(ShipMoveInstruction(ship.shipId, self.frames_since_start % 2 == 0, False, ship.speed < 2, False, self.frames_since_start % 10 == 0))

        return moves
