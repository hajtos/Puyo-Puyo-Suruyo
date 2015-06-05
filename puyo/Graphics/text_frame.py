import pygame

class TextFrame(object):
    BASICFONT_NAME = 'comicsansms'

    def __init__(self, size):
        # pylint: disable=E1103
        pygame.init()
        # pylint: enable=E1103
        self.basic_font_size = size
        self.basic_font = pygame.font.SysFont(self.BASICFONT_NAME, \
            self.basic_font_size)

    def make_text(self, text, color, bgcolor, corner_pos):
        '''create the Surface and Rect objects for text.'''
        text_surf = self.basic_font.render(text, True, color, bgcolor)
        text_rect = text_surf.get_rect()
        text_rect.topleft = corner_pos
        return (text_surf, text_rect)

    def change_font(self, name, size):
        self.basic_font_size = size
        self.basic_font = pygame.font.SysFont(name, \
            self.basic_font_size)
