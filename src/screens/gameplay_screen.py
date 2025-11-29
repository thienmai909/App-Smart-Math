# src/screens/gameplay_screen.py
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *
import time
import os

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
        
        self.start_time = time.time()
        self.time_left = TIME_LIMIT
        self.game_over = False
        
        self.selected_answer_index = None
        self.show_feedback_until = 0 
        self.answer_is_correct = False 

        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.answer_start_y = SCREEN_HEIGHT // 2 - 50
        self.answer_spacing = 70
        self.answer_x = SCREEN_WIDTH // 2
        
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        
        self.assets = self._load_assets()

    def _load_assets(self):
        assets = {}
        try:
            # Sử dụng ASSETS_DIR đã được sửa trong config.py
            assets['nen_lv'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nen_lv.png')).convert()
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nen_cauhoi.png')).convert_alpha()
            assets['game_over'] = pygame.image.load(os.path.join(ASSETS_DIR, 'game_over.png')).convert_alpha()
            
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_DIR, 'nut_back.png')).convert_alpha()
            self.back_button_rect.size = assets['nut_back'].get_size()
            
            assets['molv1'] = pygame.image.load(os.path.join(ASSETS_DIR, 'molv1.png')).convert_alpha()
            
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_DIR, 'thanh_tiendo.png')).convert_alpha()
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh Gameplay: {e}. Vui lòng kiểm tra thư mục assets.")
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            assets['nen_lv'].fill(COLOR_BG)
            assets['nut_back'] = self._create_placeholder_button("<< MENU", COLOR_WRONG)
            
        assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))

        return assets
    
    def _create_placeholder_button(self, text, color):
        surf = pygame.Surface((100, 40), pygame.SRCALPHA)
        surf.fill(color)
        text_surf = self.font_small.render(text, True, COLOR_WHITE)
        text_rect = text_surf.get_rect(center=(50, 20))
        surf.blit(text_surf, text_rect)
        return surf


    def load_next_question(self):
        
        self.selected_answer_index = None
        self.show_feedback_until = 0
        self.answer_is_correct = False
        self.start_time = time.time()
        self.time_left = TIME_LIMIT
        
    def handle_input(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_manager.switch_screen("MENU")
            return 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("MENU")
                return

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

        self.show_feedback_until = time.time() + 1.5

    def update(self):
        if self.game_over:
            return

        current_time = time.time()
        
        if self.selected_answer_index is None:
            self.time_left = TIME_LIMIT - int(current_time - self.start_time)
            if self.time_left <= 0:
                self.time_left = 0
                self.game_over = True 
                print("HẾT GIỜ! Game Over.")
        
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            if not self.game_over:
                self.load_next_question()
            
    def draw(self, surface):
        self.button_rects = []
        
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        # 1. Vẽ điểm số và Timer
        if 'thanh_tiendo' in self.assets:
            tiendo_rect = self.assets['thanh_tiendo'].get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(self.assets['thanh_tiendo'], tiendo_rect)
            
            timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
            timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
            timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(timer_text, timer_text_rect)

        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))
        
        # 2. Vẽ nút Back/Menu 
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        # 3. Vẽ Câu hỏi
        if 'nen_cauhoi' in self.assets:
            question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
            surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
            question_rect_center = question_bg_rect.center
        else:
            question_rect_center = self.question_pos

        question_text = self.font_large.render(self.current_question["question"], True, COLOR_TEXT)
        question_rect = question_text.get_rect(center=question_rect_center)
        surface.blit(question_text, question_rect)

        # 4. Vẽ 4 Đáp án
        button_image = self.assets.get('molv1', None)
        
        for i, answer in enumerate(self.current_question["answers"]):
            y_pos = self.answer_start_y + i * self.answer_spacing
            
            if button_image:
                button_width, button_height = button_image.get_size()
            else:
                button_width, button_height = 400, 50

            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (self.answer_x, y_pos)
            self.button_rects.append(button_rect) 
            
            button_color = COLOR_ACCENT 
            is_highlighted = False
            
            if self.selected_answer_index is not None:
                if i == self.current_question["correct_index"]:
                    button_color = COLOR_CORRECT
                    is_highlighted = True
                elif i == self.selected_answer_index and not self.answer_is_correct:
                    button_color = COLOR_WRONG
                    is_highlighted = True

            if button_image:
                temp_surface = button_image.copy()
                if is_highlighted:
                    temp_surface.fill(button_color, special_flags=pygame.BLEND_MULT)
                surface.blit(temp_surface, button_rect.topleft)
            else:
                pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
            
            answer_display = f"{chr(65 + i)}. {answer}"
            answer_text = self.font_small.render(answer_display, True, COLOR_WHITE)
            answer_text_rect = answer_text.get_rect(midleft=(button_rect.x + 20, y_pos))
            surface.blit(answer_text, answer_text_rect)
            
        # 5. Vẽ thông báo Game Over
        if self.game_over:
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