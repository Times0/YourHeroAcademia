import logging
import os.path
from typing import List

import config
from boring import images
from boring.utils import *
from config import WIDTH, HEIGHT
from scene_objects.character import Character
from scene_objects.dialogue import Dialogue
from scene_objects.escape_point import EscapePoint
from scene_objects.monologue import Monologue
from scene_objects.utils import create_event_from_data

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

        self.game_events = []
        self.event_index = 0

        self.engine = engine

        self.name = None

    def get_current_event(self) -> "Monologue" or "Dialogue" or None:
        if self.event_index < len(self.game_events):
            return self.game_events[self.event_index]
        else:
            return None

    def load_scene(self, scene_name: str):
        import json

        with open(os.path.join(config.data_path), encoding="utf-8") as f:
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
                self.game_events.append(create_event_from_data(event_data, self))
        return self

    def next_event(self):
        self.event_index += 1
        logger.info(f"Next event: {self.get_current_event()}")

    def change_affinity(self, character_name, amount):
        self.engine.change_affinity(character_name, amount)

    def add_event(self, event):
        logger.debug(f"Adding event {event}")
        self.game_events.insert(self.event_index + 1, event)
        logger.debug(f"Events: {self.game_events}")

    def __repr__(self):
        return f"GameScene({self.name})"
