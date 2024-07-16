from ship import Ship, ShipMoveInstruction
from powerup import Powerup
from typing import List as list, Tuple as tuple, Dict as dict


class Player:
    def __init__(self, teamId: int, map_number: int):
        self.thisTeamId = teamId
        self.map_number = map_number

    def update(self, ships: list[Ship], powerups: list[Powerup]) -> list[ShipMoveInstruction]:
        """
        @param List of all the ships that are alive (see ship.py).
        @param List of all the powerups that will regenerate (see powerup.py).
        @return A list of actions that you want to do this frame.
        """
        return []
