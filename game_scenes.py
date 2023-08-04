import logging
import os.path
from typing import List, Tuple

import pygame

import data
from boring import images
from boring.config import WIDTH, HEIGHT
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

    def get_current_event(self) -> "Monologue" or "Dialogue" or None:
        if self.event_index < len(self.events):
            return self.events[self.event_index]
        else:
            return None

    def load_scene(self, scene_name: str):
        scene_data = data.scenes_data[scene_name]
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
        return Monologue(**event_data["data"], scene=scene)


class EscapePoint(Clickable):
    def __init__(self, position: Tuple[int, int], destination: 'GameScene', game_engine):
        super().__init__(self.go_to_next_scene)
        self.position = position
        self.destination = destination
        self.game_engine = game_engine

    def draw(self, screen):
        size = 10
        pygame.draw.circle(screen, pygame.Color("Yellow"), self.position, size)
        self.rect = pygame.Rect(self.position[0] - size, self.position[1] - size, size * 2, size * 2)

    def go_to_next_scene(self):
        self.game_engine.change_scene_to(self.destination)


class Character:
    def __init__(self, name: str, position: Tuple[int, int]):
        self.name = name
        self.position = position
        self.humeur = "neutral"

    def draw(self, screen):
        img = images.loader.get_image(self.name, self.humeur)
        screen.blit(img, img.get_rect(center=self.position))
