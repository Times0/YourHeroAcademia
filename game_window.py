import os.path
from typing import List, Tuple

import pygame

from boring import images
from boring.config import WIDTH, HEIGHT


class GameWindow:
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

    def __init__(self,
                 background_path: str,
                 escape_points: List['EscapePoint'],
                 *args):
        self.background = images.load(os.path.join("scenes", background_path), size=(WIDTH, HEIGHT))
        self.escape_points = escape_points
        other_objects = []
        for arg in args:
            other_objects.append(arg)


class Clickable:
    def __init__(self, onclick_f):
        self.is_hover = False
        self.clicked = False
        self.onclick_f = onclick_f
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def is_mouse_on_button(self, pos):
        return self.rect.collidepoint(pos)

    def on_hover(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

    def on_unhover(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouse_on_button(event.pos):
                    self.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                if self.clicked and self.is_mouse_on_button(event.pos):
                    print("Clicked")
                    self._on_click()
                self.clicked = False

            if event.type == pygame.MOUSEMOTION:
                was_hover = self.is_hover
                self.is_hover = self.is_mouse_on_button(event.pos)
                if self.is_hover and not was_hover:
                    self.on_hover()
                elif not self.is_hover and was_hover:
                    self.on_unhover()

    def _on_click(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.onclick_f()


class EscapePoint(Clickable):
    def __init__(self, position: Tuple[int, int], destination: 'GameWindow'):
        super().__init__(self.goto_dest)
        self.position = position
        self.destination = destination

    def draw(self, screen):
        size = 10
        pygame.draw.circle(screen, pygame.Color("Yellow"), self.position, size)
        self.rect = pygame.Rect(self.position[0] - size, self.position[1] - size, size * 2, size * 2)

    def goto_dest(self):
        print("Clicked on escape point")


void = GameWindow("1/void.jpg", [])
first_window = GameWindow("1/entrance00.jpg", [EscapePoint((100, 100), void),
                                               EscapePoint((200, 200), void)])
