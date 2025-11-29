# src/core/game_manager.py
import pygame
from src.screens.menu_screen import MenuScreen
from src.screens.level_select_screen import LevelSelectScreen
from src.screens.gameplay_screen import GameplayScreen

class GameManager:
    def __init__(self):
        # Khởi tạo tất cả các màn hình
        self.screens = {
            "MENU": MenuScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self)
        }
        self.current_screen_name = "MENU" # Bắt đầu bằng màn hình Menu
        self.current_level_key = None 

    def switch_screen(self, new_screen_name):
        self.current_screen_name = new_screen_name
        
        if new_screen_name == "GAMEPLAY":
            self.screens["GAMEPLAY"].load_next_question()

    def handle_input(self, event):
        self.screens[self.current_screen_name].handle_input(event)

    def update(self):
        self.screens[self.current_screen_name].update()

    def draw(self, surface):
        self.screens[self.current_screen_name].draw(surface)