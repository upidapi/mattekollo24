from dataclasses import dataclass

@dataclass
class Ship:
    posx: float
    posy: float
    direction: float # Between 0 and 2*pi
    speed: float
    energy: float
    teamId: int
    shipId: int
    isShooting: bool

@dataclass
class ShipMoveInstruction:
    shipId: int
    rotateLeft: bool = False
    rotateRight: bool = False
    accelerateForwards: bool = False
    accelerateBackwards: bool = False
    shoot: bool = False
