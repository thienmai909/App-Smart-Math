import pygame
from src.screens.base_screen import BaseScreen
# Quan trọng: Đảm bảo bạn import tất cả các hằng số màu đã sử dụng
from src.config import *
import os

# --- CẤU HÌNH CÁC CẤP ĐỘ (LEVELS) ---
# Đây là nơi xảy ra lỗi NameError
LEVELS = [
    {
        "name": "DỄ (Cộng/Trừ)", 
        "key": "EASY", 
        "color": GREEN, # Giả định GREEN = (0, 255, 0)
        "description": "Thực hiện phép cộng và trừ cơ bản."
    },
    {
        "name": "TRUNG BÌNH (Nhân/Chia)", 
        "key": "MEDIUM", 
        "color": YELLOW, # Giả định YELLOW = (255, 255, 0)
        "description": "Thực hiện phép nhân và chia."
    },
    {
        "name": "KHÓ (Hỗn hợp)", 
        "key": "HARD", 
        "color": BLUE, # Giả định BLUE = (0, 0, 255)
        "description": "Kết hợp tất cả các phép toán."
    },
]

# Giả định đường dẫn thư mục chứa assets (Tùy chỉnh nếu cần)
ASSETS_DIR = "assets"

class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE)
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL)
        self.level_rects = [] # Lưu trữ các Rect của nút cấp độ
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        
        # --- TẢI HÌNH ẢNH (Dựa trên danh sách assets cũ) ---
        self.assets = self._load_assets()
        
    def _load_assets(self):
        """Tải các hình ảnh cần thiết cho màn hình chọn cấp độ."""
        assets = {}
        try:
            # Nền (Dùng hình nền menu hoặc hình nền chung)
            assets['nen_lv'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nen_lv.png')).convert()
            assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # Nút Back
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nut_back.png')).convert_alpha()
            self.back_button_rect.size = assets['nut_back'].get_size()
            
            # Nút cấp độ (Giả sử dùng giaodiendautien.png làm nền chung hoặc chỉ vẽ)
            # Nếu có hình ảnh cụ thể cho nút cấp độ, hãy thay thế ở đây
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh Level Select: {e}")
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['nen_lv'].fill(COLOR_BG)
            # Fallback cho nút Back
            assets['nut_back'] = pygame.Surface((100, 40), pygame.SRCALPHA)
            assets['nut_back'].fill(COLOR_WRONG)
            
        return assets
        
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # 1. Kiểm tra nút Back/Menu
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("MENU")
                return
            
            # 2. Kiểm tra Nút Cấp độ
            for i, rect in enumerate(self.level_rects):
                if rect.collidepoint(mouse_pos):
                    selected_level = LEVELS[i]
                    print(f"Bắt đầu chơi cấp độ: {selected_level['key']} - {selected_level['name']}")
                    # TODO: Thực hiện logic chuyển sang GameplayScreen với cấp độ được chọn
                    self.game_manager.current_level_key = selected_level['key']
                    self.game_manager.switch_screen("GAMEPLAY")
                    return

    def update(self):
        pass

    def draw(self, surface):
        self.level_rects = [] # Reset list rects
        surface.blit(self.assets['nen_lv'], (0, 0)) # Vẽ hình nền
        
        # 1. Vẽ Tiêu đề
        title_text = self.font_large.render("CHỌN CẤP ĐỘ", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)
        
        # 2. Vẽ Nút Back/Menu
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        # 3. Vẽ các Nút Cấp độ
        start_y = SCREEN_HEIGHT // 3 
        spacing = 100
        
        for i, level in enumerate(LEVELS):
            y_pos = start_y + i * spacing
            button_width, button_height = 500, 70
            
            # Tạo Rect cho nút
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (SCREEN_WIDTH // 2, y_pos)
            self.level_rects.append(button_rect)
            
            # Vẽ nền nút
            button_color = level["color"]
            pygame.draw.rect(surface, button_color, button_rect, border_radius=15)
            pygame.draw.rect(surface, COLOR_ACCENT, button_rect, 5, border_radius=15) # Vẽ viền

            # Vẽ tên cấp độ
            name_text = self.font_small.render(level["name"], True, COLOR_WHITE)
            name_text_rect = name_text.get_rect(center=button_rect.center)
            surface.blit(name_text, name_text_rect)
            
            # Vẽ mô tả (tùy chọn)
            desc_text = self.font_small.render(level["description"], True, COLOR_TEXT)
            desc_rect = desc_text.get_rect(midtop=(SCREEN_WIDTH // 2, y_pos + 40))
            # surface.blit(desc_text, desc_rect) # Bỏ comment nếu muốn hiển thị mô tả