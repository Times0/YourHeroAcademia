import os.path
from typing import List, Tuple

import pygame

import data
from boring import images
from boring.config import WIDTH, HEIGHT
from ui import Clickable


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

    def __init__(self, engine: "GameEngine"):
        self.background: pygame.Surface | None = None
        self.escape_points: List[EscapePoint] | None = None

        self.engine: "GameEngine" = engine

    def load_scene(self, scene_name: str):
        scene_data = data.scenes_data[scene_name]
        self.background = images.load(os.path.join("scenes", scene_data["background"]), size=(WIDTH, HEIGHT))
        self.escape_points = []
        for point_data in scene_data["escape_points"]:
            self.escape_points.append(EscapePoint(**point_data, game_engine=self.engine))

        return self


class EscapePoint(Clickable):
    def __init__(self, position: Tuple[int, int], destination: 'GameScene', game_engine: "GameEngine"):
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


