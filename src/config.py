# config.py
import os

# --- THÔNG SỐ MÀN HÌNH ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "QUIZ GAME MASTER"

# --- ĐƯỜNG DẪN TÀI NGUYÊN (Khắc phục lỗi NameError) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'assets')
ASSETS_IMG_DIR = os.path.join(ASSETS_DIR, 'images') 
ASSETS_SND_DIR = os.path.join(ASSETS_DIR, 'sounds') 
ASSETS_FONT_DIR = os.path.join(ASSETS_DIR, 'fonts') 
MAIN_FONT = os.path.join(ASSETS_FONT_DIR, 'main_font.ttf')

# --- THÔNG SỐ GAMEPLAY & SAO ---
TIME_LIMIT = 30 
POINTS_CORRECT = 100
POINTS_WRONG = -50 
MAX_QUESTIONS = 20 

MAX_SCORE_PER_LEVEL = MAX_QUESTIONS * POINTS_CORRECT 
STAR_THRESHOLDS = {
    3: 0.95, 
    2: 0.75, 
    1: 0.50, 
    0: 0.00
}

# --- MÀU SẮC ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BG = (28, 28, 28) 
COLOR_TEXT = (255, 240, 200) 
COLOR_TITLE = (255, 180, 0) 
COLOR_ACCENT = (0, 150, 255) 
COLOR_CORRECT = (0, 200, 0) 
COLOR_WRONG = (255, 50, 50) 
COLOR_INFO = (255, 120, 0) 

# --- FONT SIZE ---
FONT_SIZE_TITLE = 80
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24