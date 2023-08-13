from scene_objects.scene import GameScene


class GameEngine:
    def __init__(self):
        self.current_scene: GameScene | None = None
        self.loaded_scenes = {}

        self.affinites = {}  # Charactername: affinity(int)

    def handle_events(self, events):
        if not self.current_scene:
            return
        for point in self.current_scene.escape_points:
            point.handle_events(events)
        if self.current_scene.get_current_event() is not None:
            self.current_scene.get_current_event().handle_events(events)

    def update(self, dt):
        pass

    def draw(self, screen):
        if not self.current_scene:
            return
        # draw background
        screen.blit(self.current_scene.background, (0, 0))

        # draw character
        if self.current_scene.charcter:
            self.current_scene.charcter.draw(screen)

        # draw mono/dialogues
        if self.current_scene.get_current_event() is not None:
            self.current_scene.get_current_event().draw(screen)

        # draw escape points
        for point in self.current_scene.escape_points:
            point.draw(screen)

    def change_scene_to(self, scene_name):
        self.current_scene = self.get_scene(scene_name)

    def get_scene(self, scene_name: str) -> GameScene:
        if scene_name in self.loaded_scenes:
            return self.loaded_scenes[scene_name]
        else:
            self.loaded_scenes[scene_name] = GameScene(self).load_scene(scene_name)
            return self.loaded_scenes[scene_name]

    def change_affinity(self, character_name, amount):
        if character_name in self.affinites:
            self.affinites[character_name] += amount
        else:
            self.affinites[character_name] = amount
