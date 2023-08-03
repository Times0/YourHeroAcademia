import pygame.sprite

from boring import config
from boring.config import Color
from engine import GameEngine


class Game:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win

        self.engine = GameEngine()
        self.engine.change_scene_to("entrance")

    def run(self):
        clock = pygame.time.Clock()
        while self.game_is_on:
            dt = clock.tick(config.FPS)
            self.win.fill(Color("Black"))
            self.draw(self.win)
            self.update(dt)
            self.events()

    def update(self, dt):
        self.engine.update(dt)

    def events(self):
        events = pygame.event.get()
        self.engine.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.game_is_on = False

    def draw(self, win):
        win.fill(Color("Black"))
        self.engine.draw(win)
        pygame.display.flip()
