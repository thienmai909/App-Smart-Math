
# screens/level_select_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *

class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        
        self.levels = [
            {"name": "DỄ (Cộng/Trừ)", "key": "EASY", "color": GREEN},
            {"name": "TRUNG BÌNH (Nhân/Chia)", "key": "MEDIUM", "color": BLUE},
            {"name": "KHÓ (Hỗn Hợp)", "key": "HARD", "color": RED},
        ]
        
        self.level_buttons = []
        self._setup_buttons()

    def _setup_buttons(self):
        """Thiết lập vị trí cho các nút cấp độ."""
        self.level_buttons = []
        button_width = 300
        button_height = 70
        start_y = SCREEN_HEIGHT // 3
        padding = 30
        
        for i, level in enumerate(self.levels):
            x = (SCREEN_WIDTH - button_width) // 2
            y = start_y + i * (button_height + padding)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.level_buttons.append((rect, level["key"]))

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, (rect, level_key) in enumerate(self.level_buttons):
                if rect.collidepoint(mouse_pos):
                    # Truyền cấp độ đã chọn vào màn hình Gameplay
                    # Lưu ý: Cần cập nhật GameManager để truyền dữ liệu (xem phần dưới)
                    print(f"Đã chọn cấp độ: {level_key}")
                    self.game_manager.set_screen("gameplay", level_key=level_key)
                    break

    def update(self):
        pass

    def draw(self, surface):
        surface.fill(DARK_GRAY)

        # Tiêu đề
        title_text = "CHỌN CẤP ĐỘ"
        title_surf = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_surf, title_rect)

        # Vẽ các nút cấp độ
        for i, (rect, level_key) in enumerate(self.level_buttons):
            level_data = self.levels[i]
            
            # Vẽ hình chữ nhật
            pygame.draw.rect(surface, level_data["color"], rect, border_radius=10)
            pygame.draw.rect(surface, WHITE, rect, 3, border_radius=10) # Viền

            # Vẽ chữ trên nút
            text_surf = self.font_medium.render(level_data["name"], True, BLACK)
            text_rect_center = text_surf.get_rect(center=rect.center)
            surface.blit(text_surf, text_rect_center)