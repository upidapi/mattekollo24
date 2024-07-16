
from  pprint import pprint
from ship import Ship, ShipMoveInstruction
from powerup import Powerup


class Player:
    def __init__(self, teamId: int, map_number: int):
        self.thisTeamId = teamId
        self.map_number = map_number

    first_frame = True
    def update(self, ships, powerups):
        """
        @param List of all the ships that are alive (see ship.py).
        @param List of all the powerups that will regenerate (see powerup.py).
        @return A list of actions that you want to do this frame.
        """
        actions = []

        # speed upp to max (0.2 * 20 = 4)
        if Player.first_frame: 
            for ship in ships:
                if ship.teamId != self.thisTeamId:
                    continue
                
                for _ in range(20):
                    actions.append(ShipMoveInstruction(
                        shipId=ship.shipId,
                        accelerateForwards=True,
                    ))

        Player.first_frame = False

        
        """
        try: 
            pprint(ships)
            pprint(powerups)
        except BaseException:
            print("fuck")
        """

        pprint(ships)
        pprint(powerups)
        pprint(actions)
        print()
        print()

        return actions
    
# token 410990
    
