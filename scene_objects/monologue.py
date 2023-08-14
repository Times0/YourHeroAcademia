from scene_objects.character import Character
from scene_objects.utils import *
from boring import images

counter_font = get_font("animeace.ttf", 40)

x, y = 150, 540  # MODIFY HERE TO CHANGE THE POSITION OF THE MONOLOGUE

# Relative to the monologue background
MONOLOGUE_BACKGROUND_POS = (x, y)
MONOLOGUE_TEXT_RECT = pygame.Rect(x + 440, y + 270, 1166, 180)
MONOLOGUE_CIRCLE_CENTER = x + 227, y + 380
PAGE_COUNTER_POS = x + 1543, y + 206

font_monologue = get_font("animeace2_bld.ttf", 20)
font_monologue_whisper = get_font("animeace2_ital.ttf", 20)


class Monologue:
    """
    A class representing a monologue in pygame.
    The text is broken up into chunks which fit within a specified area.
    These chunks can be navigated through using the space bar.
    """

    def __init__(self, text: str, character: dict = None, current_scene=None, whisper=False):
        self.current_scene = current_scene
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
            if event.type == MOUSEBUTTONDOWN:
                self._handle_space_key()

    def _handle_space_key(self):
        """Handle the space key event."""
        self.text_box.current_index += 1
        print(f"Current index: {self.text_box.current_index}, len: {len(self.text_box.surfaces)}")
        if self.text_box.current_index >= len(self.text_box.surfaces):
            print(f"Current scene: {self.current_scene}")
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

    @staticmethod
    def _draw_background(screen):
        screen.blit(images.text_contour, MONOLOGUE_BACKGROUND_POS)
        screen.blit(images.mc, images.mc.get_rect(center=MONOLOGUE_CIRCLE_CENTER).move(0, -40))

    def _draw_page_counter(self, screen):
        """Draws the page counter on the screen."""
        page_counter = counter_font.render(
            f"{self.text_box.current_index + 1}/{len(self.text_box.surfaces)}", True, Color("Black"))
        screen.blit(page_counter, page_counter.get_rect(center=PAGE_COUNTER_POS))
