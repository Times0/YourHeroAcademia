from scene_objects.character import Character
from scene_objects.utils import *

counter_font = get_font("animeace.ttf", 40)

MONOLOGUE_TEXT_RECT = pygame.Rect(590, 770, 1166, 180)
PAGE_COUNTER_POS = (1693, 706)


class Monologue(Logue):
    """
    A class representing a monologue in pygame.
    The text is broken up into chunks which fit within a specified area.
    These chunks can be navigated through using the space bar.
    """

    def __init__(self, text: str, character: dict = None, current_scene=None, whisper=False):
        super().__init__(border_radius=15, font=defaul_font, current_scene=current_scene)

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
