from Frame import Frame
from Colors import Colors
from TextFrame import TextFrame
import pygame, sys, random
from pygame.locals import *
 
class BoardFrame(Frame):
    '''holder of one player game board'''
    #----table HEIGHTxWIDTH
    BORDER_COLOR = Colors.GREEN
    BOARD_COLOR = Colors.BLACK
    COLORS = [Colors.WHITE, Colors.PURPLE, Colors.BLUE, Colors.YELLOW, Colors.ORANGE, Colors.RED]
    
    def __init__(self, windown, start_x, start_y, window_height, window_width):
        Frame.__init__(self, windown, start_x, start_y, window_height, window_width, self.BORDER_COLOR, self.BOARD_COLOR)
    
    def setSize(self, size):
        self.size = size
        self.cell_height = self.BOARD_HEIGHT/size[1]
        self.cell_width = self.BOARD_WIDTH/size[0]
        return self
    
    def setBorder(self, size, color):
        self.BORDER_SIZE = size
        self.BORDER_COLOR = color
        return self
    
    def draw(self, gameMap):
        Frame.draw(self)
        for i, row in enumerate(gameMap):
            for j, color in enumerate(row):
                if color is not None:
                    self.drawElement(color, i, j)
    
    def drawElement(self, color, y, x):
        '''draw one element on board'''
        pygame.draw.ellipse(
            self.DISPLAYSURF,
            self.COLORS[color],
            (self.BOARD_X+x*self.cell_height, self.BOARD_Y+y*self.cell_width, self.cell_height, self.cell_width),
            0)
