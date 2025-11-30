# src/core/game_manager.py
import pygame
from src.screens.menu_screen import MenuScreen
from src.screens.level_select_screen import LevelSelectScreen
from src.screens.gameplay_screen import GameplayScreen
from data.questions import get_level_1_questions, get_level_2_questions, get_level_3_questions, get_level_4_questions, get_level_5_questions, get_level_6_questions
from data.save_manager import load_game_data, save_game_data 
# Import LEVELS từ level_select_screen để ánh xạ
from src.screens.level_select_screen import LEVELS 

# Ánh xạ LEVEL KEY với hàm tạo câu hỏi tương ứng
QUESTION_FUNCTIONS = {
    "LEVEL_1": get_level_1_questions,
    "LEVEL_2": get_level_2_questions,
    "LEVEL_3": get_level_3_questions,
    "LEVEL_4": get_level_4_questions,
    "LEVEL_5": get_level_5_questions,
    "LEVEL_6": get_level_6_questions,
}

class GameManager:
    def __init__(self):
        # Khởi tạo tất cả các màn hình
        self.screens = {
            "MENU": MenuScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self)
        }
        self.current_screen_name = "MENU" 
        self.current_level_key = None 
        self.questions_pool = [] 
        self.question_index = 0 
        
        # Tải dữ liệu Game (Highscore)
        self.game_data = load_game_data()

    def switch_screen(self, new_screen_name):
        self.current_screen_name = new_screen_name
        
        if new_screen_name == "GAMEPLAY":
            if self.current_level_key and self.current_level_key in QUESTION_FUNCTIONS:
                # 1. Tải câu hỏi (20 câu/level)
                self.questions_pool = QUESTION_FUNCTIONS[self.current_level_key](num_questions=20)
                self.question_index = 0
                # 2. Reset và tải câu hỏi đầu tiên trên màn hình Gameplay
                self.screens["GAMEPLAY"].reset_game()
                self.screens["GAMEPLAY"].load_next_question() 
            else:
                print("LỖI: Level không hợp lệ hoặc chưa chọn.")
                self.current_screen_name = "LEVEL" 

    def handle_input(self, event):
        self.screens[self.current_screen_name].handle_input(event)

    def update(self):
        self.screens[self.current_screen_name].update()

    def draw(self, surface):
        self.screens[self.current_screen_name].draw(surface)

    def save_score(self, score):
        """Lưu điểm cao mới cho level hiện tại"""
        if self.current_level_key:
            try:
                # Tìm index của level (LEVEL_1 -> 0, LEVEL_6 -> 5)
                level_index = int(self.current_level_key.split('_')[1]) - 1
                
                if level_index < len(self.game_data['highscores']):
                    # Cập nhật điểm cao
                    if score > self.game_data['highscores'][level_index]:
                        self.game_data['highscores'][level_index] = score
                        save_game_data(self.game_data)
                        print(f"LƯU ĐIỂM CAO MỚI: Level {level_index+1}: {score}")
            except Exception as e:
                print(f"Lỗi khi lưu điểm: {e}")