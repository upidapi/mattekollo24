from dataclasses import dataclass

@dataclass
class Powerup:
    posx: float
    posy: float
    radius: float # How close you need to be to collect the points.
    timeTillActive: int # Number of frames till becoming active.
    rechargeTime: int # Number of frames from being taken till being inactive.