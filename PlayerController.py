from pygame.locals import *

class PlayerController(object):
    '''holder of player key controlls'''
    def __init__(self, LEFT, RIGHT, ROTATE_LEFT, ROTATE_RIGHT, SPEED):
        self.LEFT = LEFT
        self.RIGHT = RIGHT
        self.ROTATE_LEFT = ROTATE_LEFT
        self.ROTATE_RIGHT = ROTATE_RIGHT
        self.SPEED = SPEED