import pygame

from src.screens.menu_screen import MenuScreen
from src.screens.home_screen import HomeScreen
from src.screens.level_select_screen import LevelSelectScreen
from src.screens.gameplay_screen import GameplayScreen

from data.save_manager import load_game_data
from .load_sounds import _load_sound
from src.config import *
from data.questions import QUESTION_GENERATORS

class GameManager:
    sounds = _load_sound()
    def __init__(self):        
        self.screens = {
            "HOME": HomeScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self),
        }

        self.active_screen_key = "HOME"
        self.active_screen = self.screens[self.active_screen_key]
        self.current_level_key = None
        
        self.menu = MenuScreen(self)

        self.game_data = load_game_data()
        pygame.mixer.music.play(loops=-1)
        
        self.questions_pool = [] 
        self.question_index = 0     

    def switch_screen(self, screen_key):

        if screen_key in self.screens:
            
            # --- TẠO BỘ CÂU HỎI KHI CHUYỂN TỚI GAMEPLAY ---
            if screen_key == "GAMEPLAY" and self.current_level_key:
                generator = QUESTION_GENERATORS.get(self.current_level_key)
                if generator:
                     # Gọi hàm tạo câu hỏi
                    generated_questions = generator(MAX_QUESTIONS)
                    self.questions_pool = generated_questions
                    self.question_index = 0
                else:
                    print(f"Không tìm thấy generator cho level: {self.current_level_key}")
                    self.questions_pool = []
                    
                self.screens[screen_key].on_enter()
                
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
        
    