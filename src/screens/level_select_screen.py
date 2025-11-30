# src/screens/level_select_screen.py
import pygame
import os
from src.screens.base_screen import BaseScreen
# Đảm bảo tất cả các hằng số, bao gồm ASSETS_IMG_DIR, được import
from src.config import * # Cấu hình các cấp độ
LEVELS = [
    {"name": "Level 1: Cộng/Trừ (1-20)", "key": "LEVEL_1", "color": COLOR_CORRECT},
    {"name": "Level 2: Nhân/Chia (2-9)", "key": "LEVEL_2", "color": COLOR_ACCENT},
    {"name": "Level 3: Hỗn hợp có ngoặc", "key": "LEVEL_3", "color": COLOR_INFO}, 
    {"name": "Level 4: Tìm X cơ bản", "key": "LEVEL_4", "color": COLOR_TEXT},
    {"name": "Level 5: Phân số cơ bản", "key": "LEVEL_5", "color": COLOR_WRONG},
    {"name": "Level 6: Tìm X nâng cao", "key": "LEVEL_6", "color": COLOR_TITLE},
]

class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        try:
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        except pygame.error:
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            
        self.level_rects = []
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        # Lỗi xảy ra khi gọi _load_assets, cần đảm bảo nó sử dụng ASSETS_IMG_DIR
        self.assets = self._load_assets()
        
    def _load_assets(self):
        assets = {}
        try:
            # Sửa lỗi NameError: Sử dụng ASSETS_IMG_DIR
            nen_lv_path = os.path.join(ASSETS_IMG_DIR, 'nen_lv.png')
            assets['nen_lv'] = pygame.image.load(nen_lv_path).convert()
            assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Sửa lỗi NameError: Sử dụng ASSETS_IMG_DIR
            nut_back_path = os.path.join(ASSETS_IMG_DIR, 'nut_back.png')
            assets['nut_back'] = pygame.image.load(nut_back_path).convert_alpha()
            self.back_button_rect.size = assets['nut_back'].get_size()
            
            # Tải ảnh sao
            assets['sao'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha()
            assets['sao'] = pygame.transform.scale(assets['sao'], (30, 30))
            
        except pygame.error as e:
            print(f"!!! LỖI TẢI HÌNH ẢNH LEVEL: {e}. Kiểm tra ASSETS_IMG_DIR và file ảnh.")
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['nen_lv'].fill(COLOR_BG)
            assets['nut_back'] = pygame.Surface((100, 40), pygame.SRCALPHA)
            assets['nut_back'].fill(COLOR_WRONG)
            assets['sao'] = None
            
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
                    self.game_manager.current_level_key = selected_level['key']
                    self.game_manager.switch_screen("GAMEPLAY")
                    return

    def update(self):
        pass

    def draw(self, surface):
        self.level_rects = []
        
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        title_text = self.font_large.render("CHỌN CẤP ĐỘ", True, COLOR_TITLE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)
        
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        start_y = 150 
        spacing = 70 
        
        highscores = self.game_manager.game_data.get('highscores', [0]*6) 
        stars_data = self.game_manager.game_data.get('stars', [0]*6)
        
        star_asset = self.assets.get('sao', None)
        star_width = 30 
        
        for i, level in enumerate(LEVELS):
            y_pos = start_y + i * spacing
            button_width, button_height = 500, 60
            
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (SCREEN_WIDTH // 2, y_pos)
            self.level_rects.append(button_rect)
            
            button_color = level["color"]
            pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
            pygame.draw.rect(surface, COLOR_TEXT, button_rect, 3, border_radius=10)

            name_text = self.font_small.render(level["name"], True, COLOR_BLACK)
            name_text_rect = name_text.get_rect(midleft=(button_rect.x + 20, y_pos))
            surface.blit(name_text, name_text_rect)
            
            score = highscores[i] if i < len(highscores) else 0
            score_text = self.font_small.render(f"ĐIỂM CAO: {score}", True, COLOR_BLACK)
            
            score_text_x = button_rect.right - 10 - 3 * star_width
            score_text_rect = score_text.get_rect(midright=(score_text_x, y_pos))
            surface.blit(score_text, score_text_rect)
            
            num_stars = stars_data[i] if i < len(stars_data) else 0
            
            for s in range(3):
                star_x = button_rect.right - 10 - (3 - s) * star_width + 5
                star_y = y_pos - star_width // 2
                
                if s < num_stars and star_asset:
                    surface.blit(star_asset, (star_x, star_y))
                else:
                    pygame.draw.circle(surface, (100, 100, 100), (star_x + 15, y_pos), 10, 1)