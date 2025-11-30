import pygame
from src.screens.menu_screen import MenuScreen
from src.screens.level_select_screen import LevelSelectScreen
from src.screens.gameplay_screen import GameplayScreen

class GameManager:
    def __init__(self):
        # Dữ liệu cho phiên chơi
        self.current_level = 1
        self.total_score = 0

        # Quản lý màn hình
        # Khởi tạo các screen, truyền 'self' vào để chúng có thể gọi ngược lại
        self.screens = {
            "MENU": MenuScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self)
        }

        self.active_screen_key = "MENU"
        self.active_screen = self.screens["MENU"] # | = self.screens[self.active_screen_key]
    
    def switch_screen(self, screen_key):
        """Hàm để các màn hình con gọi khi muốn chuyển cảnh"""
        if screen_key in self.screens:
            self.active_screen_key = screen_key
            self.active_screen = self.screens[screen_key]
        else:
            print(f"Error: Screen {screen_key} not found!")

    def handle_input(self, event):
        self.active_screen.handle_input(event)
    
    def update(self):
        self.active_screen.update()

    def draw(self, surface):
        self.active_screen.draw(surface)