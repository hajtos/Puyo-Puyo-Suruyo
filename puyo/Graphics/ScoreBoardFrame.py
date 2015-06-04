from .Frame import Frame
from .Colors import COLORS as Colors
from .TextFrame import TextFrame

class ScoreBoardFrame(Frame):
    '''display and hold player name and score'''
    BORDER_COLOR = Colors.WHITE
    BOARD_COLOR = Colors.BLACK
    TEXT_COLOR = Colors.WHITE
    TEXT_MARGIN = 5
    BASICFONT_SIZE = 20

    def __init__(self, player_name, window, start_x, start_y, height, width):
        '''initialize scoreboard values'''
        Frame.__init__(self, window, (start_x, start_y), \
            height, width, self.BORDER_COLOR, self.BOARD_COLOR)
        self.text_font = TextFrame(self.BASICFONT_SIZE)
        self.display_surf = window
        self.player_name = player_name
        self.score = 0
        self.name_surf, self.name_rect = self.text_font.makeText(
            self.player_name,
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            start_x+Frame.BORDER_SIZE+self.TEXT_MARGIN,
            start_y+Frame.BORDER_SIZE+self.TEXT_MARGIN)
        self.score_surf, self.score_rect = self.text_font.makeText(
            str(self.score),
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            start_x+Frame.BORDER_SIZE+self.TEXT_MARGIN,
            start_y+Frame.BORDER_SIZE+height/2-\
                self.text_font.basic_font_size+self.TEXT_MARGIN)

    def setFont(self, name):
        '''
        set font by name,
        name must be from system name font
        '''
        self.text_font.changeFont(name, self.BASICFONT_SIZE)
        return self

    def draw(self):
        '''draw frame and data in it (name, score)'''
        Frame.draw(self)
        self.drawName()
        self.drawScore()

    def drawName(self):
        '''draw player name'''
        self.display_surf.blit(self.name_surf, self.name_rect)

    def drawScore(self):
        '''draw player score'''
        self.display_surf.blit(self.score_surf, self.score_rect)

    def setScore(self, score):
        '''set player score'''
        self.score = score
        self.score_surf, self.score_rect = self.text_font.makeText(
            str(self.score),
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            self.frame_x+self.BORDER_SIZE+self.TEXT_MARGIN,
            self.frame_y+self.BORDER_SIZE+self.frame_height/2-\
                self.text_font.basic_font_size+self.TEXT_MARGIN)

    def addScore(self, points):
        '''add points to player score'''
        self.score += points
        self.score_surf, self.score_rect = self.text_font.makeText(
            str(self.score),
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            self.frame_x+self.BORDER_SIZE+self.TEXT_MARGIN,
            self.frame_y+self.BORDER_SIZE+self.frame_height/2-\
                self.text_font.basic_font_size+self.TEXT_MARGIN)
