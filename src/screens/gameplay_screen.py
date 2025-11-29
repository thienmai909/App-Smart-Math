# src/screens/gameplay_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *
import time
import os # Cần thư viện os để quản lý đường dẫn file

# --- ĐỊNH NGHĨA CONSTANTS VÀ ASSETS (GIẢ ĐỊNH) ---

# Giả định đường dẫn thư mục chứa assets (Tùy chỉnh nếu cần)
ASSETS_DIR = "assets" 

SAMPLE_QUESTION = {
    "question": "15 + 7 bằng bao nhiêu?",
    "answers": ["21", "22", "23", "24"],
    "correct_index": 1
}

# Giả định COLORS và CONFIGS (Tùy chỉnh trong src/config.py)
# COLOR_BG = (30, 30, 40)
# COLOR_TEXT = (255, 255, 255)
# COLOR_ACCENT = (70, 130, 180) 
# COLOR_CORRECT = (60, 179, 113) 
# COLOR_WRONG = (220, 20, 60)
# COLOR_WHITE = (255, 255, 255)
# FONT_SIZE_LARGE = 60
# FONT_SIZE_SMALL = 30
# TIME_LIMIT = 30
# POINTS_CORRECT = 10
# POINTS_WRONG = 0
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE) 
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL) 
        
        self.score = 0
        self.current_question = SAMPLE_QUESTION
        self.button_rects = [] 
        
        # Logic Timer
        self.start_time = time.time()
        self.time_left = TIME_LIMIT
        self.game_over = False
        
        # Logic Trạng thái trả lời
        self.selected_answer_index = None
        self.show_feedback_until = 0 
        self.answer_is_correct = False 

        # Vị trí giao diện
        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.answer_start_y = SCREEN_HEIGHT // 2 - 50
        self.answer_spacing = 70
        self.answer_x = SCREEN_WIDTH // 2
        
        # Kích thước nút Back/Menu (Đã thay bằng hình ảnh)
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        
        # --- TẢI HÌNH ẢNH (ASSETS) ---
        self.assets = self._load_assets()

    def _load_assets(self):
        """Tải tất cả hình ảnh cần thiết cho màn hình Gameplay."""
        assets = {}
        try:
            # Nền
            assets['nen_lv'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nen_lv.png')).convert()
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nen_cauhoi.png')).convert_alpha()
            assets['game_over'] = pygame.image.load(os.path.join(ASSETS_DIR, 'game_over.png')).convert_alpha()
            
            # Nút Back
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nut_back.png')).convert_alpha()
            # Cập nhật kích thước nút back_button_rect theo hình ảnh
            self.back_button_rect.size = assets['nut_back'].get_size()
            
            # Nút Đáp án (Giả sử molv1.png là nền cho đáp án)
            # Dùng một hình ảnh cho nút đáp án, hoặc vẽ bằng Pygame
            assets['molv1'] = pygame.image.load(os.path.join(ASSETS_DIR, 'molv1.png')).convert_alpha()
            
            # Các asset khác có thể cần: sao, thanh_tiendo, thanh1sao, ...
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_DIR, 'thanh_tiendo.png')).convert_alpha()
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh: {e}")
            # Xử lý khi không tìm thấy file, sử dụng fallback (ví dụ: chỉ dùng màu)
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['nen_lv'].fill(COLOR_BG)
            assets['nut_back'] = self._create_placeholder_button("<< MENU", COLOR_WRONG)
            
        # Điều chỉnh kích thước hình nền nếu cần
        assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))

        return assets
    
    def _create_placeholder_button(self, text, color):
        """Tạo bề mặt giả khi không tải được hình ảnh nút"""
        surf = pygame.Surface((100, 40), pygame.SRCALPHA)
        surf.fill(color)
        text_surf = self.font_small.render(text, True, COLOR_WHITE)
        text_rect = text_surf.get_rect(center=(50, 20))
        surf.blit(text_surf, text_rect)
        return surf


    def load_next_question(self):
        """Tải câu hỏi tiếp theo và reset trạng thái"""
        # (Ở đây sẽ có logic tải câu hỏi mới)
        
        self.selected_answer_index = None
        self.show_feedback_until = 0
        self.answer_is_correct = False
        self.start_time = time.time() # Reset timer
        self.time_left = TIME_LIMIT
        
    def handle_input(self, event):
        if self.game_over:
            # TODO: Thêm logic để chuyển về Menu khi Game Over
            return 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # 1. Kiểm tra nút Back/Menu
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("MENU")
                return

            # 2. Kiểm tra Đáp án (chỉ cho phép click khi chưa trả lời)
            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        self.process_answer(i)
                        return

    def process_answer(self, selected_index):
        self.selected_answer_index = selected_index
        
        is_correct = (selected_index == self.current_question["correct_index"])
        self.answer_is_correct = is_correct
        
        if is_correct:
            self.score += POINTS_CORRECT 
        else:
            self.score += POINTS_WRONG 

        # Hiển thị phản hồi trong 1.5 giây
        self.show_feedback_until = time.time() + 1.5

    def update(self):
        if self.game_over:
            return

        current_time = time.time()
        
        # 1. Cập nhật Timer
        if self.selected_answer_index is None:
            self.time_left = TIME_LIMIT - int(current_time - self.start_time)
            if self.time_left <= 0:
                self.time_left = 0
                self.game_over = True 
                print("HẾT GIỜ! Game Over.")
        
        # 2. Xử lý phản hồi (chuyển câu hỏi)
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            if not self.game_over:
                self.load_next_question()
            
    def draw(self, surface):
        self.button_rects = []
        
        # 0. Vẽ Hình nền chính (sử dụng 'nen_lv.png')
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        # 1. Vẽ điểm số và Timer
        # Vẽ thanh tiến độ (giả sử thanh_tiendo.png là thanh bar)
        if 'thanh_tiendo' in self.assets:
            # Ví dụ: đặt thanh tiến độ ở trên cùng
            tiendo_rect = self.assets['thanh_tiendo'].get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(self.assets['thanh_tiendo'], tiendo_rect)
            
            # Vẽ Timer (đặt lên trên thanh tiến độ)
            timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
            timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
            timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(timer_text, timer_text_rect)

        # Vẽ điểm số
        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))
        
        # 2. Vẽ nút Back/Menu (sử dụng 'nut_back.png')
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        # 3. Vẽ Câu hỏi (Sử dụng 'nen_cauhoi.png' nếu có, hoặc chỉ vẽ chữ)
        if 'nen_cauhoi' in self.assets:
            question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
            surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
            question_rect_center = question_bg_rect.center
        else:
            question_rect_center = self.question_pos

        question_text = self.font_large.render(self.current_question["question"], True, COLOR_TEXT)
        question_rect = question_text.get_rect(center=question_rect_center)
        surface.blit(question_text, question_rect)

        # 4. Vẽ 4 Đáp án (sử dụng 'molv1.png' làm nền nút)
        button_image = self.assets.get('molv1', None)
        
        for i, answer in enumerate(self.current_question["answers"]):
            y_pos = self.answer_start_y + i * self.answer_spacing
            
            # Lấy kích thước từ hình ảnh hoặc mặc định
            if button_image:
                button_width, button_height = button_image.get_size()
            else:
                button_width, button_height = 400, 50

            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (self.answer_x, y_pos)
            self.button_rects.append(button_rect) 
            
            # --- Xử lý Màu/Nền Nút ---
            button_color = COLOR_ACCENT 
            is_highlighted = False
            
            if self.selected_answer_index is not None:
                if i == self.current_question["correct_index"]:
                    button_color = COLOR_CORRECT
                    is_highlighted = True
                elif i == self.selected_answer_index and not self.answer_is_correct:
                    button_color = COLOR_WRONG
                    is_highlighted = True

            # Vẽ nền nút: Ưu tiên dùng hình ảnh, nếu không có thì vẽ bằng Pygame
            if button_image:
                # Tạo một Surface tạm thời để tô màu
                temp_surface = button_image.copy()
                if is_highlighted:
                    # Tạo hiệu ứng highlight bằng cách tô màu lên Surface
                    temp_surface.fill(button_color, special_flags=pygame.BLEND_MULT)
                surface.blit(temp_surface, button_rect.topleft)
            else:
                # Fallback: Vẽ bằng Pygame.draw.rect
                pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
            
            # Vẽ chữ đáp án
            answer_display = f"{chr(65 + i)}. {answer}"
            answer_text = self.font_small.render(answer_display, True, COLOR_WHITE) # Thường chữ sẽ là màu trắng trên nền tối
            answer_text_rect = answer_text.get_rect(midleft=(button_rect.x + 20, y_pos))
            surface.blit(answer_text, answer_text_rect)
            
        # 5. Vẽ thông báo Game Over
        if self.game_over:
            # Sử dụng hình ảnh game_over.png nếu có, nếu không thì dùng overlay
            if 'game_over' in self.assets:
                go_image = self.assets['game_over']
                go_rect = go_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                surface.blit(go_image, go_rect)
            else:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180)) 
                surface.blit(overlay, (0, 0))
                
                game_over_text = self.font_large.render("HẾT GIỜ! Game Over", True, COLOR_WRONG)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                surface.blit(game_over_text, text_rect)