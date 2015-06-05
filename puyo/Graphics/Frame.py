import pygame

class Frame(object):
    '''basic rectangle with border to draw'''
    BORDER_SIZE = 5

    def __init__(self, windown, start_pos, \
            size, colors):
        #main windown
        self.display_surf = windown
        #starting point of gameboard + border
        self.frame_pos = start_pos
        #gameboard + border size in pixels
        self.frame_size = size
        #set colors
        self.border_color = colors[0]
        self.frame_color = colors[1]
        #starting point of gameboard
        self.board_pos = (self.frame_pos[0]+self.BORDER_SIZE, \
            self.frame_pos[1]+self.BORDER_SIZE)
        #gameboard size in pixels
        self.board_size = (self.frame_size[0]-2*self.BORDER_SIZE, \
            self.frame_size[1]-2*self.BORDER_SIZE)

    def draw(self):
        self.draw_border()
        self.draw_board()

    def draw_border(self):
        pygame.draw.rect(self.display_surf, self.border_color, \
            self.frame_pos+self.frame_size)

    def draw_board(self):
        pygame.draw.rect(self.display_surf, self.frame_color, \
            self.board_pos+self.board_size)
