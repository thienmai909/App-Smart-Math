import pygame
from src.screens.base_screen import BaseScreen
from src.config import *

try:
    VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'Nunito-ExtraBold.ttf')
except NameError:
    VIETNAMESE_FONT_PATH = None

class MenuScreen(BaseScreen):
    

    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.show_settings = False
        self.sound_setting = True
        self.bgm_setting = True

        self.assets = self._load_assets()

        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL)
            else:
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        except pygame.error:
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)

        self.settings_rect = self.assets['nen_caidat'].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.close_rect = pygame.Rect(self.settings_rect.right - 40, self.settings_rect.y + 10, 30, 30)
        self.sound_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 120, 300, 50)
        self.bgm_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 190, 300, 50)
        self.home_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 280, 300, 50)
        self.replay_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 360, 300, 50)

    def _load_assets(self):
        assets = {}
        try:          
            # Tải các assets settings
            assets['nen_caidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'anvao_caidat.png')).convert_alpha()
            assets['nen_caidat'] = pygame.transform.scale(assets['nen_caidat'], (400, 450)) 
            assets['on'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'on.png')).convert_alpha(), (50, 30))
            assets['off'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'off.png')).convert_alpha(), (50, 30))

           #  --- TẢI ẢNH CHO NÚT HOME/REPLAY (Pop-up Settings) ---
            try:
                # SỬ DỤNG nut_back.png cho nút HOME (BACK)
                assets['nut_back_icon'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
                assets['nut_back_icon'] = pygame.transform.scale(assets['nut_back_icon'], ACTION_BUTTON_SIZE)
            except pygame.error:
                # Giả định COLOR_ACCENT được định nghĩa trong src.config
                assets['nut_back_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_back_icon'].fill(COLOR_ACCENT)

            try:
                # SỬ DỤNG nutbatdau.png cho nút REPLAY (PLAY)
                assets['nut_play_icon'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_play.png')).convert_alpha()
                assets['nut_play_icon'] = pygame.transform.scale(assets['nut_play_icon'], ACTION_BUTTON_SIZE)
            except pygame.error:
                assets['nut_play_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_play_icon'].fill(COLOR_CORRECT)
        
        except pygame.error as e:
            print(f"!!! LỖI TẢI HÌNH ẢNH CỐ ĐỊNH: {e}. Kiểm tra ASSETS_IMG_DIR.")
            # Khởi tạo surface thay thế
            assets['on'] = pygame.Surface((50, 30)); assets['on'].fill(COLOR_CORRECT)
            assets['off'] = pygame.Surface((50, 30)); assets['off'].fill(COLOR_WRONG)
            assets['nut_back_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_back_icon'].fill(COLOR_ACCENT)
            assets['nut_play_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_play_icon'].fill(COLOR_CORRECT)
            
        return assets

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Đóng menu
            if self.close_rect.collidepoint(mouse_pos):
                self.show_settings = False
                return
            
            # Logic click bên trong pop-up
            if self.sound_rect.collidepoint(mouse_pos):
                self.sound_setting = not self.sound_setting

                # Thêm logic điều khiển âm thanh game_manager tại đây
            elif self.bgm_rect.collidepoint(mouse_pos):
                self.bgm_setting = not self.bgm_setting

                # Thêm logic điều khiển nhạc nền game_manager tại đây
            elif self.home_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("HOME")
                self.show_settings = False
                if self.game_manager.active_screen_key == "GAMEPLAY":
                    self.game_manager.screens[self.game_manager.active_screen_key].reset_game()

            elif self.replay_rect.collidepoint(mouse_pos):
                # Hiện tại đang chuyển về MENU
                self.show_settings = False
                if self.game_manager.active_screen_key == "GAMEPLAY":
                    self.game_manager.question_index = 0
                    self.game_manager.screens[self.game_manager.active_screen_key].reset_game()
                    self.game_manager.screens[self.game_manager.active_screen_key].load_next_question() 
                else:
                    self.game_manager.switch_screen("HOME") 
                
            return

    def update(self):
        # Âm thanh nhạc nền setting
        if self.bgm_setting:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        # Âm thanh click
        if self.sound_setting:
            self.game_manager.sounds['click'].set_volume(1.0)
        else:
            self.game_manager.sounds['click'].set_volume(0.0)



    def draw(self, surface):
        """Vẽ pop-up cài đặt lên trên màn hình.""" 
        # Giả lập overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        surface.blit(overlay, (0, 0))   
        
        # Vẽ nền pop-up
        surface.blit(self.assets['nen_caidat'], self.settings_rect.topleft)
        
        # --- VẼ CÁC THÔNG TIN/NÚT BÊN TRONG POPUP ---

        sound_icon = self.assets['on'] if self.sound_setting else self.assets['off']
        sound_icon_rect = sound_icon.get_rect(midright=(self.settings_rect.right - 40, self.sound_rect.centery))
        surface.blit(sound_icon, sound_icon_rect.topleft)


        bgm_icon = self.assets['on'] if self.bgm_setting else self.assets['off']
        bgm_icon_rect = bgm_icon.get_rect(midright=(self.settings_rect.right - 40, self.bgm_rect.centery))
        surface.blit(bgm_icon, bgm_icon_rect.topleft)

        if 'nut_back_icon' in self.assets:
            icon_asset = self.assets['nut_back_icon']
            icon_rect = icon_asset.get_rect(midright=(self.home_rect.right -0, self.home_rect.centery))
            surface.blit(icon_asset, icon_rect.topleft)

        if 'nut_play_icon' in self.assets:
            icon_asset = self.assets['nut_play_icon']
            icon_rect = icon_asset.get_rect(midright=(self.replay_rect.right -0, self.replay_rect.centery))
            surface.blit(icon_asset, icon_rect.topleft)

        # Nút đóng pop-up (X)
        pygame.draw.circle(surface, COLOR_WRONG, self.close_rect.center, 15)
        close_text = self.font_small.render("X", True, COLOR_WHITE)
        close_text_rect = close_text.get_rect(center=self.close_rect.center)
        surface.blit(close_text, close_text_rect)