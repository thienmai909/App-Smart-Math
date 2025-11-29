# src/screens/menu_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *

class MenuScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        
        self.start_button_rect = pygame.Rect(0, 0, 250, 60)
        self.start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.start_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("GAMEPLAY")

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(COLOR_BG)
        
        # Vẽ tiêu đề
        title_text = self.font_title.render(TITLE, True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        surface.blit(title_text, title_rect)
        
        # Vẽ nút Bắt đầu (Sử dụng COLOR_CORRECT cho nút chính)
        pygame.draw.rect(surface, COLOR_CORRECT, self.start_button_rect, border_radius=10)
        start_text = self.font_small.render("BẮT ĐẦU", True, COLOR_WHITE)
        start_text_rect = start_text.get_rect(center=self.start_button_rect.center)
        surface.blit(start_text, start_text_rect)