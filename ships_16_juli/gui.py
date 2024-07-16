import math
import pygame as pg
from ship import Ship
from game import Game
from typing import Dict
import constants

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
white = (255, 255, 255)

colors = [green, red, blue, purple, cyan]

shipEyeLength = 5

class Graphics:
    def __init__(self, width = 1000, height = 1000, fps = 60):
        self.fps = fps

        pg.init()
        self.screen = pg.display.set_mode([width, height])
        self.clock = pg.time.Clock()

    def render(self, game: Game):
        ships = game.ships.values()
        powerups = game.powerups
        self.screen.fill((0, 0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        for ship in ships:
            # main body
            pg.draw.circle(
                    self.screen, 
                    colors[ship.teamId % len(colors)], 
                    (ship.posx, ship.posy), 
                    constants.SHIP_RADIUS)
            # eye
            pg.draw.line(
                    self.screen, 
                    colors[
                    ship.teamId % len(colors)], 
                    (ship.posx, ship.posy), 
                    (ship.posx + math.cos(ship.direction) * (constants.SHIP_RADIUS + shipEyeLength), ship.posy + math.sin(ship.direction) * (constants.SHIP_RADIUS + shipEyeLength)), 
                    4)

            if ship.isShooting:
                # shooting line
                pg.draw.line(
                        self.screen, 
                        white, 
                        (ship.posx, ship.posy), 
                        (ship.posx + math.cos(ship.direction) * constants.SHOT_LENGTH, ship.posy + math.sin(ship.direction) * constants.SHOT_LENGTH), 
                        4)

            # energy bar
            pg.draw.line(
                    self.screen, 
                    white, 
                    (ship.posx - constants.SHIP_RADIUS, ship.posy - constants.SHIP_RADIUS * 1.5), 
                    (ship.posx + constants.SHIP_RADIUS * (-1 + 2 * ship.energy / constants.MAX_ENERGY), ship.posy - constants.SHIP_RADIUS * 1.5))

        for powerup in powerups:
            pg.draw.circle(
                    self.screen,
                    cyan if powerup.timeTillActive <= 0 else (48, 48, 48),
                    (powerup.posx, powerup.posy),
                    powerup.radius if powerup.timeTillActive <= 0 else powerup.radius * (1 - powerup.timeTillActive / powerup.rechargeTime)

            )

        # Draw the score:
        font_size = 36
        font = pg.font.Font(None, font_size)  # None uses the default font

        text = f"{game.score_1} - {game.score_2}"
        text_surface = font.render(text, True, white)

        # Get the text rectangle
        text_rect = text_surface.get_rect()
        text_rect.center = (constants.BOARD_WIDTH // 2, 25)
        self.screen.blit(text_surface, text_rect)


        pg.display.flip()
        self.clock.tick(self.fps)
