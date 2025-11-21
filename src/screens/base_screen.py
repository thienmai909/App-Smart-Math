from abc import ABC, abstractmethod

class BaseScreen(ABC):
    def __init__(self, game_manager):
        self.game_manager = game_manager

    @abstractmethod
    def handle_input(self, event):
        """Xử lý sự kiện chuột/phím"""
        pass

    @abstractmethod
    def update(self):
        """Cập nhật logic (timer, animation)"""
        pass

    @abstractmethod
    def draw(self):
        """Vẽ lên màn hình"""
        pass