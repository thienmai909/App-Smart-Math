import pygame
import os
from src.screens.base_screen import BaseScreen
from src.config import *

# ĐƯỜNG DẪN MẪU ĐẾN FONT HỖ TRỢ TIẾNG VIỆT
try:
    VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')
except NameError:
    VIETNAMESE_FONT_PATH = None

class MenuScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # SỬA LỖI FONT
        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_title = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_TITLE)
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL)
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        except pygame.error:
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            
        # KHAI BÁO CÁC RECT TẠM THỜI 
        self.start_button_rect = pygame.Rect(0, 0, 1, 1) 
        # self.setting_button_rect đã bị loại bỏ 
        self.assets = self._load_assets()
        # CĂN CHỈNH VỊ TRÍ NÚT PLAY CUỐI CÙNG
        self.start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180)    
        # TÍCH HỢP TƯƠNG TÁC SETTINGS TRỰC TIẾP TẠI LEVEL SCREEN
        # Các rect này không được sử dụng để vẽ/tương tác trong màn hình Menu, nhưng được giữ lại để tránh lỗi thuộc tính nếu logic Settings được tái sử dụng.
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
            assets['nen_menu'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'giaodiendautien.png')).convert_alpha()
            assets['nen_menu'] = pygame.transform.scale(assets['nen_menu'], (SCREEN_WIDTH, SCREEN_HEIGHT))      
            assets['nutbatdau'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutbatdau.png')).convert_alpha()
            assets['nutbatdau'] = pygame.transform.scale(assets['nutbatdau'], (250, 60)) 
            self.start_button_rect.size = assets['nutbatdau'].get_size() 
            # TẢI HÌNH ẢNH SETTINGS ĐỂ TRÁNH LỖI KHI TRUY CẬP TRONG __init__
            assets['nut_caidat'] = pygame.Surface((50, 50), pygame.SRCALPHA) # Chỉ cần dummy surface
            assets['nen_caidat'] = pygame.Surface((400, 450)); assets['nen_caidat'].fill((200, 150, 150))
            assets['on'] = pygame.Surface((50, 30)); assets['on'].fill(COLOR_CORRECT)
            assets['off'] = pygame.Surface((50, 30)); assets['off'].fill(COLOR_WRONG)

            # --- TẢI ÂM THANH MỚI THÊM VÀO ---
            assets['sound'] = {}
            assets['sound']['bgm'] = os.path.join(ASSETS_SOUND_DIR, 'nhacnen.mp3') 
            try:
                assets['sound']['click'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, 'click_dapan.wav')) 
            except pygame.error as e:
                print(f"Lỗi tải âm thanh hiệu ứng: {e}. Âm thanh sẽ không được phát.")
                assets['sound']['click'] = None
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh Menu: {e}. Vui lòng kiểm tra file ảnh.")
            assets['nen_menu'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_menu'].fill(COLOR_BG)
            assets['nutbatdau'] = pygame.Surface((250, 60)); assets['nutbatdau'].fill(COLOR_CORRECT)
            assets['nut_caidat'] = pygame.Surface((50, 50)); assets['nut_caidat'].fill(COLOR_ACCENT)
            assets['nen_caidat'] = pygame.Surface((400, 450)); assets['nen_caidat'].fill((200, 150, 150))
            assets['on'] = pygame.Surface((50, 30)); assets['on'].fill(COLOR_CORRECT)
            assets['off'] = pygame.Surface((50, 30)); assets['off'].fill(COLOR_WRONG)
            
            # FALLBACK CHO SOUND
            assets['sound'] = {'bgm': None, 'click': None}
            
        return assets

    def on_enter(self):
        """Khởi động nhạc nền khi màn hình menu được kích hoạt."""
        if self.bgm_on and 'bgm' in self.assets['sound'] and self.assets['sound']['bgm']:
            try:
                pygame.mixer.music.load(self.assets['sound']['bgm'])
                pygame.mixer.music.play(-1) # Phát lặp lại
            except pygame.error as e:
                print(f"Lỗi phát nhạc nền: {e}")

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.start_button_rect.collidepoint(mouse_pos):
                # Phát âm thanh click
                if self.assets['sound']['click'] and self.sound_on:
                    self.assets['sound']['click'].play()
                
                # Dừng nhạc nền khi chuyển màn hình
                pygame.mixer.music.stop() 
                self.game_manager.switch_screen("LEVEL") 

    def update(self):
        pass

    def _draw_settings_popup(self, surface):
        pass

    def draw(self):
        surface = self.game_manager._current_surface
        if surface is None:
            return
        surface.blit(self.assets['nen_menu'], (0, 0))
        surface.blit(self.assets['nutbatdau'], self.start_button_rect.topleft)