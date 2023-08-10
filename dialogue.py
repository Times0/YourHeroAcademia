import logging

import pygame
from pygame.locals import *

from boring import images
from boring.config import WIDTH, HEIGHT
from boring.fonts import get_font

from scene import Character

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
                 size=(WIDTH, HEIGHT), ):
        self.text = text
        self.font = font
        self.text_color = text_color
        self.width, self.height = size

        self.surfaces = []
        self.current_index = 0

        self.requires_render = True

    def render_smart(self):
        """
        Force fit in width, fits in height too and cuts the text if it doesn't fit.
        Also does not cut sentences.
        """
        max_width, max_height = self.width, self.height
        words_of_text = self.text.split(" ")
        current_width = current_height = 0
        current_surface = pygame.Surface((max_width, max_height), SRCALPHA)
        words = []
        cursor = 0
        while cursor < len(words_of_text):
            word = words_of_text[cursor]
            word_surface = self.font.render(word + " ", True, self.text_color)  # Fake render to get the size
            word_width, word_height = word_surface.get_size()

            if current_width + word_width > max_width:
                current_width = 0
                current_height += word_height

            if current_height + word_height > max_height:
                full_sentence, reste = cut_unfinished_sentence(words)
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

        self._render_words(words, current_surface)
        self.surfaces.append(current_surface)

    def _render_words(self, words, surface):
        """Render the words on the surface."""
        for word, (x, y) in words:
            word_surface = self.font.render(word + " ", True, Color("Black"))
            surface.blit(word_surface, (x, y))

    def draw(self, win, pos=(0, 0)):
        """Draw the current surface."""
        if self.requires_render:
            self.render_smart()
            self.requires_render = False
        if debug:
            pygame.draw.rect(win, Color("red"), (pos[0], pos[1], self.width, self.height), 1)
        win.blit(self.surfaces[self.current_index], (pos[0] + 5, pos[1] + 5))


class Logue:
    def __init__(self, border_radius=15, rect_alpha=200, font=defaul_font, current_scene=None):
        self.border_radius = border_radius
        self.rect_alpha = rect_alpha
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
        screen.blit(images.text_contour, (150, 500))


monologue_rect = pygame.Rect(606, 788, 1166, 168)

page_counter_rect = pygame.Rect(1624, 672, 100, 100)


class Monologue(Logue):
    """
    A class representing a monologue in pygame.
    The text is broken up into chunks which fit within a specified area.
    These chunks can be navigated through using the space bar.
    """

    def __init__(self, text: str, character: dict = None, current_scene=None):
        super().__init__(border_radius=15, rect_alpha=200, font=defaul_font, current_scene=current_scene)

        from scene import Character
        if character is not None:  # If we want to display a character
            self.character = Character(**character, position=(WIDTH / 2, HEIGHT / 2))

        self.text_box = MultiTextBox(text, font=defaul_font, size=monologue_rect.size)

    def handle_events(self, events):
        """Handles the events for the monologue."""
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._handle_space_key()

    def _handle_space_key(self):
        """Handle the space key event."""
        self.text_box.current_index += 1
        if self.text_box.current_index >= len(self.text_box.surfaces):
            self.current_scene.next_event()

    def draw(self, screen):
        """Draws the monologue on the screen."""
        if hasattr(self, "character"):
            self.character.draw(screen)
        self._draw_background(screen)
        self.text_box.draw(screen, monologue_rect.topleft)
        self._draw_page_counter(screen)

    def _draw_page_counter(self, screen):
        """Draws the page counter on the screen."""
        page_counter = self.font.render(
            f"{self.text_box.current_index + 1}/{len(self.text_box.surfaces)}", True, Color("Black")
        )
        screen.blit(page_counter, page_counter_rect.topleft)


class LineOther:
    """
    Type for a piece of dialogue that the other character says.
    text is the text that the character says.
    answers is a list of answers that the player can choose from. Each answer contains the suite of the dialogue
    """

    def __init__(self, text, answers: dict):
        self.text = text
        if answers is not None:
            self.answers: list[LinePlayer] = [LinePlayer(**answer) for answer in answers]
        else:
            self.answers = None


class LinePlayer:
    """
    Type for a piece of dialogue that the player says.
    text is the text that the player says.
    line is the next line of dialogue that the other character says.
    """

    def __init__(self, text: str, line: dict):
        self.text: str = text
        if line is not None:
            self.line: LineOther = LineOther(**line)
        else:
            self.line = None


class Clickable:
    def __init__(self, onclick_f):
        self.is_hover = False
        self.clicked = False
        self.onclick_f = onclick_f

        self.rect = pygame.rect.Rect(0, 0, 0, 0)

    def is_mouse_on_button(self, pos):
        return self.rect.collidepoint(pos)

    @staticmethod
    def on_hover():
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

    @staticmethod
    def on_unhover():
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouse_on_button(event.pos):
                    self.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                if self.clicked and self.is_mouse_on_button(event.pos):
                    self._on_click()
                self.clicked = False

            if event.type == pygame.MOUSEMOTION:
                was_hover = self.is_hover
                self.is_hover = self.is_mouse_on_button(event.pos)
                if self.is_hover and not was_hover:
                    self.on_hover()
                elif not self.is_hover and was_hover:
                    self.on_unhover()

    def _on_click(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if self.onclick_f is not None:
            self.onclick_f()


class AnswerUI(Clickable):
    def __init__(self, text: str):
        super().__init__(None)
        self.text = text
        self.font = defaul_font

    def draw(self, screen, pos):
        self.rect = pygame.Rect(pos, (500, 100))
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        surface.fill(Color("White"))
        pygame.draw.rect(surface, Color("Black"), surface.get_rect(), 5, border_radius=15)

        # Draw text
        text = self.font.render(self.text, True, Color("Black"))
        text_rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, text_rect)

        screen.blit(surface, pos)


CHARACTER_POS = (WIDTH / 2, HEIGHT / 2)


class Dialogue(Logue):
    def __init__(self, line, character=None, current_scene=None):
        super().__init__(border_radius=15, rect_alpha=200, font=defaul_font, current_scene=current_scene)

        self.whole_interaction: LineOther | LinePlayer | None = None
        self.init_lines(line)
        self.current_line: LineOther | LinePlayer = self.whole_interaction

        self.answers_ui = [AnswerUI(e.text) for e in self.current_line.answers]

        self.character = Character(name=character, position=CHARACTER_POS)

        self.dialogue_box_rect = pygame.Rect(150, 300, 500, 500)
        self.text_box = MultiTextBox(self.current_line.text, size=self.dialogue_box_rect.size)

        self.answers_box_rect = monologue_rect

    def init_lines(self, line_data):
        self.whole_interaction = LineOther(**line_data)

    def _draw_background(self, screen):
        pygame.draw.rect(screen, Color("white"), self.dialogue_box_rect, 0, border_radius=self.border_radius)
        pygame.draw.rect(screen, Color("black"), self.dialogue_box_rect, 1, border_radius=self.border_radius)

    def _draw_answers(self, screen):

        start_y = 700
        x = 700
        for i, answer in enumerate(self.answers_ui):
            pos = x, start_y + i * 100
            answer.draw(screen, pos)

    def draw(self, win):
        if debug:
            pygame.draw.rect(win, Color("red"), self.dialogue_box_rect, 1)
        self.character.draw(win)
        self._draw_background(win)
        self.text_box.draw(win, self.dialogue_box_rect.topleft)

        if self.current_line is not None and self.current_line.answers is not None:
            self._draw_answers(win)

    def handle_events(self, events):
        for answer in self.answers_ui:
            answer.handle_events(events)
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._handle_space_key()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event.pos)

    def _handle_space_key(self):
        print("space")

    def _handle_mouse_click(self, pos):
        for answerui in self.answers_ui:
            if answerui.is_mouse_on_button(pos):
                # go to corresponding line
                for answer in self.current_line.answers:
                    if answerui.text == answer.text:
                        self._handle_answer_click(answer)

    def _handle_answer_click(self, answer):
        self.current_line = answer.line
        if self.current_line is not None:
            self.text_box = MultiTextBox(self.current_line.text, size=self.dialogue_box_rect.size)
            self.answers_ui = [AnswerUI(e.text) for e in self.current_line.answers]
            if self.current_line.answers is None:
                self.current_line = None
                self.answers_ui = []

        else:
            self.current_line = None
            self.answers_ui = []
            self.current_scene.next_event()
