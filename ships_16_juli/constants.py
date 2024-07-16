import math

BOARD_WIDTH = 1000 # Pixels
BOARD_HEIGHT = 1000 # Pixels
ACCELERATION = 0.2 # Pixels / frame / frame
MAX_SPEED = 4 # Pixels per frame
MAX_ENERGY = 1000

# ew rotate 1 / 360 per action
ROTATION_SPEED = 2*math.pi / 120 # Radians per frame
SHOT_LENGTH = 100 # How far the shot reaches in pixels.
SHIP_RADIUS = 10 # Radius of ship in pixels.

SHOT_DAMAGE = 300 # How much damage you deal.

ENERGY_REGEN = 20 # How much energy you regain per frame.
ENERGY_SHOOT = 50 # How much it costs to shoot.

# 0.2 acceletation per 10 energy
# 200 energy from 0 => 4 (max speed)
ENERGY_ACCELERATION = 10 # Energy per frame you choose to accelerate.

# 10 radians rotation per action
ENERGY_ROTATION = 10 # Energy per frame you choose to rotate.

SCORE_POWERUP = 10 # How many points you get for collecting a powerup.