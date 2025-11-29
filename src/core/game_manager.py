# src/core/game_manager.py
from src.screens.gameplay_screen import GameplayScreen
from src.screens.menu_screen import MenuScreen 

class GameManager:
    def __init__(self):
        # Khởi tạo tất cả các màn hình
        self.screens = {
            "MENU": MenuScreen(self),
            "GAMEPLAY": GameplayScreen(self)
        } 
        # Bắt đầu bằng màn hình MENU
        self.current_screen = self.screens["MENU"] 
        print(f"GameManager khởi tạo. Màn hình hiện tại: {self.current_screen.__class__.__name__}")

    def switch_screen(self, screen_name):
        """Chuyển đổi màn hình hiện tại"""
        if screen_name in self.screens:
            print(f"Chuyển màn hình từ {self.current_screen.__class__.__name__} sang {screen_name}")
            self.current_screen = self.screens[screen_name]
        else:
            print(f"Lỗi: Không tìm thấy màn hình '{screen_name}'")

    def handle_input(self, event):
        self.current_screen.handle_input(event)

    def update(self):
        self.current_screen.update()

    def draw(self, surface):
        self.current_screen.draw(surface)