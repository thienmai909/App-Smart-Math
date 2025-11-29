# src/screens/gameplay_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *

# Giả định một cấu trúc dữ liệu đơn giản cho câu hỏi
SAMPLE_QUESTION = {
    "question": "Thủ đô của Việt Nam là gì?",
    "answers": ["Hồ Chí Minh", "Hà Nội", "Đà Nẵng", "Huế"],
    "correct_index": 1 # Đáp án là "Hà Nội" (index 1)
}

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # 1. Khởi tạo Font và Màu sắc
        self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE) 
        self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL) 
        self.color_text = COLOR_TEXT 
        
        # 2. Dữ liệu trò chơi
        self.current_question = SAMPLE_QUESTION
        self.score = 0
        self.button_rects = [] # Lưu trữ vị trí (Rect) của các nút đáp án để kiểm tra click
        
        # 3. Tọa độ giao diện
        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.answer_start_y = SCREEN_HEIGHT // 2 - 50
        self.answer_spacing = 70
        self.answer_x = SCREEN_WIDTH // 2
        self.back_button_rect = pygame.Rect(10, 10, 100, 40) # Vị trí nút Back

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # 1. Kiểm tra click vào nút Back/Thoát
            if self.back_button_rect.collidepoint(mouse_pos):
                print("Clicked BACK. Switching to MENU.")
                self.game_manager.switch_screen("MENU")
                return

            # 2. Kiểm tra click vào đáp án
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.process_answer(i)
                    return

    def process_answer(self, selected_index):
        """Xử lý khi người chơi chọn một đáp án"""
        if selected_index == self.current_question["correct_index"]:
            self.score += 10 
            print(f"Đáp án {selected_index + 1} ĐÚNG! Điểm hiện tại: {self.score}")
        else:
            print(f"Đáp án {selected_index + 1} SAI. Điểm giữ nguyên: {self.score}")
        
        # Tạm thời, không làm gì thêm sau khi trả lời.
        # Logic chuyển câu hỏi tiếp theo sẽ được thêm vào đây sau.

    def update(self):
        pass 

    def draw(self, surface):
        surface.fill(COLOR_BG)
        
        # Reset danh sách Rects của đáp án
        self.button_rects = []
        
        # 1. Vẽ điểm số
        score_text = self.font_small.render(f"Điểm: {self.score}", True, self.color_text)
        surface.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))

        # 2. Vẽ nút Back/Thoát
        pygame.draw.rect(surface, COLOR_RED, self.back_button_rect, border_radius=5) 
        back_text = self.font_small.render("<< BACK", True, COLOR_WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        surface.blit(back_text, back_text_rect)

        # 3. Vẽ Câu hỏi
        question_text = self.font_large.render(self.current_question["question"], True, self.color_text)
        question_rect = question_text.get_rect(center=self.question_pos)
        surface.blit(question_text, question_rect)

        # 4. Vẽ 4 Đáp án
        for i, answer in enumerate(self.current_question["answers"]):
            y_pos = self.answer_start_y + i * self.answer_spacing
            
            # Kích thước nút
            button_width, button_height = 400, 50
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (self.answer_x, y_pos)
            
            # Lưu Rect để xử lý click
            self.button_rects.append(button_rect) 
            
            # Vẽ nền nút
            pygame.draw.rect(surface, COLOR_BUTTON, button_rect, border_radius=10)
            
            # Vẽ chữ đáp án
            answer_display = f"{chr(65 + i)}. {answer}" # Dùng A, B, C, D
            answer_text = self.font_small.render(answer_display, True, COLOR_TEXT)
            answer_text_rect = answer_text.get_rect(midleft=(button_rect.x + 20, y_pos))
            surface.blit(answer_text, answer_text_rect)