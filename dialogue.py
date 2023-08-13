import logging
import pygame
import pygame as pg
from pygame.locals import *

from boring import images
from boring.config import WIDTH, HEIGHT
from boring.fonts import get_font
from scene import Character

logger = logging.getLogger(__name__)

defaul_font = get_font("basic.ttf", 30)
font_monologue = get_font("animeace2_bld.ttf", 30)
font_monologue_whisper = get_font("animeace2_ital.ttf", 30)


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
            word_surface = self.font.render(word + " ", True, Color("Black"))
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


counter_font = get_font("animeace.ttf", 40)

MONOLOGUE_TEXT_RECT = pygame.Rect(590, 770, 1166, 180)
PAGE_COUNTER_POS = (1693, 706)
MONOLOGUE_COUNTOUR_POS = (150, 500)
MONOLOGUE_CIRCLE_CENTER = (377, 880)


class Monologue(Logue):
    """
    A class representing a monologue in pygame.
    The text is broken up into chunks which fit within a specified area.
    These chunks can be navigated through using the space bar.
    """

    def __init__(self, text: str, character: dict = None, current_scene=None, whisper=False):
        super().__init__(border_radius=15, font=defaul_font, current_scene=current_scene)

        from scene import Character
        if character is not None:  # If we want to display a character
            self.character = Character(**character, position=(WIDTH / 2, HEIGHT / 2))
        self.whisper = whisper

        if self.whisper:
            font = font_monologue_whisper
            text = f"({text})" if text[0] != "(" else f"{text}"
        else:
            font = font_monologue
        self.text_box = MultiTextBox(text, font=font, position=MONOLOGUE_TEXT_RECT.topleft,
                                     size=MONOLOGUE_TEXT_RECT.size)

    def handle_events(self, events):
        """Handles the events for the monologue."""
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self._handle_space_key()

    def _handle_space_key(self):
        """Handle the space key event."""
        self.text_box.current_index += 1
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
        page_counter = counter_font.render(
            f"{self.text_box.current_index + 1}/{len(self.text_box.surfaces)}", True, Color("Black"))
        screen.blit(page_counter, page_counter.get_rect(center=PAGE_COUNTER_POS))


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

    def __init__(self, preview: str, text: str, line: dict, impacts: dict = None):
        self.preview: str = preview
        self.text: str = text
        if line is not None:
            self.line: LineOther = LineOther(**line)
        else:
            self.line = None
        self.impacts = impacts


# Answer UI constants
ANSWER_UI_POS = (556, 525)
BORDER_SIZE = 5
BORDER_RADIUS = 15
INFLATE_SIZE = (20, 20)
TEXT_OFFSET = (10, 10)
TEXT_Y_OFFSET_MULTIPLIER = 30

from PygameUIKit.button import ButtonText


class AnswerUI(ButtonText):
    def __init__(self, text: str, index: int, onclick_f):
        super().__init__(text, onclick_f, Color("White"), font_monologue, 15, Color("Black"),
                         outline_color=Color("Black"))
        self.text = text

        render = self.font.render(self.text, True, Color("Black"))
        x, y = ANSWER_UI_POS
        y += index * (TEXT_Y_OFFSET_MULTIPLIER + render.get_height())
        self.rect = render.get_rect(topleft=(x, y)).inflate(*INFLATE_SIZE)

    def on_hover(self):
        pass

    def draw2(self, win):
        super().draw(win, *self.rect.topleft)


CHARACTER_POS = (WIDTH / 2, HEIGHT / 2)
TEXTBOX_MONOLOGUE_POS = MONOLOGUE_TEXT_RECT.topleft

CHARACTER_TEXT_INFLATE = (20, 20)


class CharacterTextBox(MultiTextBox):
    def __init__(self, text, character):
        w, h = 400, 500
        x, y = character.rect.move(20, 20).topright
        self.rect = pygame.Rect(x, y, w, h)
        super().__init__(text, position=(x, y), size=(w, h), font=font_monologue)

    def draw(self, screen):
        rect = self.rect.copy()
        rect.height = self.get_current_text_height()
        rect.inflate_ip(*CHARACTER_TEXT_INFLATE)
        draw_transparent_rect_with_border_radius(screen, rect, Color("White"), 15, alpha=200)
        pygame.draw.rect(screen, Color("Black"), rect, 4, border_radius=15)
        super().draw(screen)


class Dialogue(Logue):
    def __init__(self, line, character, current_scene=None):
        super().__init__(border_radius=15, font=font_monologue, current_scene=current_scene)
        self.character = Character(name=character, position=CHARACTER_POS)
        self.answers_box_rect = MONOLOGUE_TEXT_RECT

        self.whole_interaction: LineOther = LineOther(**line)
        self.current_line: LineOther | LinePlayer = self.whole_interaction

        self.answers_ui = []
        self.chosen_answer: LinePlayer | None = None

        self.character_text_box: CharacterTextBox | None = None
        self.player_answer: Monologue | None = None
        self.player_monologue: Monologue | None = None

        self.step = 0  # 0 = other speaks, 1 = player sees answers, 2 = player's chara is monologuing, 3 = player speaks

        self.render_text_boxes()

    def render_text_boxes(self):
        if self.current_line is None:
            return
        self.character_text_box = CharacterTextBox(self.current_line.text, self.character)
        if self.current_line.answers is not None:
            self._init_answers_ui()
        elif self.current_line.monologue is not None:
            logger.debug("Init player monologue")
            self.player_monologue = Monologue(self.current_line.monologue, whisper=True)

    def _draw_answers(self, screen):
        for answer in self.answers_ui:
            answer.draw2(screen)

    def draw(self, win):
        self.character.draw(win)

        self._draw_background(win)

        if self.step in (0, 1):
            self.character_text_box.draw(win)

        if self.step == 1:
            # draw answers
            self._draw_answers(win)
        elif self.step == 2:
            self.player_monologue.draw(win, draw_bg=False)  # already drawn
        elif self.step == 3:
            self.player_answer.draw(win, draw_bg=False)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._handle_space_key()
                    return
        if self.step == 0:
            # Other is talking waiting for space press handled already
            pass
            return
        elif self.step == 1:
            # Player has to choose answer
            for answer in self.answers_ui:
                answer.handle_events(events)
        elif self.step == 2:
            pass
        elif self.step == 3:
            # wait for space press
            pass

    def next_step(self):
        if debug:
            print(f"Old step: {self.step}", end=" ")
        if self.step == 0:
            if self.current_line.answers is not None:
                self.step = 1
            elif self.current_line.monologue is not None:
                self.step = 2
            else:
                self.current_line = None
                self.current_scene.next_event()
                return
        elif self.step == 1:
            self.step = 3
        elif self.step == 2:
            self.step = 3
            self.current_line = None
            self.current_scene.next_event()
            return
        elif self.step == 3:  # player answered
            if self.chosen_answer.line is None:
                # End of dialogue
                print(f"End of dialogue bc {self.chosen_answer.preview} does not have a line")
                self.current_line = None
                self.current_scene.next_event()
                return
            self.step = 0
            self.current_line = self.chosen_answer.line
            self.chosen_answer = None

        self.render_text_boxes()
        if debug:
            print(f"-> New step : {self.step}")

    def _handle_space_key(self):
        if self.step == 0:
            if self.character_text_box.is_finished():
                self.next_step()
            else:
                self.character_text_box.next()
        elif self.step == 1:
            pass
        elif self.step == 2:
            print("Handling space key in step 2")
            logger.debug("Handling space key in step 2")
            if self.player_monologue.text_box.is_finished():
                logger.debug("Monologue finished")
                self.next_step()
            else:
                logger.debug("Monologue not finished")
                self.player_monologue.text_box.next()
        elif self.step == 3:
            self.next_step()

    def _handle_answer_click(self, answer):
        print(f"Chosen answer: {answer.preview}")
        self.chosen_answer = answer
        if answer.impacts is not None:
            for character, delta in answer.impacts.items():
                self.change_affinity(character, delta)
        self.player_answer = Monologue(answer.text)
        if self.step == 1:
            self.next_step()

    def _init_answers_ui(self):
        for i, answer in enumerate(self.current_line.answers):
            f = lambda: self._handle_answer_click(answer)
            self.answers_ui.append(AnswerUI(answer.preview, i, f))

    def change_affinity(self, character, delta):
        """Change affinity of character by delta
        Propagates to current scene to engine
        """
        self.current_scene.change_affinity(character, delta)
        print(self.current_scene.engine.affinites)


def draw_transparent_rect_with_border_radius(screen, rect, color, border_radius, alpha):
    surf = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.rect(surf, color, surf.get_rect(), border_radius=border_radius)
    surf.set_alpha(alpha)
    screen.blit(surf, rect)
