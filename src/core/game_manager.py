import pygame
import os 
import sys 
from src.screens.menu_screen import MenuScreen
from src.screens.level_select_screen import LevelSelectScreen
from src.screens.gameplay_screen import GameplayScreen
from data.save_manager import load_game_data, save_game_data 
from .load_sounds import _load_sound
from src.config import MAX_QUESTIONS, MAX_SCORE_PER_LEVEL, STAR_THRESHOLDS 
from src.screens.level_select_screen import LEVELS 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) 
# --- TÍCH HỢP QUESTION GENERATOR ---
try:
    from data.questions import (
        get_level_1_questions, get_level_2_questions, get_level_3_questions,
        get_level_4_questions, get_level_5_questions, get_level_6_questions
    )
    # Mapping các hàm tạo câu hỏi theo KEY của level
    QUESTION_GENERATORS = {
        "LEVEL_1": get_level_1_questions,
        "LEVEL_2": get_level_2_questions,
        "LEVEL_3": get_level_3_questions,
        "LEVEL_4": get_level_4_questions,
        "LEVEL_5": get_level_5_questions,
        "LEVEL_6": get_level_6_questions,
    }
except ImportError as e:
    print(f"LỖI TẢI questions.py: {e}. Vui lòng đảm bảo file data/questions.py tồn tại và import đúng.")
    QUESTION_GENERATORS = {}
# ------------------------------------


class GameManager:
    sounds = _load_sound()
    def __init__(self):        
        self.screens = {
            "MENU": MenuScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self)
        }

        self.active_screen_key = "MENU"
        self.active_screen = self.screens[self.active_screen_key]
        self.current_level_key = None
        
        self.game_data = load_game_data()
        pygame.mixer.music.play(loops=-1)
        
        self.questions_pool = [] 
        self.question_index = 0 
    
    def get_level_best_score(self, level_key):
        """Lấy điểm cao nhất của level hiện tại."""
        if level_key in self.game_data and "best_score" in self.game_data[level_key]:
            return self.game_data[level_key]["best_score"]
        return 0


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
            
            if screen_key in ["MENU", "LEVEL"]:
                 pygame.mixer.music.stop()
            
        else:
            print(f"Error: Screen {screen_key} not found!")
        

    def handle_input(self, event):
        self.active_screen.handle_input(event)

    def update(self):
        self.active_screen.update()

    def draw(self, surface):
        # Sửa lỗi: Đảm bảo MenuScreen và LevelSelectScreen nhận surface
        self._current_surface = surface 
        
        if self.active_screen_key == "GAMEPLAY":
            self.active_screen.draw() # GameplayScreen.draw() không cần tham số
        else:
            self.active_screen.draw(surface) # MenuScreen/LevelSelectScreen cần tham số
        
    def calculate_stars(self, score):
        if MAX_SCORE_PER_LEVEL <= 0:
            return 0
        
        score_ratio = score / MAX_SCORE_PER_LEVEL
        
        sorted_thresholds = sorted(STAR_THRESHOLDS.items(), key=lambda item: item[0], reverse=True)
        
        for stars, threshold in sorted_thresholds:
            if score_ratio >= threshold:
                return stars
        return 0

    def save_score(self, new_score):
        if not self.current_level_key:
            return

        current_data = self.game_data.get('scores', {})
        current_stars = self.game_data.get('stars', [0] * len(LEVELS))
        
        new_stars = self.calculate_stars(new_score)
        
        level_data = current_data.get(self.current_level_key, {'high_score': 0})
        if new_score > level_data['high_score']:
            level_data['high_score'] = new_score
            current_data[self.current_level_key] = level_data
        
        try:
            level_index = next(i for i, level in enumerate(LEVELS) if level['key'] == self.current_level_key)
            if new_stars > current_stars[level_index]:
                current_stars[level_index] = new_stars
                self.game_data['stars'] = current_stars
                
        except StopIteration:
            return
            
        self.game_data['scores'] = current_data
        save_game_data(self.game_data)