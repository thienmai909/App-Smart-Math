# src/config.py
import pygame
import os
import sys

# Lấy đường dẫn thư mục hiện tại của file config.py (src/)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Đi ngược 1 cấp để về thư mục gốc của dự án
BASE_DIR = os.path.dirname(CURRENT_DIR)

# Định nghĩa thư mục assets (assets nằm cùng cấp với src/)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Màn hình
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
FPS = 120
TITLE = "Smart Math"

# Màu sắc
COLOR_BG = (0, 0, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_ACCENT = (255, 200, 0)
COLOR_CORRECT = (50, 200, 50)
GREEN = COLOR_CORRECT
COLOR_WRONG = (200, 50, 50)
COLOR_WHITE = (255, 255, 255)

# Định nghĩa YELLOW và BLUE để LevelSelectScreen có thể import
YELLOW = (255, 255, 0)     
BLUE = (30, 144, 255)      

# Cài đặt
POINTS_CORRECT = 5
POINTS_WRONG = -2
TIME_LIMIT = 30

# Font size
FONT_SIZE_TITLE = 72
FONT_SIZE_LARGE = 48
FONT_SIZE_SMALL = 30
FONT_SIZE_MEDIUM = 40