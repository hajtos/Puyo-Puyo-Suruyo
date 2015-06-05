from .frame import Frame
from .colors import COLORS as Colors
from .text_frame import TextFrame

class ScoreBoardFrame(Frame):
    '''display and hold player name and score'''
    BORDER_COLOR = Colors.WHITE
    BOARD_COLOR = Colors.BLACK
    TEXT_COLOR = Colors.WHITE
    TEXT_MARGIN = 5
    BASICFONT_SIZE = 20

    def __init__(self, player_name, window, start_pos, size):
        '''initialize scoreboard values'''
        Frame.__init__(self, window, start_pos, \
            size, (self.BORDER_COLOR, self.BOARD_COLOR))
        self.text_font = TextFrame(self.BASICFONT_SIZE)
        self.display_surf = window
        self.player_name = player_name
        self.score = 0
        self.name_field = self.text_font.make_text(self.player_name, \
            self.TEXT_COLOR, self.BOARD_COLOR, \
            (start_pos[0]+Frame.BORDER_SIZE+self.TEXT_MARGIN, \
                start_pos[1]+Frame.BORDER_SIZE+self.TEXT_MARGIN))
        self.score_field = self.text_font.make_text(str(self.score), \
            self.TEXT_COLOR, self.BOARD_COLOR, \
            (start_pos[0]+Frame.BORDER_SIZE+self.TEXT_MARGIN, \
                start_pos[1]+Frame.BORDER_SIZE+size[0]/2-\
                self.text_font.basic_font_size+self.TEXT_MARGIN))

    def set_font(self, name):
        '''
        set font by name,
        name must be from system name font
        '''
        self.text_font.change_font(name, self.BASICFONT_SIZE)
        return self

    def draw(self):
        '''draw frame and data in it (name, score)'''
        Frame.draw(self)
        self.draw_name()
        self.draw_score()

    def draw_name(self):
        '''draw player name'''
        self.display_surf.blit(self.name_field[0], self.name_field[1])

    def draw_score(self):
        '''draw player score'''
        self.display_surf.blit(self.score_field[0], self.score_field[1])

    def set_score(self, score):
        '''set player score'''
        self.score = score
        self.score_field = self.text_font.make_text(str(self.score), \
            self.TEXT_COLOR, self.BOARD_COLOR, \
            (self.frame_pos[0]+self.BORDER_SIZE+self.TEXT_MARGIN, \
                self.frame_pos[1]+self.BORDER_SIZE+self.frame_size[0]/2-\
                self.text_font.basic_font_size+self.TEXT_MARGIN))

    def add_score(self, points):
        '''add points to player score'''
        self.score += points
        self.score_field = self.text_font.make_text(str(self.score), \
            self.TEXT_COLOR, self.BOARD_COLOR, \
            (self.frame_pos[0]+self.BORDER_SIZE+self.TEXT_MARGIN, \
                self.frame_pos[1]+self.BORDER_SIZE+self.frame_size[0]/2-\
                self.text_font.basic_font_size+self.TEXT_MARGIN))
