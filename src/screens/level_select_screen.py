# src/screens/level_select_screen.py
import pygame
import os
from src.screens.base_screen import BaseScreen
from src.config import *
# Cấu trúc LEVELS mới với image_key
LEVELS = [
    {"name": "LEVEL 1", "key": "LEVEL_1", "image_key": "molv1"},
    {"name": "LEVEL 2", "key": "LEVEL_2", "image_key": "lv2"},
    {"name": "LEVEL 3", "key": "LEVEL_3", "image_key": "lv3"},
    {"name": "LEVEL 4", "key": "LEVEL_4", "image_key": "lv4"},
    {"name": "LEVEL 5", "key": "LEVEL_5", "image_key": "lv5"},
    {"name": "LEVEL 6", "key": "LEVEL_6", "image_key": "lv6"},
]

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

        self.setting_button_rect = pygame.Rect(0, 0, 1, 1)       
        self.assets = self._load_assets()
        
        # Khởi tạo rect cho tiêu đề "LEVEL"
        self.level_title_text_surface = self.font_title.render("LEVEL", True, (255, 204, 0))
        self.level_title_rect = self.assets['level_title_bg'].get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Rect cho thanh progress bar 
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
            
            assets['khoalv'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'khoalv.png')).convert_alpha(), (130, 130))
            
            # TẢI NÚT CÀI ĐẶT
            assets['nut_caidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha()
            assets['nut_caidat'] = pygame.transform.scale(assets['nut_caidat'], (50, 50))
            self.setting_button_rect.size = assets['nut_caidat'].get_size()
            self.setting_button_rect.topright = (SCREEN_WIDTH - 20, 20) 
            
            # TẢI LEVEL TITLE BG VÀ PROGRESS BAR 
            assets['level_title_bg'] = pygame.Surface((500, 100), pygame.SRCALPHA); assets['level_title_bg'].fill((255, 255, 255, 200))
            assets['progress_fill'] = pygame.Surface((1, 1), pygame.SRCALPHA); assets['progress_fill'].fill(COLOR_CORRECT)
            
            # Tải hình ảnh cho nút level 
            for level_data in LEVELS:
                image_key = level_data['image_key']
                path = os.path.join(ASSETS_IMG_DIR, f'{image_key}.png')
                if os.path.exists(path):
                    assets[image_key] = pygame.transform.scale(pygame.image.load(path).convert_alpha(), (170, 90))
                else:
                    surface = pygame.Surface((170, 90), pygame.SRCALPHA)
                    surface.fill((200, 100, 100, 200)) 
                    assets[image_key] = surface

                #Tai anh ngoi sao
                star_path = os.path.join(ASSETS_IMG_DIR, 'sao.png')
                if os.path.exists(star_path):
                    assets['star_icon'] = pygame.transform.scale(pygame.image.load(star_path).convert_alpha(), (20, 20))
                else:
                    assets['star_icon'] = pygame.Surface((20, 20), pygame.SRCALPHA); assets['star_icon'].fill((255, 255, 0, 200))
            
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
                    # Lấy dữ liệu sao để kiểm tra khóa
                    stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS)) 
                    
                    # KIỂM TRA LOGIC KHÓA:
                    is_locked = (i > 0 and stars_data[i-1] == 0)       
                    if not is_locked:
                        selected_level = LEVELS[i]
                        self.game_manager.current_level_key = selected_level['key']
                        self.game_manager.switch_screen("GAMEPLAY")
                        return
                    else:
                        print("Level đang bị khóa!") 
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
        
        # VẼ NỀN LEVEL
        surface.blit(self.assets['nen_lv'], (0, 0))

        # VẼ NÚT CÀI ĐẶT 
        surface.blit(self.assets['nut_caidat'], self.setting_button_rect.topleft)

        # VẼ CÁC NÚT LEVEL
        level_button_width = 170
        level_button_height = 90
        padding_x = 30
        padding_y = 30
        star_spacing = 4

        # Tính toán vị trí bắt đầu để căn giữa các nút level 
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
            # Vẽ hình ảnh nút level
            level_image = self.assets.get(level['image_key'])
            if level_image:
                # Nếu không bị khóa, vẽ level bình thường
                surface.blit(level_image, button_rect.topleft)
                
        # --- VẼ VÒNG LẶP HÌNH ẢNH SAO ---
                current_stars = stars_data[i]
                star_asset = self.assets.get('star_icon')
                if current_stars > 0 and star_asset:
                    star_size = star_asset.get_width()
                    # Tính toán tổng chiều rộng của tất cả sao để căn giữa
                    total_stars_width = (current_stars * star_size) + ((current_stars - 1) * star_spacing)
                    # Vị trí X bắt đầu để căn giữa toàn bộ khối sao
                    start_star_x = button_rect.centerx - (total_stars_width // 2)
                    star_y = button_rect.bottom - star_size - 5 # Đặt sao cách đáy nút 5px
                    for star_index in range(current_stars):
                        star_x = start_star_x + star_index * (star_size + star_spacing)
                        surface.blit(star_asset, (star_x, star_y))
            
            # Vẽ khóa nếu level bị khóa
            if is_locked and self.assets.get('khoalv'):
                khoa_asset = self.assets['khoalv']
                khoa_rect = khoa_asset.get_rect()
                khoa_rect.topleft = (button_rect.left, button_rect.top)
                surface.blit(khoa_asset, khoa_rect.topleft)
  
        #  VẼ POP-UP CÀI ĐẶT nếu show_settings = True
        if self.show_settings:
            self._draw_settings_popup(surface)