from Frame import Frame
from Colors import Colors
from TextFrame import TextFrame
import pygame, sys, random
from pygame.locals import *

class ScoreBoardFrame(Frame):
    '''display and hold player name and score'''
    BORDER_COLOR = Colors.WHITE
    BOARD_COLOR = Colors.BLACK
    TEXT_COLOR = Colors.WHITE
    TEXT_MARGIN = 5
    BASICFONT_SIZE = 20
    
    def __init__(self, player_name, window, start_x, start_y, height, width):
        '''initialize scoreboard values'''
        Frame.__init__(self, window, start_x, start_y, height, width, self.BORDER_COLOR, self.BOARD_COLOR)
        
        self.textFont = TextFrame(self.BASICFONT_SIZE)
        self.DISPLAYSURF = window
        self.PLAYER_NAME = player_name
        self.SCORE = 0
        
        self.NAME_SURF, self.NAME_RECT = self.textFont.makeText(
            self.PLAYER_NAME,
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            start_x+Frame.BORDER_SIZE+self.TEXT_MARGIN,
            start_y+Frame.BORDER_SIZE+self.TEXT_MARGIN)
        
        self.SCORE_SURF, self.SCORE_RECT = self.textFont.makeText(
            str(self.SCORE),
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            start_x+Frame.BORDER_SIZE+self.TEXT_MARGIN,
            start_y+Frame.BORDER_SIZE+height/2 - self.textFont.BASICFONT_SIZE + self.TEXT_MARGIN)
        
    def setFont(self, name):
        '''
        set font by name,
        name must be from system name font
        '''
        self.BASICFONT_NAME = name
        self.textFont = TextFrame(self.BASICFONT_NAME, self.BASICFONT_SIZE)
        return self
        
    def draw(self):
        '''draw frame and data in it (name, score)'''
        Frame.draw(self)
        self.drawName()
        self.drawScore()
    
    def drawName(self):
        '''draw player name'''
        self.DISPLAYSURF.blit(self.NAME_SURF, self.NAME_RECT)
    
    def drawScore(self):
        '''draw player score'''
        self.DISPLAYSURF.blit(self.SCORE_SURF, self.SCORE_RECT)

    def setScore(self, score):
        '''set player score'''
        self.SCORE = score
        self.SCORE_SURF, self.SCORE_RECT = self.textFont.makeText(
            str(self.SCORE),
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            self.FRAME_X+self.BORDER_SIZE+self.TEXT_MARGIN,
            self.FRAME_Y+self.BORDER_SIZE+self.FRAME_HEIGHT/2-self.textFont.BASICFONT_SIZE+self.TEXT_MARGIN)

    def addScore(self, points):
        '''add points to player score'''
        self.SCORE += points
        self.SCORE_SURF, self.SCORE_RECT = self.textFont.makeText(
            str(self.SCORE),
            self.TEXT_COLOR,
            self.BOARD_COLOR,
            self.FRAME_X+self.BORDER_SIZE+self.TEXT_MARGIN,
            self.FRAME_Y+self.BORDER_SIZE+self.FRAME_HEIGHT/2-self.textFont.BASICFONT_SIZE+self.TEXT_MARGIN)