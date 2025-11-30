# src/screens/level_select_screen.py
import pygame
import os
from src.screens.base_screen import BaseScreen
from src.config import * 
LEVELS = [
    {"name": "Level 1: Cộng/Trừ (1-20)", "key": "LEVEL_1", "color": COLOR_CORRECT},
    {"name": "Level 2: Nhân/Chia (2-9)", "key": "LEVEL_2", "color": COLOR_ACCENT},
    {"name": "Level 3: Hỗn hợp có ngoặc", "key": "LEVEL_3", "color": COLOR_INFO}, 
    {"name": "Level 4: Tìm X cơ bản", "key": "LEVEL_4", "color": COLOR_TEXT},
    {"name": "Level 5: Phân số cơ bản", "key": "LEVEL_5", "color": COLOR_WRONG},
    {"name": "Level 6: Tìm X nâng cao", "key": "LEVEL_6", "color": COLOR_TITLE},
]

# ĐƯỜNG DẪN MẪU ĐẾN FONT HỖ TRỢ TIẾNG VIỆT
try:
    VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')
except NameError:
    VIETNAMESE_FONT_PATH = None

class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # SỬA LỖI FONT
        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_title = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_TITLE) 
                self.font_large = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_LARGE)
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL)
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        except pygame.error:
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            
        self.level_rects = []
        self.back_button_rect = pygame.Rect(20, 20, 100, 40)
        self.assets = self._load_assets()
        
    def _load_assets(self):
        assets = {}
        try:
            assets['nen_lv'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_lv.png')).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['nut_back'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha(), (150, 60))
            self.back_button_rect.size = assets['nut_back'].get_size()
            self.back_button_rect.topleft = (20, 20)
            assets['sao'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha(), (25, 25))
            assets['khoalv'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'khoalv.png')).convert_alpha(), (60, 60))

        except pygame.error as e:
            print(f"!!! LỖI TẢI HÌNH ẢNH LEVEL: {e}. Kiểm tra ASSETS_IMG_DIR và file ảnh.")
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_lv'].fill(COLOR_BG)
            assets['nut_back'] = pygame.Surface((150, 60), pygame.SRCALPHA); assets['nut_back'].fill(COLOR_WRONG)
            assets['sao'] = None
            assets['khoalv'] = pygame.Surface((60, 60), pygame.SRCALPHA); assets['khoalv'].fill((100, 100, 100))
            
        return assets
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("MENU")
                return
            
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(mouse_pos):
                    # Lấy dữ liệu sao để kiểm tra khóa
                    stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS)) 
                    is_locked = (i > 0 and stars_data[i-1] == 0)
                    if not is_locked:
                        selected_level = LEVELS[i]
                        self.game_manager.current_level_key = selected_level['key']
                        self.game_manager.switch_screen("GAMEPLAY")
                        return

    def update(self):
        pass

    def draw(self):
        surface = self.game_manager._current_surface
        if surface is None:
            return
            
        self.level_rects = []
        
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        title_text = self.font_title.render("CHỌN CẤP ĐỘ", True, COLOR_TITLE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)
        
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        start_y = 180 
        spacing = 80 
        
        # Củng cố: Luôn lấy highscores và stars từ game_data, với giá trị mặc định 0
        highscores = self.game_manager.game_data.get('highscores', [0] * len(LEVELS)) 
        stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS))
        
        star_asset = self.assets.get('sao', None)
        khoa_asset = self.assets.get('khoalv', None) 
        star_width = 25 
        
        for i, level in enumerate(LEVELS):
            y_pos = start_y + i * spacing
            button_width, button_height = 600, 70
            
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (SCREEN_WIDTH // 2, y_pos)
            self.level_rects.append(button_rect)
            
            # Logic khóa: Level i bị khóa nếu Level i-1 có 0 sao
            is_locked = (i > 0 and stars_data[i-1] == 0) 
            
            button_color = level["color"]
            if is_locked:
                button_color = (150, 150, 150)
            
            pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
            pygame.draw.rect(surface, COLOR_TEXT, button_rect, 3, border_radius=10)

            name_text = self.font_small.render(level["name"], True, COLOR_BLACK)
            name_text_rect = name_text.get_rect(midleft=(button_rect.x + 30, y_pos)) 
            surface.blit(name_text, name_text_rect)
            
            if is_locked and khoa_asset:
                khoa_rect = khoa_asset.get_rect(midleft=(button_rect.x + 250, y_pos))
                surface.blit(khoa_asset, khoa_rect)
                
                overlay_lock = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                overlay_lock.fill((255, 255, 255, 150)) 
                surface.blit(overlay_lock, button_rect.topleft)
                
            else:
                score = highscores[i] if i < len(highscores) else 0
                score_text = self.font_small.render(f"ĐIỂM CAO: {score}", True, COLOR_BLACK)
                
                score_text_x = button_rect.right - 10 - 4 * star_width
                score_text_rect = score_text.get_rect(midright=(score_text_x, y_pos))
                surface.blit(score_text, score_text_rect)
                
                num_stars = stars_data[i] if i < len(stars_data) else 0 
                star_start_x = button_rect.right - 10 - 3 * star_width 
                
                # VẼ SAO VÀ OUTLINE SAO
                for s in range(3):
                    star_x = star_start_x + s * star_width
                    star_y = y_pos - star_width // 2
                    
                    if s < num_stars and star_asset:
                        surface.blit(star_asset, (star_x, star_y))
                    else:
                        # Vẽ outline (vòng tròn) cho sao chưa đạt
                        pygame.draw.circle(surface, (100, 100, 100), (star_x + star_width // 2, y_pos), 10, 1)