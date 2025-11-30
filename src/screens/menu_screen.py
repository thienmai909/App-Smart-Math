# src/screens/menu_screen.py
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
            
        self.start_button_rect = pygame.Rect(0, 0, 250, 60)
        self.start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        self.setting_button_rect = pygame.Rect(0, 0, 250, 60)
        self.setting_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)


    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.start_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("LEVEL") 
            elif self.setting_button_rect.collidepoint(mouse_pos):
                print("Chuyển sang màn hình CÀI ĐẶT (chưa có)") 

    def update(self):
        pass

    def draw(self): # CHỮ KÝ HÀM ĐÚNG: KHÔNG CÓ THAM SỐ
        surface = self.game_manager._current_surface
        if surface is None:
            return

        surface.fill(COLOR_BG)
        
        title_text = self.font_title.render(TITLE, True, COLOR_TITLE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        surface.blit(title_text, title_rect)
        
        pygame.draw.rect(surface, COLOR_CORRECT, self.start_button_rect, border_radius=10)
        start_text = self.font_small.render("BẮT ĐẦU", True, COLOR_WHITE)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        surface.blit(start_text, start_text_rect)
        
        pygame.draw.rect(surface, COLOR_ACCENT, self.setting_button_rect, border_radius=10)
        setting_text = self.font_small.render("CÀI ĐẶT", True, COLOR_WHITE)
        setting_text_rect = setting_text.get_rect(center=self.setting_button_rect.center)
        surface.blit(setting_text, setting_text_rect)