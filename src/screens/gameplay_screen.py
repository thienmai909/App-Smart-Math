# src/screens/gameplay_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *
import time # Cần thư viện time để quản lý thời gian

SAMPLE_QUESTION = {
    "question": "15 + 7 bằng bao nhiêu?",
    "answers": ["21", "22", "23", "24"],
    "correct_index": 1
}

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
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)

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
        surface.fill(COLOR_BG)
        self.button_rects = []
        
        # 1. Vẽ điểm số và Timer
        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))

        # Vẽ Timer
        timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
        timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
        surface.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, 10))
        
        # 2. Vẽ nút Back/Menu
        pygame.draw.rect(surface, COLOR_WRONG, self.back_button_rect, border_radius=5) 
        back_text = self.font_small.render("<< MENU", True, COLOR_WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        surface.blit(back_text, back_text_rect)

        # 3. Vẽ Câu hỏi
        question_text = self.font_large.render(self.current_question["question"], True, COLOR_TEXT)
        question_rect = question_text.get_rect(center=self.question_pos)
        surface.blit(question_text, question_rect)

        # 4. Vẽ 4 Đáp án
        for i, answer in enumerate(self.current_question["answers"]):
            y_pos = self.answer_start_y + i * self.answer_spacing
            
            button_width, button_height = 400, 50
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (self.answer_x, y_pos)
            self.button_rects.append(button_rect) 
            
            # Chọn màu nền nút
            button_color = COLOR_ACCENT # Màu mặc định (đã sửa từ COLOR_BUTTON)
            if self.selected_answer_index is not None:
                # Nếu đang hiển thị feedback
                if i == self.current_question["correct_index"]:
                    button_color = COLOR_CORRECT # Đáp án đúng luôn màu xanh lá
                elif i == self.selected_answer_index and not self.answer_is_correct:
                    button_color = COLOR_WRONG # Đáp án sai người chơi chọn màu đỏ

            # Vẽ nền nút
            pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
            
            # Vẽ chữ đáp án
            answer_display = f"{chr(65 + i)}. {answer}"
            answer_text = self.font_small.render(answer_display, True, COLOR_TEXT)
            answer_text_rect = answer_text.get_rect(midleft=(button_rect.x + 20, y_pos))
            surface.blit(answer_text, answer_text_rect)
            
        # 5. Vẽ thông báo Game Over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            surface.blit(overlay, (0, 0))
            
            game_over_text = self.font_large.render("HẾT GIỜ! Game Over", True, COLOR_WRONG)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(game_over_text, text_rect)