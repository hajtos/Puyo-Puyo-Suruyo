from .frame import Frame
from .colors import COLORS as Colors
import pygame

class BoardFrame(Frame):
    '''holder of one player game board'''
    #----table HEIGHTxWIDTH
    BORDER_COLOR = Colors.GREEN
    BOARD_COLOR = Colors.BLACK
    COLORS = [Colors.WHITE, Colors.LIGHTGREEN, \
        Colors.BLUE, Colors.YELLOW, Colors.ORANGE, Colors.RED]

    def __init__(self, windown, start, window_height, window_width):
        self.cell_height = 0
        self.cell_width = 0
        self.border_size = 0
        Frame.__init__(self, windown, start, \
            (window_height, window_width), \
            (self.BORDER_COLOR, self.BOARD_COLOR))

    def set_size(self, size):
        self.cell_height = self.board_size[0]/size[1]
        self.cell_width = self.board_size[1]/size[0]
        return self

    def set_border(self, size, color):
        self.border_size = size
        BoardFrame.BORDER_COLOR = color
        return self

    def draw_map(self, game_map):
        Frame.draw(self)
        for i, row in enumerate(game_map):
            for j, color in enumerate(row):
                if color is not None:
                    self.draw_element(color, i, j)

    def draw_element(self, color, ypos, xpos):
        '''draw one element on board'''
        pygame.draw.ellipse(
            self.display_surf,
            self.COLORS[color],
            (self.board_pos[0]+xpos*self.cell_height, \
                self.board_pos[1]+ypos*self.cell_width, \
                self.cell_height, self.cell_width),
            0)
