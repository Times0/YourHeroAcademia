import pygame as pg
from PygameUIKit.button import ButtonImageText

from scene_objects.character import Character
from scene_objects.monologue import Monologue, MONOLOGUE_TEXT_RECT
from scene_objects.utils import *
from scene_objects.utils import MultiTextBox
from boring import images

logger = logging.getLogger(__name__)


def create_event_from_data(event_data, scene) -> "Monologue" or "Dialogue":
    if event_data["type"] == "monologue":
        return Monologue(**event_data["data"], current_scene=scene)
    elif event_data["type"] == "dialogue":
        return Dialogue(**event_data["data"], current_scene=scene)


class LineOther:
    """
    Type for a piece of dialogue that the other character says.
    text is the text that the character says.
    Either answers or monologue is not None.
    Answers is a list of LinePlayer that contains the answers that the player can give and the next line of dialogue
    Monologue is a string that the character says after the text is finished.
    """

    def __init__(self, text, answers: dict = None, next_event: dict = None, scene=None):
        self.text = text
        if answers is not None:
            self.answers = [LinePlayer(**answer, scene=scene) for answer in answers]
        else:
            self.answers = None
        self.next_event = create_event_from_data(next_event, scene) if next_event is not None else None


class LinePlayer:
    """
    Type for a piece of dialogue that the player says.
    text is the text that the player says.
    line is the next line of dialogue that the other character says.
    """

    def __init__(self, preview: str, text: str, line: dict, impacts: dict = None, scene=None):
        self.preview: str = preview
        self.text: str = text
        if line is not None:
            self.line: LineOther = LineOther(**line, scene=scene)
        else:
            self.line = None
        self.impacts = impacts


# Answer UI constants
ANSWER_UI_POS = (429, 755)
BORDER_SIZE = 5
BORDER_RADIUS = 15
INFLATE_SIZE = (20, 20)
TEXT_OFFSET = (10, 10)
TEXT_Y_OFFSET_MULTIPLIER = 10

font_answer = get_font("animeace.ttf", 40)


class AnswerUI(ButtonImageText):
    def __init__(self, text: str, index: int, nb_answers, onclick_f):
        super().__init__(images.btn_answer,
                         onclick_f=onclick_f,
                         text=text,
                         text_color=Color("Black"),
                         image_hover=images.btn_answer_hover,
                         font=font_answer)

        if nb_answers == 3:
            x, y = (429, 700)
        else:
            x, y = ANSWER_UI_POS
        y += index * (TEXT_Y_OFFSET_MULTIPLIER + self.rect.height)
        self.rect.x = x
        self.rect.y = y

    def draw2(self, win):
        super().draw(win, *self.rect.topleft)


CHARACTER_POS_DEFAULT = (WIDTH / 2, HEIGHT * 0.8)
TEXTBOX_MONOLOGUE_POS = MONOLOGUE_TEXT_RECT.topleft

CHARACTER_TEXT_INFLATE = (20, 20)

font_character = get_font("animeace.ttf", 30)


class CharacterTextBox(MultiTextBox):
    def __init__(self, text, character):
        w, h = 400, 500
        x, y = character.rect.move(20, 20).topright
        self.rect = pygame.Rect(x, y, w, h)
        super().__init__(text, position=(x, y), size=(w, h), font=font_character)

    def draw(self, screen):
        rect = self.rect.copy()
        rect.height = self.get_current_text_height()
        rect.inflate_ip(*CHARACTER_TEXT_INFLATE)
        draw_transparent_rect_with_border_radius(screen, rect, Color("White"), 15, alpha=200)
        pygame.draw.rect(screen, Color("Black"), rect, 4, border_radius=15)
        super().draw(screen)


class Dialogue:
    def __init__(self, line, character, character_position=CHARACTER_POS_DEFAULT, current_scene=None):
        self.current_scene = current_scene

        self.character = Character(name=character, position=character_position)
        self.answers_box_rect = MONOLOGUE_TEXT_RECT

        self.whole_interaction: LineOther = LineOther(**line, scene=current_scene)
        self.current_line: LineOther | LinePlayer = self.whole_interaction

        self.answers_ui = []
        self.chosen_answer: LinePlayer | None = None

        self.character_text_box: CharacterTextBox | None = None
        self.player_answer: Monologue | None = None
        self.next_event: Dialogue | Monologue | None = None

        self.step = 0  # 0 = other speaks, 1 = player sees answers, 2 = player speaks

        self.render_text_boxes()

    def render_text_boxes(self):
        if self.current_line is None:
            return
        self.character_text_box = CharacterTextBox(self.current_line.text, self.character)
        if self.current_line.answers is not None:
            self._init_answers_ui()

    def _draw_answers(self, screen):
        for answer in self.answers_ui:
            answer.draw2(screen)

    def draw(self, win):
        self.character.draw(win)

        # self._draw_background(win)

        if self.step in (0, 1):
            self.character_text_box.draw(win)
        if self.step == 1:
            self._draw_answers(win)
        elif self.step == 2:
            self.player_answer.draw(win, draw_bg=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._handle_space_key_or_click()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_space_key_or_click()

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
            else:
                self.current_line = None
                self.current_scene.next_event()
                return
        elif self.step == 1:
            self.step = 2
        elif self.step == 2:  # player answered
            if self.chosen_answer.line is None:
                # End of dialogue
                print(f"End of dialogue bc {self.chosen_answer.preview} does not have a line")
                self.current_line = None
                self.current_scene.next_event()
                return
            else:
                self.step = 0
                self.current_line = self.chosen_answer.line
                self.chosen_answer = None

        self.render_text_boxes()
        if debug:
            print(f"-> New step : {self.step}")

    def _handle_space_key_or_click(self):
        if self.step == 0:
            if self.character_text_box.is_finished():
                self.next_step()
            else:
                self.character_text_box.next()
        elif self.step == 2:
            self.next_step()

    def _handle_answer_click(self, answer):
        print(f"Chosen answer: {answer.preview}")
        self.chosen_answer = answer
        if answer.impacts is not None:
            for character, delta in answer.impacts.items():
                self.change_affinity(character, delta)
        self.player_answer = Monologue(answer.text)
        self.load_new_line(answer.line)
        self.next_step()

    def _init_answers_ui(self):
        self.answers_ui = []
        for i, answer in enumerate(self.current_line.answers):
            f = lambda a=answer: self._handle_answer_click(a)
            self.answers_ui.append(AnswerUI(answer.preview, i, len(self.current_line.answers), f))

    def change_affinity(self, character, delta):
        """Change affinity of character by delta
        Propagates to current scene to engine
        """
        self.current_scene.change_affinity(character, delta)
        print(self.current_scene.engine.affinites)

    def load_new_line(self, line):
        self.current_line = line
        self.next_event = line.next_event
        if self.next_event is not None:
            self.current_scene.add_event(self.next_event)


def draw_transparent_rect_with_border_radius(screen, rect, color, border_radius, alpha):
    surf = pg.Surface(rect.size, pg.SRCALPHA)
    pg.draw.rect(surf, color, surf.get_rect(), border_radius=border_radius)
    surf.set_alpha(alpha)
    screen.blit(surf, rect)
