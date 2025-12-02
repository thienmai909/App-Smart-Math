# config.py
import os

# --- THÔNG SỐ MÀN HÌNH ---
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 120
TITLE = "Toán thông minh"

# --- ĐƯỜNG DẪN TÀI NGUYÊN (Khắc phục lỗi NameError) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'assets')
ASSETS_IMG_DIR = os.path.join(ASSETS_DIR, 'images') 
ASSETS_SND_DIR = os.path.join(ASSETS_DIR, 'sounds') 
ASSETS_FONT_DIR = os.path.join(ASSETS_DIR, 'fonts') 
MAIN_FONT = os.path.join(ASSETS_FONT_DIR, 'main_font.ttf')

# --- THÔNG SỐ GAMEPLAY & SAO ---
TIME_LIMIT = 30 
POINTS_CORRECT = 5
POINTS_WRONG = -2
MAX_QUESTIONS = 20 

MAX_SCORE_PER_LEVEL = MAX_QUESTIONS * POINTS_CORRECT 
STAR_THRESHOLDS = {
    3: 0.95, 
    2: 0.75, 
    1: 0.50, 
    0: 0.00
}

# --- MÀU SẮC ---
COLOR_BG = (255, 245, 220)      # Màu nền chính (Vàng kem Sáng) 
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT = (0, 0, 0)          # <Màu chữ chính (Đen Thuần)
COLOR_ACCENT = (255, 105, 180)  # Màu nhấn (Hồng Nóng/Rực rỡ) 
COLOR_TITLE = (128, 0, 128)     # Màu tiêu đề (Tím Hoàng Gia Đậm) 
COLOR_INFO = (255, 165, 0)      # Màu thông tin (Cam Sáng/Rực Rỡ) 
COLOR_CORRECT = (0, 128, 0)     # Màu đáp án đúng (Xanh Lá Cây Cỏ Đậm) 
COLOR_WRONG = (255, 0, 0)
# --- FONT SIZE ---
FONT_SIZE_TITLE = 80
FONT_SIZE_LARGE = 48
FONT_SIZE_MEDIUM = 36
FONT_SIZE_SMALL = 24