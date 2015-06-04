import pygame

class Frame(object):
    '''basic rectangle with border to draw'''
    BORDER_SIZE = 5

    def __init__(self, windown, start_pos, \
            height, width, frame_color, board_color):
        #main windown
        self.display_surf = windown
        #starting point of gameboard + border
        self.frame_x = start_pos[0]
        self.frame_y = start_pos[1]
        #gameboard + border size in pixels
        self.frame_height = height
        self.frame_width = width
        #set colors
        self.border_color = frame_color
        self.frame_color = board_color
        #starting point of gameboard
        self.board_x = self.frame_x+self.BORDER_SIZE
        self.board_y = self.frame_y+self.BORDER_SIZE
        #gameboard size in pixels
        self.board_height = self.frame_height-2*self.BORDER_SIZE
        self.board_width = self.frame_width-2*self.BORDER_SIZE

    def draw(self):
        self.drawBorder()
        self.drawBoard()

    def drawBorder(self):
        pygame.draw.rect(self.display_surf, self.border_color, \
            [self.frame_x, self.frame_y, self.frame_height, self.frame_width])

    def drawBoard(self):
        pygame.draw.rect(self.display_surf, self.frame_color, \
            [self.board_x, self.board_y, self.board_height, self.board_width])
