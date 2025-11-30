# src/config.py
import os

# --- THÔNG SỐ MÀN HÌNH ---
TITLE = "QUIZ GAME MASTER"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- ĐƯỜNG DẪN TÀI NGUYÊN (SỬA LỖI NAMEERROR) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_IMG_DIR = os.path.join(BASE_DIR, 'assets', 'images') # Biến sử dụng cho ảnh
ASSETS_SND_DIR = os.path.join(BASE_DIR, 'assets', 'sounds') # Biến sử dụng cho âm thanh

# --- THÔNG SỐ GAMEPLAY & SAO ---
TIME_LIMIT = 30 
POINTS_CORRECT = 100
POINTS_WRONG = -50 

MAX_SCORE_PER_LEVEL = 2000 
STAR_THRESHOLDS = {
    3: 0.90,
    2: 0.70,
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
FONT_SIZE_SMALL = 30
FONT_SIZE_MEDIUM = 36