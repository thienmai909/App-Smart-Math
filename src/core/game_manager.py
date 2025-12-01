# src/core/game_manager.py
import pygame
import os
import sys 
from src.screens.menu_screen import MenuScreen
from src.screens.level_select_screen import LevelSelectScreen
from src.screens.gameplay_screen import GameplayScreen
# Import các hàm tạo câu hỏi từ data/questions.py
from data.questions import get_level_1_questions, get_level_2_questions, get_level_3_questions, get_level_4_questions, get_level_5_questions, get_level_6_questions
# Import các hàm lưu/tải từ data/save_manager.py
from data.save_manager import load_game_data, save_game_data 
from src.screens.level_select_screen import LEVELS 
from src.config import POINTS_CORRECT, MAX_QUESTIONS, STAR_THRESHOLDS

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
        self._current_surface = None 
        self.sound_assets = self._load_sound_assets()
        
        # PHẢI KHAI BÁO CÁC THUỘC TÍNH NÀY TRƯỚC KHI KHỞI TẠO CÁC MÀN HÌNH
        # để tránh lỗi "AttributeError: 'GameManager' object has no attribute 'question_index'"
        self.current_screen_name = "MENU" 
        self.current_level_key = None 
        self.questions_pool = [] 
        self.question_index = 0 
        
        # Khởi tạo tất cả các màn hình
        self.screens = {
            "MENU": MenuScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self),
        }
        
        # Tải dữ liệu điểm và sao
        self.game_data = load_game_data()
        
        if 'stars' not in self.game_data:
            self.game_data['stars'] = [0] * len(LEVELS)
        if 'highscores' not in self.game_data:
            self.game_data['highscores'] = [0] * len(LEVELS)


    def _load_sound_assets(self):
        assets = {}
        # Tìm đường dẫn tuyệt đối cho thư mục assets/sounds
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        sound_dir = os.path.join(project_root, 'assets', 'sounds')
        
        try:
            pygame.mixer.init()
            # Khắc phục lỗi nếu không tìm thấy file âm thanh
            if os.path.exists(os.path.join(sound_dir, 'click_dapan.wav')):
                assets['click_dapan'] = pygame.mixer.Sound(os.path.join(sound_dir, 'click_dapan.wav'))
            if os.path.exists(os.path.join(sound_dir, 'correct.mp3')):
                assets['correct'] = pygame.mixer.Sound(os.path.join(sound_dir, 'correct.mp3'))
            if os.path.exists(os.path.join(sound_dir, 'no.mp3')):
                assets['wrong'] = pygame.mixer.Sound(os.path.join(sound_dir, 'no.mp3'))
        except Exception as e:
            print(f"Cảnh báo: Lỗi tải âm thanh: {e}")
            assets = {}
        return assets
    
    def calculate_stars(self, final_score):
        """Tính toán số sao dựa trên điểm số cuối cùng và ngưỡng từ config."""
        max_score = MAX_QUESTIONS * POINTS_CORRECT
        
        # Ngăn chia cho 0 nếu MAX_QUESTIONS = 0
        if max_score == 0:
            return 0

        score_ratio = final_score / max_score
            
        if score_ratio >= STAR_THRESHOLDS[3]: 
            return 3
        elif score_ratio >= STAR_THRESHOLDS[2]: 
            return 2
        elif score_ratio >= STAR_THRESHOLDS[1]: 
            return 1
        else:
            return 0

    def switch_screen(self, new_screen_name):
        self.current_screen_name = new_screen_name
        
        if new_screen_name == "GAMEPLAY":
            if self.current_level_key and self.current_level_key in QUESTION_FUNCTIONS:
                # Nạp câu hỏi từ data/questions.py
                self.questions_pool = QUESTION_FUNCTIONS[self.current_level_key](num_questions=MAX_QUESTIONS)
                self.question_index = 0
                self.screens["GAMEPLAY"].reset_game()
                # BẮT BUỘC gọi load_next_question() sau khi nạp pool
                self.screens["GAMEPLAY"].load_next_question() 
            else:
                print("LỖI: Level không hợp lệ hoặc chưa chọn. Chuyển về Level Select.")
                self.current_screen_name = "LEVEL" 

    def handle_input(self, event):
        self.screens[self.current_screen_name].handle_input(event)

    def update(self):
        self.screens[self.current_screen_name].update()

    def draw(self, surface):
        self._current_surface = surface 
        self.screens[self.current_screen_name].draw()

    def save_score(self, score):
        if self.current_level_key:
            try:
                # Trích xuất index từ key ví dụ: "LEVEL_1" -> 0
                level_index = int(self.current_level_key.split('_')[1]) - 1
                num_stars = self.calculate_stars(score)
                
                if level_index < len(self.game_data['highscores']):
                    data_changed = False
                    
                    # Cập nhật Highscore nếu điểm mới cao hơn
                    if score > self.game_data['highscores'][level_index]:
                        self.game_data['highscores'][level_index] = score
                        data_changed = True
                        
                    # Cập nhật Stars nếu số sao mới nhiều hơn
                    if num_stars > self.game_data['stars'][level_index]:
                        self.game_data['stars'][level_index] = num_stars
                        data_changed = True
                        
                    if data_changed:
                        save_game_data(self.game_data)
                    
            except Exception as e:
                print(f"Lỗi khi lưu điểm: {e}")