from Frame import Frame
import pygame, sys, random
from pygame.locals import *

class TextFrame(object):
    BASICFONT_NAME = 'comicsansms'
    
    def __init__(self, size):
        pygame.init()
        self.BASICFONT_SIZE = size
        self.BASICFONT = pygame.font.SysFont(self.BASICFONT_NAME, self.BASICFONT_SIZE)
    
    def makeText(self, text, color, bgcolor, top, left):
        '''create the Surface and Rect objects for text.'''
        textSurf = self.BASICFONT.render(text, True, color, bgcolor)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)