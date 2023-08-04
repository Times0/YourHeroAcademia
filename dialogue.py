import logging

import pygame
from pygame.locals import *

from boring import images
from boring.config import WIDTH, HEIGHT
from boring.fonts import get_font

logger = logging.getLogger(__name__)

defaul_font = get_font("animeace.ttf", 30)


def cut_unfinished_sentence(words, punctuation=(".", "!", "?", ";", "…", "\n")):
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


class Monologue:
    """
    A class representing a monologue in pygame.
    The text is broken up into chunks which fit within a specified area.
    These chunks can be navigated through using the space bar.
    """

    def __init__(self, text: str, character: dict = None, scene=None):
        from scene import Character
        self.scene = scene

        if character is not None:
            self.character = Character(**character, position=(WIDTH / 2, HEIGHT / 2))

        self.whole_text = text
        self.border_radius = 15
        self.rect_alpha = 200
        self.font = defaul_font

        x, y = (587, 769)
        x1, y1 = (1778, 956)

        w, h = (x1 - x, y1 - y)

        self._init_rects((x, y), w, h, 50)
        self._init_text()
        self._render_all()

    def _init_rects(self, pos, width: int, height: int, offset: int):
        """Initialize the rectangles for the text display."""

        self.countour_rect = pygame.Rect(*pos, width, height)
        self.text_rect = self.countour_rect.inflate(-20, -20)

    def _init_text(self):
        """Initialize the text related attributes."""
        self.words_in_text = self.whole_text.split(" ")
        self.current_chunk = 0
        self.surfaces = []

    def _render_all(self):
        """Render all the chunks of the text."""
        self.surfaces = []
        self.nb_chunks = 0
        max_width, max_height = self.text_rect.size
        current_width = current_height = 0
        current_surface = pygame.Surface(self.text_rect.size, SRCALPHA)
        words = []  # tyype: List[Tuple[str,Tuple[int,int]]]
        cursor = 0
        while cursor < len(self.words_in_text):
            word = self.words_in_text[cursor]
            word_surface = self.font.render(word + " ", True, Color("Black"))  # Fake render to get the size
            word_width, word_height = word_surface.get_size()

            if current_width + word_width > max_width:
                current_width = 0
                current_height += word_height

            if current_height + word_height > max_height:
                cut_words, remaining = cut_unfinished_sentence(words)
                self._render_words(cut_words, current_surface)
                self._append_current_surface(current_surface)
                current_surface = pygame.Surface(self.text_rect.size, SRCALPHA)
                current_width = 0
                current_height = 0
                cursor -= len(remaining)
                words = []
                continue

            words.append((word, (current_width, current_height)))
            current_width += word_width
            cursor += 1

        self._render_words(words, current_surface)
        self._append_current_surface(current_surface)
        logger.info(f"Monologue has been rendered in {self.nb_chunks} chunks.")

    def _render_words(self, words, surface):
        """Render the words on the surface."""
        for word, (x, y) in words:
            word_surface = self.font.render(word + " ", True, Color("Black"))
            surface.blit(word_surface, (x, y))

    def _append_current_surface(self, surface):
        """Appends the current surface to the list of surfaces and increment the number of chunks."""
        self.surfaces.append(surface)
        self.nb_chunks += 1

    def handle_events(self, events):
        """Handles the events for the monologue."""
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._handle_space_key()

    def _handle_space_key(self):
        """Handle the space key event."""
        self.current_chunk += 1
        if self.current_chunk >= self.nb_chunks:
            self.scene.next_event()

    def draw(self, screen):
        """Draws the current chunk of the monologue on the screen."""
        self._draw_character(screen)
        self._draw_background(screen)
        self._draw_text(screen)
        self._draw_chunk_number(screen)

    def _draw_character(self, screen):
        """Draws the character on the screen."""
        if self.character is not None:
            self.character.draw(screen)

    def _draw_background(self, screen):
        """Draws the background for the monologue."""
        # pygame.draw.rect(screen, Color("Black"), self.countour_rect, 0, border_radius=self.border_radius)
        # pygame.draw.rect(screen, Color("White"), self.text_rect, 1)
        screen.blit(images.text_contour, (150, 500))

    def _draw_text(self, screen):
        """Draws the text of the current chunk."""
        screen.blit(self.surfaces[self.current_chunk], self.text_rect)

    def _draw_chunk_number(self, screen):
        """Draws the number of the current chunk on the screen."""
        chunk_text = f"{self.current_chunk + 1}/{self.nb_chunks}"
        chunk_surface = self.font.render(chunk_text, True, Color("Black"))
        screen.blit(chunk_surface, chunk_surface.get_rect(bottomright=self.countour_rect.bottomright).move(-10, -10))


class Dialogue:
    pass
