import pygame
import os
import time
from src.screens.base_screen import BaseScreen
from src.config import * # ĐƯỜNG DẪN MẪU ĐẾN FONT HỖ TRỢ TIẾNG VIỆT
try:
    # Cần đảm bảo ASSETS_FONT_DIR được định nghĩa trong config
    VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')
except NameError:
    VIETNAMESE_FONT_PATH = None

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # SỬA LỖI FONT
        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_title = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_TITLE) 
                self.font_large = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_LARGE)
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL) 
                self.font_medium = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_MEDIUM)
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
                self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
        except pygame.error:
            self.font_title = pygame.font.SysFont("Arial", 60)
            self.font_large = pygame.font.SysFont("Arial", 40)
            self.font_small = pygame.font.SysFont("Arial", 24)
            self.font_medium = pygame.font.SysFont("Arial", 30)
        
        # Khởi tạo các biến trạng thái trò chơi
        self.score = 0
        self.current_question = None 
        self.button_rects = [] 
        
        try:
            self.time_limit = TIME_LIMIT
        except NameError:
            self.time_limit = 30
        
        self.start_time = time.time()
        self.time_left = self.time_limit
        self.game_over = False
        self.final_stars = 0 
        self.selected_answer_index = None
        self.show_feedback_until = 0 
        self.answer_is_correct = False 

        # Vị trí các phần tử UI
        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 20)
        self.answer_start_y = SCREEN_HEIGHT // 2 + 50
        self.answer_spacing = 80 
        self.answer_x = SCREEN_WIDTH // 2
        
        # Tải assets
        self.assets = self._load_assets() 
        
        # Thiết lập Rect cho các nút
        self.back_button_rect = self.assets['nut_back'].get_rect(topleft=(20, 20))
        self.game_over_button_rect = pygame.Rect(0, 0, 250, 60)
        self.game_over_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)

        # Biến Tiến độ Câu hỏi
        self.total_questions = len(self.game_manager.questions_pool)
        self.progress_bar_rect = pygame.Rect(SCREEN_WIDTH // 2 - 250, 80, 500, 30)


    def _load_assets(self):
        assets = {}
        try:
            # Tải và scale các assets UI
            assets['nen_lv'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_lv.png')).convert()
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_cauhoi.png')).convert_alpha()
            assets['game_over'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
            
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
            assets['nut_back'] = pygame.transform.scale(assets['nut_back'], (150, 60))

            assets['molv1'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'molv1.png')).convert_alpha()
            assets['molv1'] = pygame.transform.scale(assets['molv1'], (400, 60))
            
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            assets['thanh_tiendo'] = pygame.transform.scale(assets['thanh_tiendo'], (500, 30))
            
            assets['sao_large'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha()
            assets['sao_large'] = pygame.transform.scale(assets['sao_large'], (50, 50))
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh Gameplay: {e}. Vui lòng kiểm tra thư mục {ASSETS_IMG_DIR} và file ảnh.")
            # Assets dự phòng
            assets['nen_lv'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_lv'].fill(COLOR_BG)
            assets['nut_back'] = pygame.Surface((150, 60)); assets['nut_back'].fill(COLOR_WRONG)
            assets['molv1'] = pygame.Surface((400, 60)); assets['molv1'].fill(COLOR_ACCENT)
            assets['thanh_tiendo'] = pygame.Surface((500, 30)); assets['thanh_tiendo'].fill(COLOR_GRAY)
            assets['sao_large'] = None
            
        assets['nen_lv'] = pygame.transform.scale(assets['nen_lv'], (SCREEN_WIDTH, SCREEN_HEIGHT))
        return assets
    
    # Hàm được gọi bởi GameManager khi màn hình được chuyển đến
    def start_level(self):
        self.reset_game()
        self.load_next_question()

    def reset_game(self):
        self.score = 0
        self.current_question = None
        self.game_over = False
        self.time_left = self.time_limit
        self.selected_answer_index = None
        self.final_stars = 0
        self.game_manager.question_index = 0

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
            self.time_left = self.time_limit
        
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
            
            # Nút Back -> Quay lại màn hình chọn Level
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("LEVEL_SELECT")
                return

            # Xử lý chọn đáp án
            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        if self.game_manager.sound_assets.get('click_dapan'):
                             self.game_manager.sound_assets['click_dapan'].play()
                        self.process_answer(i)
                        return

    def process_answer(self, selected_index):
        self.selected_answer_index = selected_index
        
        is_correct = (selected_index == self.current_question["correct_index"])
        self.answer_is_correct = is_correct
        
        if is_correct:
            if self.game_manager.sound_assets.get('correct'):
                self.game_manager.sound_assets['correct'].play()
            try:
                self.score += POINTS_CORRECT 
            except NameError:
                self.score += 10 
        else:
            if self.game_manager.sound_assets.get('wrong'):
                self.game_manager.sound_assets['wrong'].play()
            try:
                self.score += POINTS_WRONG 
            except NameError:
                self.score += -5 

        self.show_feedback_until = time.time() + 1.5

    def update(self):
        if self.game_over:
            return

        current_time = time.time()
        
        if self.selected_answer_index is None:
            self.time_left = self.time_limit - int(current_time - self.start_time)
            
            if self.time_left <= 0:
                self.time_left = 0
                self.game_over = True
                
                try:
                    self.final_stars = self.game_manager.calculate_stars(self.score + POINTS_WRONG)
                except NameError:
                    self.final_stars = self.game_manager.calculate_stars(self.score - 5)
                    
                self.game_manager.save_score(self.score) 
        
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            self.load_next_question()
            
    def draw(self): 
        surface = self.game_manager._current_surface
        if surface is None:
            return
            
        self.button_rects = []
        
        surface.blit(self.assets['nen_lv'], (0, 0))
        
        # 1. VẼ THANH TIẾN ĐỘ CÂU HỎI
        tiendo_asset = self.assets.get('thanh_tiendo')
        if tiendo_asset and self.total_questions > 0:
            tiendo_rect = tiendo_asset.get_rect(center=(SCREEN_WIDTH // 2, 80))
            
            # 1a. Vẽ nền (thanh_tiendo)
            surface.blit(tiendo_asset, tiendo_rect.topleft)
            
            # 1b. Tính toán và Vẽ thanh Fill
            current_q_index_for_display = self.game_manager.question_index - 1 
            if current_q_index_for_display < 0: current_q_index_for_display = 0 
            
            progress_ratio = current_q_index_for_display / self.total_questions
            
            max_fill_width = 480 
            fill_width = int(max_fill_width * progress_ratio)
            
            fill_rect = pygame.Rect(tiendo_rect.x + 10, tiendo_rect.y + 5, fill_width, 20)
            pygame.draw.rect(surface, COLOR_CORRECT, fill_rect, border_radius=5)
            
            # 1c. Vẽ Text Tiến độ
            progress_text = self.font_small.render(f"Câu hỏi: {current_q_index_for_display}/{self.total_questions}", True, COLOR_BLACK)
            progress_text_rect = progress_text.get_rect(center=tiendo_rect.center)
            surface.blit(progress_text, progress_text_rect)

        # 2. VẼ TIMER VÀ ĐIỂM
        timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
        timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
        surface.blit(timer_text, (SCREEN_WIDTH // 2 - 300, 20)) 

        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 20 - score_text.get_width(), 20))
        
        # 3. VẼ NÚT BACK
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        if self.current_question:
            # 4. VẼ CÂU HỎI
            if 'nen_cauhoi' in self.assets:
                question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
                surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
                question_rect_center = question_bg_rect.center
            else:
                question_rect_center = self.question_pos

            question_text = self.font_large.render(self.current_question["question"], True, COLOR_TEXT)
            question_rect = question_text.get_rect(center=question_rect_center)
            surface.blit(question_text, question_rect)

            # 5. VẼ 4 ĐÁP ÁN (Hình ảnh molv1)
            button_image = self.assets.get('molv1', None)
            
            for i, answer in enumerate(self.current_question["answers"]):
                y_pos = self.answer_start_y + i * self.answer_spacing
                
                if button_image:
                    button_width, button_height = button_image.get_size()
                else:
                    button_width, button_height = 400, 60

                button_rect = pygame.Rect(0, 0, button_width, button_height)
                button_rect.center = (self.answer_x, y_pos) 
                self.button_rects.append(button_rect) 
                
                button_color = COLOR_ACCENT 
                is_highlighted = False
                
                # Highlight đáp án
                if self.selected_answer_index is not None:
                    if i == self.current_question["correct_index"]:
                        button_color = COLOR_CORRECT
                        is_highlighted = True
                    elif i == self.selected_answer_index and not self.answer_is_correct:
                        button_color = COLOR_WRONG
                        is_highlighted = True

                if button_image:
                    temp_surface = button_image.copy()
                    
                    # 5a. Vẽ hình ảnh nút (có chữ LEVEL 1)
                    surface.blit(temp_surface, button_rect.topleft)
                    
                    # 5b. CHE PHỦ CHỮ "LEVEL 1" bằng màu nền (Giả định chữ nằm giữa)
                    # Rect che (cần điều chỉnh tọa độ này nếu cần)
                    # Giả định: Chữ Level nằm từ x+100 đến x+300, y+10 đến y+50
                    cover_rect = pygame.Rect(button_rect.x + 100, button_rect.y + 10, 200, 40)
                    # Sử dụng COLOR_ACCENT là màu nền mặc định của nút
                    pygame.draw.rect(surface, COLOR_ACCENT, cover_rect) 
                    
                    # 5c. ÁP DỤNG MÀU HIGHLIGHT (vẽ Rect mới lên trên vùng đáp án)
                    if is_highlighted:
                        # Vùng highlight rộng hơn, bao gồm cả vùng che
                        highlight_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_width - 10, button_height - 10)
                        
                        # Tạo surface tạm thời để có độ trong suốt (alpha)
                        highlight_surface = pygame.Surface(highlight_rect.size, pygame.SRCALPHA)
                        # Tô màu highlight với độ trong suốt (ví dụ alpha 100)
                        highlight_surface.fill(button_color + (100,)) 
                        surface.blit(highlight_surface, highlight_rect.topleft)

                else:
                    # Logic vẽ rect dự phòng nếu không có hình ảnh
                    pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
                
                # 5d. Vẽ text đáp án (A. Nội dung) lên trên cùng
                answer_display = f"{chr(65 + i)}. {answer}"
                answer_text = self.font_medium.render(answer_display, True, COLOR_WHITE) 
                answer_text_rect = answer_text.get_rect(midleft=(button_rect.x + 40, y_pos)) 
                surface.blit(answer_text, answer_text_rect)
            
        # 6. VẼ THÔNG BÁO GAME OVER
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