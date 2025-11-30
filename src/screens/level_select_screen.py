# src/screens/level_select_screen.py
import pygame
import os
from src.screens.base_screen import BaseScreen
from src.config import *
# Cấu trúc LEVELS mới với image_key
LEVELS = [
    {"name": "LEVEL 1", "key": "LEVEL_1", "image_key": "molv1"},
    {"name": "LEVEL 2", "key": "LEVEL_2", "image_key": "molv2"},
    {"name": "LEVEL 3", "key": "LEVEL_3", "image_key": "molv3"},
    {"name": "LEVEL 4", "key": "LEVEL_4", "image_key": "molv4"},
    {"name": "LEVEL 5", "key": "LEVEL_5", "image_key": "molv5"},
    {"name": "LEVEL 6", "key": "LEVEL_6", "image_key": "molv6"},
]

# ĐƯỜNG DẪN MẪU ĐẾN FONT HỖ TRỢ TIẾNG VIỆT
try:
    VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')
except NameError:
    VIETNAMESE_FONT_PATH = None

# THÔNG SỐ PROGRESS BAR CỐ ĐỊNH
PROGRESS_BAR_WIDTH = 400
PROGRESS_BAR_HEIGHT = 40
PROGRESS_BAR_PADDING = 5

class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # SỬA LỖI FONT
        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_title = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_TITLE) 
                self.font_large = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_LARGE)
                self.font_medium = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_MEDIUM)
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL)
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        except pygame.error:
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            
        self.level_rects = []
        # LOẠI BỎ NÚT BACK (chỉ giữ lại Rect Setting)
        self.setting_button_rect = pygame.Rect(0, 0, 1, 1) 
        
        self.assets = self._load_assets() # Tải assets
        
        # Khởi tạo rect cho tiêu đề "LEVEL"
        self.level_title_text_surface = self.font_title.render("LEVEL", True, (255, 204, 0))
        # ĐIỀU CHỈNH Y CHO TOÀN BỘ KHỐI TIÊU ĐỀ XUỐNG THẤP HƠN (Ví dụ: 150)
        self.level_title_rect = self.assets['level_title_bg'].get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Rect cho thanh progress bar (Đường màu cam dưới tiêu đề)
        self.progress_bar_bg_rect = pygame.Rect(0, 0, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT)
        self.progress_bar_bg_rect.center = (SCREEN_WIDTH // 2, self.level_title_rect.bottom + 10)
        
        # --- TRẠNG THÁI VÀ RECT CÀI ĐẶT ---
        self.show_settings = False
        self.settings_rect = self.assets['nen_caidat'].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.close_rect = pygame.Rect(self.settings_rect.right - 40, self.settings_rect.y + 10, 30, 30)
        self.sound_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 120, 300, 50)
        self.bgm_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 190, 300, 50)
        self.home_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 260, 300, 50)
        self.replay_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 330, 300, 50)
        self.sound_on = True 
        self.bgm_on = True 
        
    def _load_assets(self):
        assets = {}
        try:
            assets['nen_lv'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_lv.png')).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            assets['khoalv'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'khoalv.png')).convert_alpha(), (60, 60))
            
            # TẢI NÚT CÀI ĐẶT
            assets['nut_caidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha()
            assets['nut_caidat'] = pygame.transform.scale(assets['nut_caidat'], (50, 50))
            self.setting_button_rect.size = assets['nut_caidat'].get_size()
            self.setting_button_rect.topright = (SCREEN_WIDTH - 20, 20) 
            
            # TẢI LEVEL TITLE BG VÀ PROGRESS BAR (Dùng Surface thay thế)
            assets['level_title_bg'] = pygame.Surface((500, 100), pygame.SRCALPHA); assets['level_title_bg'].fill((255, 255, 255, 200))
            assets['progress_fill'] = pygame.Surface((1, 1), pygame.SRCALPHA); assets['progress_fill'].fill(COLOR_CORRECT)
            
            # Tải hình ảnh cho nút level (molvX.png)
            for level_data in LEVELS:
                image_key = level_data['image_key']
                path = os.path.join(ASSETS_IMG_DIR, f'{image_key}.png')
                if os.path.exists(path):
                    assets[image_key] = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (200, 120))
                else:
                    surface = pygame.Surface((200, 120), pygame.SRCALPHA)
                    surface.fill((200, 100, 100, 200)) 
                    assets[image_key] = surface

            # Tải các assets settings
            assets['nen_caidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'anvao_caidat.png')).convert_alpha()
            assets['nen_caidat'] = pygame.transform.scale(assets['nen_caidat'], (400, 450)) 
            assets['on'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'on.png')).convert_alpha(), (50, 30))
            assets['off'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'off.png')).convert_alpha(), (50, 30))

        except pygame.error as e:
            print(f"!!! LỖI TẢI HÌNH ẢNH CỐ ĐỊNH: {e}. Kiểm tra ASSETS_IMG_DIR.")
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_lv'].fill(COLOR_BG)
            assets['level_title_bg'] = pygame.Surface((500, 100), pygame.SRCALPHA); assets['level_title_bg'].fill((255, 255, 255, 200))
            assets['progress_fill'] = pygame.Surface((1, 1), pygame.SRCALPHA); assets['progress_fill'].fill(COLOR_CORRECT)
            assets['nut_back'] = pygame.Surface((1, 1)); 
            assets['nen_caidat'] = pygame.Surface((400, 450)); assets['nen_caidat'].fill((200, 150, 150))
            assets['on'] = pygame.Surface((50, 30)); assets['on'].fill(COLOR_CORRECT)
            assets['off'] = pygame.Surface((50, 30)); assets['off'].fill(COLOR_WRONG)
            
            for level_data in LEVELS:
                image_key = level_data['image_key']
                surface = pygame.Surface((200, 120), pygame.SRCALPHA)
                surface.fill((200, 100, 100, 200)) 
                assets[image_key] = surface
            
        return assets
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # --- ƯU TIÊN 1: XỬ LÝ POP-UP SETTINGS NẾU ĐANG MỞ ---
            if self.show_settings:
                if self.close_rect.collidepoint(mouse_pos):
                    self.show_settings = False
                    return
                
                # Logic click bên trong pop-up
                if self.sound_rect.collidepoint(mouse_pos):
                    self.sound_on = not self.sound_on
                elif self.bgm_rect.collidepoint(mouse_pos):
                    self.bgm_on = not self.bgm_on
                elif self.home_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("MENU")
                    self.show_settings = False
                elif self.replay_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("MENU") 
                    self.show_settings = False
                return 
            
            # --- ƯU TIÊN 2: XỬ LÝ NÚT CÀI ĐẶT (MỞ POP-UP) ---
            if self.setting_button_rect.collidepoint(mouse_pos):
                self.show_settings = True 
                return
        
            # --- ƯU TIÊN 3: XỬ LÝ CÁC NÚT LEVEL ---
            for rect_data in self.level_rects:
                i = rect_data['index']
                rect = rect_data['rect']
                if rect.collidepoint(mouse_pos):
                    stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS)) 
                    is_locked = (i > 0 and stars_data[i-1] == 0)
                    if not is_locked:
                        selected_level = LEVELS[i]
                        self.game_manager.current_level_key = selected_level['key']
                        self.game_manager.switch_screen("GAMEPLAY")
                        return

    def update(self):
        if self.show_settings:
            if self.sound_on:
                pygame.mixer.set_reserved(0) 
            else:
                pygame.mixer.set_reserved(1)
            
    def _draw_settings_popup(self, surface):
        """Vẽ pop-up cài đặt lên trên màn hình."""
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        surface.blit(overlay, (0, 0))
        
        surface.blit(self.assets['nen_caidat'], self.settings_rect.topleft)
        
         # Vẽ icon ON/OFF
        sound_icon = self.assets['on'] if self.sound_on else self.assets['off']
        sound_icon_rect = sound_icon.get_rect(midright=(self.settings_rect.right - 40, self.sound_rect.centery))
        surface.blit(sound_icon, sound_icon_rect.topleft)

        bgm_icon = self.assets['on'] if self.bgm_on else self.assets['off']
        bgm_icon_rect = bgm_icon.get_rect(midright=(self.settings_rect.right - 40, self.bgm_rect.centery))
        surface.blit(bgm_icon, bgm_icon_rect.topleft)
        
        # Nút đóng pop-up
        pygame.draw.circle(surface, COLOR_WRONG, self.close_rect.center, 15)
        close_text = self.font_small.render("X", True, COLOR_WHITE)
        close_text_rect = close_text.get_rect(center=self.close_rect.center)
        surface.blit(close_text, close_text_rect)
            
    def draw(self):
        surface = self.game_manager._current_surface
        if surface is None:
            return
            
        self.level_rects = [] # Reset list rects mỗi lần vẽ
        
        # 1. VẼ NỀN LEVEL
        surface.blit(self.assets['nen_lv'], (0, 0))

        # 3. VẼ NÚT CÀI ĐẶT (VỊ TRÍ ĐÃ TỐI ƯU)
        surface.blit(self.assets['nut_caidat'], self.setting_button_rect.topleft)

        # 5. VẼ CÁC NÚT LEVEL (Bố cục lưới 3x2)
        level_button_width = 200
        level_button_height = 120
        padding_x = 30
        padding_y = 30
        
        # Tính toán vị trí bắt đầu để căn giữa các nút level (Giao diện 3x2)
        total_width_row = (level_button_width * 3) + (padding_x * 2)
        start_x = (SCREEN_WIDTH - total_width_row) // 2
        start_y = self.progress_bar_bg_rect.bottom + 50 

        stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS))

        for i, level in enumerate(LEVELS):
            row = i // 3 
            col = i % 3 
            
            x_pos = start_x + col * (level_button_width + padding_x)
            y_pos = start_y + row * (level_button_height + padding_y)


            button_rect = pygame.Rect(x_pos, y_pos, level_button_width, level_button_height)
            self.level_rects.append({'index': i, 'rect': button_rect})
            
            is_locked = (i > 0 and stars_data[i-1] == 0)
            

                
        # 7. VẼ POP-UP CÀI ĐẶT nếu show_settings = True
        if self.show_settings:
            self._draw_settings_popup(surface)