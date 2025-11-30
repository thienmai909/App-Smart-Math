# src/screens/gameplay_screen.py
import pygame
import os
import time
from src.screens.base_screen import BaseScreen
from src.config import *

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init>(game_manager)
        
        try:
            self.font_large = pygame.font.Font(None, FONT_SIZE_LARGE) 
            self.font_small = pygame.font.Font(None, FONT_SIZE_SMALL) 
            self.font_title = pygame.font.Font(None, FONT_SIZE_TITLE) 
            self.font_medium = pygame.font.Font(None, FONT_SIZE_MEDIUM) # Thêm font medium
        except pygame.error:
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
        
        # --- KHẮC PHỤC LỖI ATTRIBUTEERROR: KHAI BÁO CÁC RECT TRƯỚC KHI TẢI ASSETS ---
        self.back_button_rect = pygame.Rect(10, 10, 100, 40) # Khai báo trước
        self.game_over_button_rect = pygame.Rect(0, 0, 200, 50) # Khai báo trước
        # -----------------------------------------------------------------------------
        
        self.score = 0
        self.current_question = None 
        self.button_rects = [] 
        
        self.start_time = time.time()
        self.time_left = TIME_LIMIT
        self.game_over = False
        self.final_stars = 0 

        self.selected_answer_index = None
        self.show_feedback_until = 0 
        self.answer_is_correct = False 

        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.answer_start_y = SCREEN_HEIGHT // 2 - 50
        self.answer_spacing = 70
        self.answer_x = SCREEN_WIDTH // 2
        
        self.assets = self._load_assets() # Gọi hàm tải assets (Bây giờ đã an toàn)
        
        # Gán center cho nút game over sau khi đã gọi load assets
        self.game_over_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)

    def _load_assets(self):
        assets = {}
        try:
            assets['nen_lv'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_lv.png')).convert()
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_cauhoi.png')).convert_alpha()
            assets['game_over'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
            # Dòng lỗi cũ đã được chuyển lên trên. Giờ chỉ cần gán size:
            self.back_button_rect.size = assets['nut_back'].get_size() 
            assets['molv1'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'molv1.png')).convert_alpha()
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            
            assets['sao_large'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha()
            assets['sao_large'] = pygame.transform.scale(assets['sao_large'], (50, 50))
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh Gameplay: {e}. Vui lòng kiểm tra thư mục {ASSETS_IMG_DIR}.")
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_lv'].fill(COLOR_BG)
            assets['nut_back'] = pygame.Surface((100, 40)); assets['nut_back'].fill(COLOR_WRONG)
            assets['molv1'] = pygame.Surface((400, 70)); assets['molv1'].fill(COLOR_ACCENT)
            assets['sao_large'] = None
            
        assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))
        return assets

    def reset_game(self):
        self.score = 0
        self.current_question = None
        self.game_over = False
        self.time_left = TIME_LIMIT
        self.selected_answer_index = None
        self.final_stars = 0

    def load_next_question(self):
        
        if self.game_manager.question_index < len(self.game_manager.questions_pool):
            q_data = self.game_manager.questions_pool[self.game_manager.question_index]
            
            self.current_question = {
                "question": q_data["question"],
                "answers": [str(o) for o in q_data["options"]], 
                "correct_answer": str(q_data["answer"])
            }
            try:
                self.current_question["correct_index"] = self.current_question["answers"].index(self.current_question["correct_answer"])
            except ValueError:
                self.current_question["correct_index"] = -1
            
            self.game_manager.question_index += 1
            
            self.selected_answer_index = None
            self.show_feedback_until = 0
            self.answer_is_correct = False
            self.start_time = time.time()
            self.time_left = TIME_LIMIT
        
        else:
            self.game_over = True
            self.final_stars = self.game_manager.calculate_stars(self.score)
            self.game_manager.save_score(self.score) 

    def handle_input(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.game_over_button_rect.collidepoint(mouse_pos):
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
                        if 'click_dapan' in self.game_manager.sound_assets:
                             self.game_manager.sound_assets['click_dapan'].play()
                        self.process_answer(i)
                        return

    def process_answer(self, selected_index):
        self.selected_answer_index = selected_index
        
        is_correct = (selected_index == self.current_question["correct_index"])
        self.answer_is_correct = is_correct
        
        if 'correct' in self.game_manager.sound_assets and is_correct:
            self.game_manager.sound_assets['correct'].play()
        elif 'wrong' in self.game_manager.sound_assets and not is_correct:
            self.game_manager.sound_assets['wrong'].play()
        
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
                self.final_stars = self.game_manager.calculate_stars(self.score + POINTS_WRONG)
                self.game_manager.save_score(self.score + POINTS_WRONG) 
        
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            self.load_next_question()
            
    def draw(self, surface):
        self.button_rects = []
        
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        # 1. VẼ ĐIỂM SỐ VÀ TIMER
        if 'thanh_tiendo' in self.assets:
            tiendo_rect = self.assets['thanh_tiendo'].get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(self.assets['thanh_tiendo'], tiendo_rect)
            
            timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
            timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
            timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(timer_text, timer_text_rect)

        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 10 - score_text.get_width(), 10))
        
        # 2. VẼ NÚT BACK/MENU
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        if self.current_question:
            # 3. VẼ CÂU HỎI
            if 'nen_cauhoi' in self.assets:
                question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
                surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
                question_rect_center = question_bg_rect.center
            else:
                question_rect_center = self.question_pos

            question_text = self.font_large.render(self.current_question["question"], True, COLOR_TEXT)
            question_rect = question_text.get_rect(center=question_rect_center)
            surface.blit(question_text, question_rect)

            # 4. VẼ 4 ĐÁP ÁN
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
                answer_text_rect = answer_text.get_rect(midleft=(button_rect.x + 40, y_pos)) # Căn lề trái
                surface.blit(answer_text, answer_text_rect)
            
        # 5. VẼ THÔNG BÁO GAME OVER
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            surface.blit(overlay, (0, 0))
            
            if 'game_over' in self.assets:
                go_image = self.assets['game_over']
                go_rect = go_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
                surface.blit(go_image, go_rect)
            else:
                game_over_text = self.font_title.render("KẾT THÚC!", True, COLOR_WRONG)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
                surface.blit(game_over_text, text_rect)
                
            score_final_text = self.font_large.render(f"ĐIỂM CUỐI: {self.score}", True, COLOR_TEXT)
            score_final_rect = score_final_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            surface.blit(score_final_text, score_final_rect)
            
            # VẼ SAO ĐẠT ĐƯỢC
            star_asset = self.assets.get('sao_large', None)
            star_width = 50
            star_spacing = 15
            
            total_width = 3 * star_width + 2 * star_spacing
            star_start_x = SCREEN_WIDTH // 2 - total_width // 2
            
            for s in range(3):
                star_x = star_start_x + s * (star_width + star_spacing)
                star_y = SCREEN_HEIGHT // 2 + 50
                
                if s < self.final_stars and star_asset:
                    surface.blit(star_asset, (star_x, star_y))
                else:
                    pygame.draw.circle(surface, (150, 150, 150), (star_x + star_width//2, star_y + star_width//2), star_width//2, 2)
                    
            # Nút Quay lại Menu
            pygame.draw.rect(surface, COLOR_CORRECT, self.game_over_button_rect, border_radius=10)
            menu_text = self.font_small.render("VỀ MENU", True, COLOR_WHITE)
            menu_text_rect = menu_text.get_rect(center=self.game_over_button_rect.center)
            surface.blit(menu_text, menu_text_rect)