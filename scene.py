import logging
import os.path
from typing import List, Tuple

from boring import images
from boring.config import WIDTH, HEIGHT
from boring.utils import *
from character import Character
from dialogue import Monologue, Dialogue
from ui import Clickable

logger = logging.getLogger(__name__)


class GameScene:
    """
    This class holds the information of one game screen, the game is made of many game screens
    Information include:
    - background
    - Yellow points (escape points)
    - Characters present
    - Dialogues
    - Monologues

    These windows are rendered in the game engine
    """

    def __init__(self, engine):
        self.background: pygame.Surface | None = None
        self.escape_points: List[EscapePoint] | None = None
        self.charcter: Character | None = None

        self.events = []
        self.event_index = 0

        self.engine = engine

        self.name = None

    def get_current_event(self) -> "Monologue" or "Dialogue" or None:
        if self.event_index < len(self.events):
            return self.events[self.event_index]
        else:
            return None

    def load_scene(self, scene_name: str):
        import json

        with open(os.path.join("data.json")) as f:
            data = json.load(f)

        self.name = scene_name
        scene_data = data[scene_name]
        self.background = images.load(os.path.join("scenes", scene_data["background"]), size=(WIDTH, HEIGHT))
        self.escape_points = []
        for point_data in scene_data["escape_points"]:
            self.escape_points.append(EscapePoint(**point_data, game_engine=self.engine))
        if "character" in scene_data:
            self.charcter = Character(**scene_data["character"])
        if "events" in scene_data:
            for event_data in scene_data["events"]:
                self.events.append(create_event_from_data(event_data, self))
        return self

    def next_event(self):
        self.event_index += 1


def create_event_from_data(event_data, scene) -> "Monologue" or "Dialogue":
    if event_data["type"] == "monologue":
        return Monologue(**event_data["data"], current_scene=scene)
    elif event_data["type"] == "dialogue":
        print(event_data["data"])
        return Dialogue(**event_data["data"], current_scene=scene)


from boring.fonts import get_font

font_tooltip = get_font("animeace.ttf", 32)


class EscapePoint(Clickable):
    def __init__(self, position: Tuple[int, int], destination: str, game_engine):
        super().__init__(self.go_to_next_scene)
        self.position = position
        self.destination = destination
        self.game_engine = game_engine
        self.animate_size = 10
        self.growing = True

    def draw(self, screen):
        size = 10

        if self.show_tooltip:
            # Improved Glow effect
            # The glow_sizes list determines the radii of the circles for the glow effect,
            # from outermost (largest and most transparent) to innermost (smallest and least transparent).
            glow_sizes = [size + i for i in range(15, 3, -2)]  # e.g. [25, 23, 21, ...]

            # Colors gradually transition from a soft yellow with low opacity to a stronger yellow with higher opacity.
            colors = [(255, 255, 128, i) for i in range(10, 60, 10)]

            for g_size, color in zip(glow_sizes, colors):
                glow_surface = pygame.Surface((g_size * 2, g_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, color, (g_size, g_size), g_size)
                screen.blit(glow_surface, (self.position[0] - g_size, self.position[1] - g_size))

            # Draw the primary dot
            size += 3
            pygame.draw.circle(screen, pygame.Color("Orange"), self.position, size)
        else:
            # Animation logic
            if self.growing:
                self.animate_size += 0.2  # Adjust speed as needed
                if self.animate_size >= 12:  # Maximum size
                    self.growing = False
            else:
                self.animate_size -= 0.2  # Adjust speed as needed
                if self.animate_size <= 8:  # Minimum size
                    self.growing = True

            pygame.draw.circle(screen, pygame.Color("Yellow"), self.position, int(self.animate_size))
            pygame.draw.circle(screen, pygame.Color("Black"), self.position, self.animate_size, 2)

        self.rect = pygame.Rect(self.position[0] - self.animate_size, self.position[1] - self.animate_size,
                                2 * self.animate_size, 2 * self.animate_size)
        # draw border arround the escape point circle

        if self.show_tooltip:
            self.draw_tooltip(screen)

    def go_to_next_scene(self):
        self.game_engine.change_scene_to(self.destination)

    def draw_tooltip(self, screen):
        text_surface = render_glow(self.destination, font_tooltip, pygame.Color("White"), pygame.Color("Black")  )
        text_rect = text_surface.get_rect(center=self.position)
        text_rect.y -= 50
        screen.blit(text_surface, text_rect)
