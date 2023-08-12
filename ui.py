import pygame


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

        self.show_tooltip = False

    def is_mouse_on_button(self, pos):
        return self.rect.collidepoint(pos)

    def on_hover(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        self.show_tooltip = True

    def on_unhover(self):
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.show_tooltip = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_mouse_on_button(event.pos):
                    self.clicked = True

            if event.type == pygame.MOUSEBUTTONUP:
                if self.clicked and self.is_mouse_on_button(event.pos):
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
        if self.onclick_f is not None:
            self.onclick_f()
