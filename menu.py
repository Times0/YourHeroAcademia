import logging

import pygame
from PygameUIKit import button, Group
from pygame.color import Color

from boring import images
from boring.fonts import get_font

logger = logging.getLogger(__name__)


class MainMenu:
    def __init__(self, win, game_class):
        self.win = win
        self.game_class = game_class

        # UI
        self.ui = Group()
        self.font_menu_btn = get_font("mha.ttf", 150)

        self.btn_start = button.ButtonText("Start new game", self.start_game, Color("White"), self.font_menu_btn,
                                           ui_group=self.ui, border_radius=10)
        self.btn_quit = button.ButtonText("Leave", self.quit_game, Color("White"), self.font_menu_btn,
                                          ui_group=self.ui, border_radius=10)

        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60)
            self.draw(self.win)
            self.update(dt)
            self.events()

    def events(self):
        events = pygame.event.get()
        self.ui.handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(Color("Black"))
        screen.blit(images.main_menu_bg, (0, 0))
        SCREEN_CENTER_W = screen.get_width() // 2
        SCREEN_CENTER_H = screen.get_height() // 2
        self.btn_start.draw(screen, *self.btn_start.surface.get_rect(center=(SCREEN_CENTER_W, SCREEN_CENTER_H - 150)).topleft)
        self.btn_quit.draw(screen, *self.btn_quit.surface.get_rect(center=(SCREEN_CENTER_W, SCREEN_CENTER_H + 150)).topleft)
        pygame.display.flip()

    def start_game(self):
        logger.info("Starting game")
        self.running = False
        self.game_class(self.win).run()

    def quit_game(self):
        logger.info("Quitting game...")
        pygame.quit()
        exit()
