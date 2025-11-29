# src/screens/level_select_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *
import os

# --- CẤU HÌNH CÁC CẤP ĐỘ (LEVELS) ---
LEVELS = [
    {"name": "DỄ (Cộng/Trừ)", "key": "EASY", "color": GREEN, "description": "Thực hiện phép cộng và trừ cơ bản."},
    {"name": "TRUNG BÌNH (Nhân/Chia)", "key": "MEDIUM", "color": YELLOW, "description": "Thực hiện phép nhân và chia."},
    {"name": "KHÓ (Hỗn hợp)", "key": "HARD", "color": BLUE, "description": "Kết hợp tất cả các phép toán."},
]

class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # SỬA LỖI FONT: Pygame Font có thể gây lỗi nếu không tìm thấy font hệ thống
        try:
            # Ưu tiên sử dụng font hệ thống mặc định (None)
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        except pygame.error as e:
            print(f"Lỗi Font: {e}")
            # Dùng font cơ bản nhất
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            
        self.level_rects = []
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        
        self.assets = self._load_assets()
        
    def _load_assets(self):
        assets = {}
        try:
            # Tải ảnh nền
            nen_lv_path = os.path.join(ASSETS_DIR, 'nen_lv.png')
            assets['nen_lv'] = pygame.image.load(nen_lv_path).convert()
            assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Tải nút back
            nut_back_path = os.path.join(ASSETS_DIR, 'nut_back.png')
            assets['nut_back'] = pygame.image.load(nut_back_path).convert_alpha()
            self.back_button_rect.size = assets['nut_back'].get_size()
            
            print(f"DEBUG: Tải thành công ảnh từ {ASSETS_DIR}")
            
        except pygame.error as e:
            # Nếu xảy ra lỗi pygame.error (ví dụ: file bị hỏng), in ra thông báo chi tiết
            print(f"!!! LỖI TẢI HÌNH ẢNH (Pygame Error): {e}")
            print(">>> HÃY KIỂM TRA LẠI: File nen_lv.png và nut_back.png có bị hỏng không?")
            
            # Sử dụng các Surface màu làm fallback
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['nen_lv'].fill(COLOR_BG)
            
            assets['nut_back'] = pygame.Surface((100, 40), pygame.SRCALPHA)
            assets['nut_back'].fill(COLOR_WRONG)
            
        return assets
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("MENU")
                return
            
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(mouse_pos):
                    selected_level = LEVELS[i]
                    print(f"Bắt đầu chơi cấp độ: {selected_level['key']} - {selected_level['name']}")
                    self.game_manager.current_level_key = selected_level['key']
                    self.game_manager.switch_screen("GAMEPLAY")
                    return

    def update(self):
        pass

    def draw(self, surface):
        self.level_rects = []
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        title_text = self.font_large.render("CHỌN CẤP ĐỘ", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)
        
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        start_y = SCREEN_HEIGHT // 3 
        spacing = 100
        
        for i, level in enumerate(LEVELS):
            y_pos = start_y + i * spacing
            button_width, button_height = 500, 70
            
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (SCREEN_WIDTH // 2, y_pos)
            self.level_rects.append(button_rect)
            
            button_color = level["color"]
            pygame.draw.rect(surface, button_color, button_rect, border_radius=15)
            pygame.draw.rect(surface, COLOR_ACCENT, button_rect, 5, border_radius=15)

            name_text = self.font_small.render(level["name"], True, COLOR_WHITE)
            name_text_rect = name_text.get_rect(center=button_rect.center)
            surface.blit(name_text, name_text_rect)