from game_scenes import GameScene


class GameEngine:
    def __init__(self):
        self.current_window = None
        self.loaded_scenes = {}

    def handle_events(self, events):
        if not self.current_window:
            return
        for point in self.current_window.escape_points:
            point.handle_events(events)


    def update(self, dt):
        pass

    def draw(self, screen):
        if not self.current_window:
            return
        # draw background
        screen.blit(self.current_window.background, (0, 0))

        # draw escape points
        for point in self.current_window.escape_points:
            point.draw(screen)

    def change_scene_to(self, scene_name):
        self.current_window = self.get_scene(scene_name)

    def get_scene(self, scene_name: str) -> GameScene:
        if scene_name in self.loaded_scenes:
            return self.loaded_scenes[scene_name]
        else:
            self.loaded_scenes[scene_name] = GameScene(self).load_scene(scene_name)
            return self.loaded_scenes[scene_name]
