import logging

import pygame
import pygame as pg
from pygame.locals import *

from boring import images
from boring.config import WIDTH, HEIGHT
from boring.fonts import get_font
from scene import Character

logger = logging.getLogger(__name__)

defaul_font = get_font("animeace.ttf", 30)


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


debug = False


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
        current_width = current_height = 0
        current_surface = pygame.Surface((max_width, max_height), SRCALPHA)
        words = []
        cursor = 0
        while cursor < len(words_of_text):
            word = words_of_text[cursor]
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

    def draw(self, win):
        """Draw the current surface."""
        if self.requires_render:
            self.render_smart()
            self.requires_render = False

        if debug:
            pygame.draw.rect(win, Color("red"), self.rect.inflate(-10, -10), 1)
        win.blit(self.surfaces[self.current_index], self.rect.topleft)


MONOLOGUE_COUNTOUR_POS = (150, 500)
MONOLOGUE_CIRCLE_CENTER = (377, 860)


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
        screen.blit(images.mc, images.mc.get_rect(center=MONOLOGUE_CIRCLE_CENTER).move(0,-40))


monologue_rect = pygame.Rect(606, 788, 1166, 168)

page_counter_rect = pygame.Rect(1624, 672, 100, 100)


class Monologue(Logue):
    """
    A class representing a monologue in pygame.
    The text is broken up into chunks which fit within a specified area.
    These chunks can be navigated through using the space bar.
    """

    def __init__(self, text: str, character: dict = None, current_scene=None):
        super().__init__(border_radius=15, font=defaul_font, current_scene=current_scene)

        from scene import Character
        if character is not None:  # If we want to display a character
            self.character = Character(**character, position=(WIDTH / 2, HEIGHT / 2))

        self.text_box = MultiTextBox(text, font=defaul_font, position=monologue_rect.topleft, size=monologue_rect.size)

    def handle_events(self, events):
        """Handles the events for the monologue."""
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._handle_space_key()

    def _handle_space_key(self):
        """Handle the space key event."""
        self.text_box.current_index += 20
        if self.text_box.current_index >= len(self.text_box.surfaces):
            if self.current_scene is not None:
                self.current_scene.next_event()

    def draw(self, screen, draw_bg=True):
        """Draws the monologue on the screen."""
        if hasattr(self, "character"):
            self.character.draw(screen)
        if draw_bg:
            self._draw_background(screen)

        self.text_box.draw(screen)
        self._draw_page_counter(screen)

    def _draw_page_counter(self, screen):
        """Draws the page counter on the screen."""
        page_counter = self.font.render(
            f"{self.text_box.current_index + 1}/{len(self.text_box.surfaces)}", True, Color("Black"))
        screen.blit(page_counter, page_counter_rect.topleft)


class LineOther:
    """
    Type for a piece of dialogue that the other character says.
    text is the text that the character says.
    Either answers or monologue is not None.
    Answers is a list of LinePlayer that contains the answers that the player can give and the next line of dialogue
    Monologue is a string that the character says after the text is finished.
    """

    def __init__(self, text, answers: dict = None, monologue: str = None):
        self.text = text
        if answers is not None:
            self.answers = [LinePlayer(**answer) for answer in answers]
        else:
            self.answers = None
        self.monologue = monologue


class LinePlayer:
    """
    Type for a piece of dialogue that the player says.
    text is the text that the player says.
    line is the next line of dialogue that the other character says.
    """

    def __init__(self, preview: str, text: str, line: dict):
        self.preview: str = preview
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


# Answer UI constants
BORDER_SIZE = 5
BORDER_RADIUS = 15
INFLATE_SIZE = (20, 20)
TEXT_OFFSET = (10, 10)
TEXT_Y_OFFSET_MULTIPLIER = 50
OPTION_OFFSET = 10


class AnswerUI(Clickable):
    def __init__(self, text: str, index: int):
        super().__init__(None)
        self.text = text
        self.font = defaul_font

        self.render = self.font.render(self.text, True, Color("Black"))
        x, y = TEXTBOX_MONOLOGUE_POS
        y += index * (TEXT_Y_OFFSET_MULTIPLIER + OPTION_OFFSET)
        self.rect = self.render.get_rect(topleft=(x, y)).inflate(*INFLATE_SIZE)

    def draw(self, screen):
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        surface.fill(Color("White"))
        pygame.draw.rect(surface, Color("Black"), surface.get_rect(), BORDER_SIZE, border_radius=BORDER_RADIUS)

        # Draw text
        surface.blit(self.render, TEXT_OFFSET)
        screen.blit(surface, self.rect)


CHARACTER_POS = (WIDTH / 2, HEIGHT / 2)
TEXTBOX_MONOLOGUE_POS = monologue_rect.topleft


class CharacterTextBox(MultiTextBox):
    def __init__(self, text, character):
        w, h = 400, 500
        x, y = character.rect.move(20, 20).topright
        self.rect = pygame.Rect(x, y, w, h)
        super().__init__(text, position=(x, y), size=(w, h))


class Dialogue(Logue):
    def __init__(self, line, character, current_scene=None):
        super().__init__(border_radius=15, font=defaul_font, current_scene=current_scene)
        self.character = Character(name=character, position=CHARACTER_POS)
        self.answers_box_rect = monologue_rect

        self.whole_interaction: LineOther = LineOther(**line)
        self.current_line: LineOther | LinePlayer = self.whole_interaction

        self.answers_ui = []
        self.chosen_answer: LinePlayer | None = None

        self.character_text_box: CharacterTextBox | None = None
        self.player_answer: Monologue | None = None
        self.player_monologue: Monologue | None = None

        self.step = 0  # 0 = character text, 1 = both, 2 = answer text

        self.render_text_boxes()

    def render_text_boxes(self):
        if self.current_line is None:
            return
        self.character_text_box = CharacterTextBox(self.current_line.text, self.character)
        if self.current_line.answers is not None:
            self._init_answers_ui()
        elif self.current_line.monologue is not None:
            self.player_monologue = Monologue(self.current_line.monologue)

    def _draw_answers(self, screen):
        for answer in self.answers_ui:
            answer.draw(screen)

    def draw(self, win):
        self.character.draw(win)

        self._draw_background(win)

        if self.step in (0, 1):
            draw_transparent_rect_with_border_radius(win,
                                                     self.character_text_box.rect.inflate(15, 15), 15,
                                                     Color("white"), alpha=200)
            pygame.draw.rect(win, Color("Black"), self.character_text_box.rect.inflate(15, 15), 5, border_radius=15)

            self.character_text_box.draw(win)

        if self.step == 1:
            # draw answers / monologue
            if self.current_line.answers is not None:
                self._draw_answers(win)
            elif self.current_line.monologue is not None:
                self.player_monologue.draw(win, draw_bg=False)  # already drawn
        if self.step == 2:
            self.player_answer.draw(win, draw_bg=False)

    def handle_events(self, events):
        for answer in self.answers_ui:
            answer.handle_events(events)
        if self.player_monologue is not None:
            self.player_monologue.handle_events(events)
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._handle_space_key()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event.pos)

    def _handle_space_key(self):
        if self.step == 1 and self.current_line.answers is None:
            self.current_scene.next_event()
        if self.step in (0, 2):
            self.step += 1
            self.render_text_boxes()
        if self.step == 3:
            self.current_line = self.chosen_answer.line
            self.step = 0
            self.chosen_answer = None
            self.render_text_boxes()

    def _handle_mouse_click(self, pos):
        for answerui in self.answers_ui:
            if answerui.is_mouse_on_button(pos):
                print("clicked")
                for answer in self.current_line.answers:
                    if answerui.text == answer.preview:
                        self._handle_answer_click(answer)
                break

    def _handle_answer_click(self, answer):
        self.chosen_answer = answer
        self.player_answer = Monologue(answer.text)
        self.step = 2

    def _init_answers_ui(self):
        self.answers_ui = [AnswerUI(e.preview, i) for i, e in enumerate(self.current_line.answers)]


def draw_transparent_rect_with_border_radius(screen, rect, border_radius, color, alpha):
    surf = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.rect(surf, color, surf.get_rect().inflate(-1, -1), border_radius=border_radius)
    surf.set_alpha(alpha)
    screen.blit(surf, rect)
