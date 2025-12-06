import pygame
import os
from src.screens.base_screen import BaseScreen
from src.config import *

class HomeScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        # KHAI BÁO CÁC RECT TẠM THỜI 
        self.start_button_rect = pygame.Rect(0, 0, 1, 1) 
        self.assets = self._load_assets()

        # CĂN CHỈNH VỊ TRÍ NÚT PLAY CUỐI CÙNG
        self.start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180)   
        
    def _load_assets(self):
        assets = {}
        try:
            assets['nen_home'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'giaodiendautien.png')).convert_alpha()
            assets['nen_home'] = pygame.transform.scale(assets['nen_home'], (SCREEN_WIDTH, SCREEN_HEIGHT))     
            assets['nutbatdau'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutbatdau.png')).convert_alpha()
            assets['nutbatdau'] = pygame.transform.scale(assets['nutbatdau'], (250, 50)) 
            self.start_button_rect.size = assets['nutbatdau'].get_size() 
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh Home: {e}. Vui lòng kiểm tra file ảnh.")
            assets['nen_home'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_home'].fill(COLOR_BG)
            assets['nutbatdau'] = pygame.Surface((250, 50)); assets['nutbatdau'].fill(COLOR_CORRECT)
            
        return assets

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if self.start_button_rect.collidepoint(mouse_pos):
                self.game_manager.sounds['click'].play()
                self.game_manager.switch_screen("LEVEL") 

    def update(self):
        pass

    def draw(self, surface):
        if surface is None:
            return
        surface.blit(self.assets['nen_home'], (0, 0))
        surface.blit(self.assets['nutbatdau'], self.start_button_rect.topleft)
        
