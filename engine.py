from game_window import GameWindow


class GameEngine:
    def __init__(self, game_window: GameWindow):
        self.current_window = game_window

    def handle_events(self, events):
        for point in self.current_window.escape_points:
            point.handle_events(events)

    def update(self, dt):
        pass

    def draw(self, screen):
        # draw background
        screen.blit(self.current_window.background, (0, 0))

        # draw escape points
        for point in self.current_window.escape_points:
            point.draw(screen)

