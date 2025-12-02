import pygame

from src.screens.menu_screen import MenuScreen
from src.screens.level_select_screen import LevelSelectScreen
# from src.screens.gameplay_screen import GameplayScreen

from data.save_manager import load_game_data
from .load_sounds import _load_sound

class GameManager:
    sounds = _load_sound()
    def __init__(self):        
        # Khởi tạo tất cả các màn hình
        self.screens = {
            "MENU": MenuScreen(self),
            "LEVEL": LevelSelectScreen(self),
        }

        self.active_screen_key = "MENU"
        self.active_screen = self.screens[self.active_screen_key]
        self.current_level_key = None
        
        self.game_data = load_game_data()
        pygame.mixer.music.play(loops=-1)


    def switch_screen(self, screen_key):

        if screen_key in self.screens:
            self.active_screen_key = screen_key
            self.active_screen = self.screens[self.active_screen_key]
        else:
            print(f"Error: Screen {screen_key} not found!")
        

    def handle_input(self, event):
        self.active_screen.handle_input(event)

    def update(self):
        self.active_screen.update()

    def draw(self, surface):
        self.active_screen.draw(surface)