import logging

import pygame
from pygame.locals import *

from boring import utils
from config import *
from boring.fonts import get_font

logger = logging.getLogger(__name__)
defaul_font = get_font("basic.ttf", 30)
font_monologue = get_font("animeace2_bld.ttf", 30)
font_monologue_whisper = get_font("animeace2_ital.ttf", 30)

from boring import images

debug = True


class TextBox:
    def __init__(self, text, font=defaul_font, text_color=(255, 255, 255), size=(WIDTH, HEIGHT)):
        self.text = text
        self.font = font
        self.color = text_color
        self.width, self.height = size

        self.surface = pygame.Surface(size)

    def render(self):
        """
        Force fit in width, tries to fit in height.
        """
        current_width = 0
        current_height = 0

        words = self.text.split(" ")
        for word in words:
            if word == "\n":
                current_width = 0
                current_height += self.font.get_height()
                continue
            word_surface = self.font.render(word, True, self.color)
            word_width, word_height = word_surface.get_size()
            if current_width + word_width > self.width:
                current_width = 0
                current_height += word_height
            self.surface.blit(word_surface, (current_width, current_height))
            current_width += word_width


class MultiTextBox:
    def __init__(self, text,
                 font=defaul_font,
                 text_color=Color("white"),
                 position=None,
                 size=(WIDTH, HEIGHT)):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.width, self.height = size
        self.position = position

        self.rect = pygame.Rect(position, size)

        self.surfaces = []
        self.texts_heights = []
        self.current_index = 0

        self.render_smart()
        self.requires_render = False

    def render_smart(self):
        """
        Force fit in width, fits in height too and cuts the text if it doesn't fit.
        Also does not cut sentences.
        """
        max_width, max_height = self.width, self.height
        words_of_text = self.text.split(" ")
        current_width = current_height = word_height = 0
        current_surface = pygame.Surface((max_width, max_height), SRCALPHA)
        words = []
        cursor = 0

        while cursor < len(words_of_text):
            word = words_of_text[cursor]
            if not word:
                logger.warning("Empty word in text: %s at index %s", self.text, cursor)
                cursor += 1
                continue
            if word[0] == "\n" and current_height != 0:
                current_width = 0
                current_height += self.font.get_height()
                word = word[1:]
            # remove \n from the word
            word = word.replace("\n", "")

            word_surface = self.font.render(word + " ", True, self.text_color)  # Fake render to get the size
            word_width, word_height = word_surface.get_size()

            if current_width + word_width > max_width:
                current_width = 0
                current_height += word_height

            if current_height + word_height > max_height:
                full_sentence, reste = cut_unfinished_sentence(words)
                self.texts_heights.append(max(full_sentence, key=lambda x: x[1][1])[1][1] + word_height)
                self._render_words(full_sentence, current_surface)
                self.surfaces.append(current_surface)
                current_surface = pygame.Surface((max_width, max_height), SRCALPHA)
                current_width = 0
                current_height = 0
                cursor -= len(reste)
                words = []
                continue

            words.append((word, (current_width, current_height)))
            current_width += word_width
            cursor += 1
        self.texts_heights.append(current_height + word_height)
        self._render_words(words, current_surface)
        self.surfaces.append(current_surface)

    def _render_words(self, words, surface):
        """Render the words on the surface."""
        for word, (x, y) in words:
            word_surface = utils.render_glow(word + " ", self.font, Color("white"), Color("black"), opx=2)
            surface.blit(word_surface, (x, y))

    def draw(self, win):
        """Draw the current surface."""
        if self.requires_render:
            self.render_smart()
            self.requires_render = False

        if debug:
            pygame.draw.rect(win, Color("red"), self.rect, 1)
        win.blit(self.surfaces[self.current_index], self.rect.topleft)

    def get_current_text_height(self):
        return self.texts_heights[self.current_index]

    def is_finished(self):
        return self.current_index == (len(self.surfaces) - 1)

    def next(self):
        if self.current_index < len(self.surfaces) - 1:
            self.current_index += 1
        else:
            logger.warning("Tried to go to next text box but there is no next text box.")


MONOLOGUE_COUNTOUR_POS = (150, 500)
MONOLOGUE_CIRCLE_CENTER = (377, 880)


class Logue:
    def __init__(self, border_radius=15, font=defaul_font, current_scene=None):
        self.border_radius = border_radius
        self.font = font

        x, y = (587, 769)
        x1, y1 = (1778, 956)

        w, h = (x1 - x, y1 - y)
        self.current_scene = current_scene
        self._init_rects((x, y), w, h)

    def _init_rects(self, pos, width: int, height: int):
        """Initialize the rectangles for the text display."""
        self.countour_rect = pygame.Rect(*pos, width, height)
        self.text_rect = self.countour_rect.inflate(-20, -20)

    def _draw_background(self, screen):
        """Draws the background for the monologue."""
        # Draw character head in the circle
        screen.blit(images.text_contour, MONOLOGUE_COUNTOUR_POS)
        # Draw the circle
        screen.blit(images.mc, images.mc.get_rect(center=MONOLOGUE_CIRCLE_CENTER).move(0, -40))


def cut_unfinished_sentence(words, punctuation=(".", "!", "?", ";", "…")):
    """Cut the last word if it is not finished."""
    # find index of the last punctuation
    last_punctuation_index = -1
    for i, (word, _) in enumerate(words):
        if word and word[-1] in punctuation:
            last_punctuation_index = i
    if last_punctuation_index == -1:
        return words, []
    else:
        return words[:last_punctuation_index + 1], words[last_punctuation_index + 1:]
