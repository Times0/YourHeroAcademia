import logging

import pygame.sprite
from PygameUIKit import Group
from PygameUIKit.button import ButtonPngIcon
from pygame import Color

import config
from boring import images
from engine import GameEngine

logging.basicConfig(level=logging.DEBUG, filename="game.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt=" %M:%S")

logger = logging.getLogger(__name__)

EDITOR = False


class Game:
    def __init__(self, win):
        self.game_is_on = True
        self.win = win

        self.engine = GameEngine()
        self.engine.change_scene_to("classroom")

        self.ui = Group()
        self.btn_quit = ButtonPngIcon(images.btn_quit, Color("Grey"), self.quit)
        self.ui.add(self.btn_quit)

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
        self.ui.handle_events(events)
        self.engine.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.game_is_on = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                if EDITOR:
                    pass

    def draw(self, win):
        self.engine.draw(win)
        self.btn_quit.draw(win, *self.btn_quit.image.get_rect(topright=(config.WIDTH - 15, 15)).topleft)
        pygame.display.flip()

    def quit(self):
        self.game_is_on = False
