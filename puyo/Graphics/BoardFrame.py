from .Frame import Frame
from .Colors import COLORS as Colors
import pygame

class BoardFrame(Frame):
    '''holder of one player game board'''
    #----table HEIGHTxWIDTH
    BORDER_COLOR = Colors.GREEN
    BOARD_COLOR = Colors.BLACK
    COLORS = [Colors.WHITE, Colors.PURPLE, \
        Colors.BLUE, Colors.YELLOW, Colors.ORANGE, Colors.RED]

    def __init__(self, windown, start_x, \
            start_y, window_height, window_width):
        self.cell_height = 0
        self.cell_width = 0
        self.border_size = 0
        Frame.__init__(self, windown, (start_x, start_y), \
            window_height, window_width, self.BORDER_COLOR, self.BOARD_COLOR)

    def setSize(self, size):
        self.cell_height = self.board_height/size[1]
        self.cell_width = self.board_width/size[0]
        return self

    def setBorder(self, size, color):
        self.border_size = size
        BoardFrame.BORDER_COLOR = color
        return self

    def drawMap(self, game_map):
        Frame.draw(self)
        for i, row in enumerate(game_map):
            for j, color in enumerate(row):
                if color is not None:
                    self.drawElement(color, i, j)

    def drawElement(self, color, ypos, xpos):
        '''draw one element on board'''
        pygame.draw.ellipse(
            self.display_surf,
            self.COLORS[color],
            (self.board_x+xpos*self.cell_height, \
                self.board_y+ypos*self.cell_width, \
                self.cell_height, self.cell_width),
            0)
