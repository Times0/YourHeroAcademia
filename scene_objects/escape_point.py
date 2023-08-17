from typing import Tuple

import pygame

from boring.fonts import get_font
from boring.utils import render_glow
from ui import Clickable

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

    def draw_animation(self, screen):
        pass

    def go_to_next_scene(self):
        self.game_engine.change_scene_to(self.destination)

    def draw_tooltip(self, screen):
        dest = self.destination.replace("_", " ").title()
        text_surface = render_glow(dest, font_tooltip, pygame.Color("White"), pygame.Color("Black"))
        text_rect = text_surface.get_rect(center=self.position)
        text_rect.y -= 50
        screen.blit(text_surface, text_rect)
