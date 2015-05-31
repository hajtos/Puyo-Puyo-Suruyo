import pygame, sys, random
from pygame.locals import *

class Frame(object):
    '''basic rectangle with border to draw'''
    BORDER_SIZE = 5
    
    def __init__(self, windown, start_x, start_y, height, width, frame_color, board_color):
        #main windown
        self.DISPLAYSURF = windown
        #starting point of gameboard + border
        self.FRAME_X = start_x
        self.FRAME_Y = start_y
        #gameboard + border size in pixels
        self.FRAME_HEIGHT = height
        self.FRAME_WIDTH = width
        #set colors
        self.BORDER_COLOR = frame_color
        self.FRAME_COLOR = board_color
        #starting point of gameboard
        self.BOARD_X = self.FRAME_X+self.BORDER_SIZE
        self.BOARD_Y = self.FRAME_Y+self.BORDER_SIZE
        #gameboard size in pixels
        self.BOARD_HEIGHT = self.FRAME_HEIGHT-2*self.BORDER_SIZE
        self.BOARD_WIDTH = self.FRAME_WIDTH-2*self.BORDER_SIZE
    
    def draw(self):
        self.drawBorder()
        self.drawBoard()
    
    def drawBorder(self):
        pygame.draw.rect(self.DISPLAYSURF, self.BORDER_COLOR, [self.FRAME_X, self.FRAME_Y, self.FRAME_HEIGHT, self.FRAME_WIDTH])
        
    def drawBoard(self):
        pygame.draw.rect(self.DISPLAYSURF, self.BOARD_COLOR, [self.BOARD_X, self.BOARD_Y, self.BOARD_HEIGHT, self.BOARD_WIDTH])
