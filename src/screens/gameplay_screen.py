import pygame
import os
import time
import random 
from src.screens.base_screen import BaseScreen
from src.config import *

VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # --- KHỞI TẠO FONT ---
        try:
            selected_font_path = None
            
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                selected_font_path = VIETNAMESE_FONT_PATH
            else:
                font_candidates = ['Segoe UI', 'Times New Roman', 'Arial Unicode MS', 'DejaVuSans', 'Arial']
                for candidate in font_candidates:
                    match = pygame.font.match_font(candidate)
                    if match:
                        selected_font_path = match
                        break
                
            if selected_font_path:
                self.font_title = pygame.font.Font(selected_font_path, FONT_SIZE_TITLE) 
                self.font_large = pygame.font.Font(selected_font_path, FONT_SIZE_LARGE)
                self.font_small = pygame.font.Font(selected_font_path, FONT_SIZE_SMALL) 
                self.font_medium = pygame.font.Font(selected_font_path, FONT_SIZE_MEDIUM)
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
                self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
                
        except pygame.error:
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
        
        # Kích thước cố định 
        self.ANSWER_BUTTON_SIZE = (350, 80)
        self.STAR_SIZE = 50 
        self.STAR_BAR_SIZE = (300, 60)
        self.back_button_rect = pygame.Rect(20, 20, 100, 40) 
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 100, 40) # Rect cho nút Cài đặt
        
        self.GAME_OVER_BUTTON_SIZE = (250, 60) 
        self.game_over_button_rect = pygame.Rect(0, 0, *self.GAME_OVER_BUTTON_SIZE)
        
        self.score = 0
        self.current_question = None 
        self.button_rects = [] 
        
        self.time_limit = TIME_LIMIT
        self.start_time = time.time()
        self.time_left = self.time_limit
        self.game_over = False
        self.final_stars = 0 

        self.selected_answer_index = None
        self.show_feedback_until = 0 
        self.answer_is_correct = False 

        # Vị trí câu hỏi 
        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30)
        self.answer_start_y = SCREEN_HEIGHT // 2 + 50
        self.answer_spacing = 140 
        
        self.assets = self._load_assets() 
        
        self.game_over_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
        
    def _load_assets(self):
        assets = {}
        assets['is_settings_fallback'] = False # Cờ theo dõi việc sử dụng fallback
        try:
            # 1. NỀN MÀN HÌNH CHÍNH (nenchinh.png)
            try:
                assets['nen_chinh'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nenchinh.png')).convert()
                assets['nen_chinh'] = pygame.transform.scale(assets['nen_chinh'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)

            # 2. NỀN CÂU HỎI (nencauhoi.png)
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nencauhoi.png')).convert_alpha()
            assets['nen_cauhoi'] = pygame.transform.scale(assets['nen_cauhoi'], (750, 200))
            
            # 3. NỀN ĐÁP ÁN (nendapan.png)
            assets['nen_dapan'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nendapan.png')).convert_alpha()
            assets['nen_dapan'] = pygame.transform.scale(assets['nen_dapan'], self.ANSWER_BUTTON_SIZE)
            
            # 4. GAME OVER IMAGE (game_over.png)
            try:
                assets['game_over_image'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
                assets['game_over_image'] = pygame.transform.scale(assets['game_over_image'], (600, 400)) 
            except pygame.error:
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)
                text_go = self.font_title.render("GAME OVER", True, COLOR_TITLE)
                text_score = self.font_large.render("Score", True, COLOR_TEXT)
                assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
                assets['game_over_image'].blit(text_score, text_score.get_rect(center=(200, 100)))

            # 5. NÚT BACK (nut_back)
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
            assets['nut_back'] = pygame.transform.scale(assets['nut_back'], (80, 30))
            self.back_button_rect.size = assets['nut_back'].get_size() 
            self.back_button_rect.topleft = (20, 20)
            
            # 5b. NÚT SETTINGS (nutcaidat.png)
            try:
                # SỬ DỤNG TÊN FILE nutcaidat.png CHÍNH XÁC
                assets['nutcaidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha() 
                assets['nutcaidat'] = pygame.transform.scale(assets['nutcaidat'], (80, 30))
            except pygame.error:
                print("Không tìm thấy nutcaidat.png. Sử dụng surface màu mặc định.")
                assets['nutcaidat'] = pygame.Surface((80, 30)); assets['nutcaidat'].fill(COLOR_INFO) 
                assets['is_settings_fallback'] = True # Bật cờ fallback
            
            self.settings_button_rect.size = assets['nutcaidat'].get_size()
            self.settings_button_rect.topright = (SCREEN_WIDTH - 20, 20) 

            # 6. NÚT NEXT (nut_next.png)
            try:
                assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
                assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.GAME_OVER_BUTTON_SIZE)
            except pygame.error:
                assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
                
            # 7. THANH TIẾN ĐỘ (thanh_tiendo)
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            assets['thanh_tiendo'] = pygame.transform.scale(assets['thanh_tiendo'], (300, 40))
            
            # 8. THANH SAO & SAO
            star_surf = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE), pygame.SRCALPHA)
            pygame.draw.polygon(star_surf, (255, 223, 0), [(25, 0), (33, 17), (50, 19), (38, 30), (41, 50), (25, 38), (9, 50), (12, 30), (0, 19), (17, 17)], 0)
            assets['sao_large'] = star_surf
            
            for i in range(4):
                    filename = f'thanh_sao_{i}.png'
                    try:
                        star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, filename)).convert_alpha()
                        assets[f'thanh_sao_{i}'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)
                    except pygame.error:
                        fallback_surf = pygame.Surface(self.STAR_BAR_SIZE, pygame.SRCALPHA)
                        fallback_surf.fill((200, 200, 200, 150))
                        assets[f'thanh_sao_{i}'] = fallback_surf
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh: {e}. Sử dụng Surface màu mặc định cho các thành phần bị thiếu.")
            assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)
            assets['nen_cauhoi'] = pygame.Surface((650, 150), pygame.SRCALPHA); assets['nen_cauhoi'].fill((255, 255, 255, 150))
            assets['nen_dapan'] = pygame.Surface(self.ANSWER_BUTTON_SIZE, pygame.SRCALPHA); assets['nen_dapan'].fill(COLOR_ACCENT) 
            assets['nut_back'] = pygame.Surface((150, 60)); assets['nut_back'].fill(COLOR_WRONG)
            assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
            assets['thanh_tiendo'] = pygame.Surface((300, 40)); assets['thanh_tiendo'].fill((200, 200, 200))
            assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA); 
            text_go = self.font_title.render("GAME OVER", True, COLOR_TITLE)
            assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
            assets['sao_large'] = None
            assets['nutcaidat'] = pygame.Surface((80, 30)); assets['nutcaidat'].fill(COLOR_INFO) 
            assets['is_settings_fallback'] = True # Bật cờ fallback
            for i in range(4):
                    assets[f'thanh_sao_{i}'] = pygame.Surface(self.STAR_BAR_SIZE); assets[f'thanh_sao_{i}'].fill((200, 200, 200))
        return assets

    def reset_game(self):
        self.score = 0
        self.current_question = None
        self.game_over = False
        self.time_left = self.time_limit
        self.selected_answer_index = None
        self.final_stars = 0
        self.start_time = time.time()

    def load_next_question(self):
        
        if self.game_manager.question_index < len(self.game_manager.questions_pool):
            q_data = self.game_manager.questions_pool[self.game_manager.question_index]
            
            # Đảm bảo các lựa chọn là string để hiển thị, kể cả khi là số
            answers = [str(o) for o in q_data["options"]]
            correct_answer = str(q_data["answer"])
            random.shuffle(answers)

            self.current_question = {
                "question": q_data["question"],
                "answers": answers, 
                "correct_answer": correct_answer
            }
            try:
                self.current_question["correct_index"] = self.current_question["answers"].index(correct_answer)
            except ValueError:
                self.current_question["correct_index"] = -1
            
            self.game_manager.question_index += 1
            
            self.selected_answer_index = None
            self.show_feedback_until = 0
            self.answer_is_correct = False
            self.start_time = time.time()
            self.time_left = self.time_limit
        
        else:
            # Hết câu hỏi -> GAME OVER
            self.game_over = True
            self.final_stars = self.game_manager.calculate_stars(self.score)
            self.game_manager.save_score(self.score) 

    def handle_input(self, event):
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.game_over_button_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("LEVEL") 
            return 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # XỬ LÝ NÚT BACK (QUAY VỀ LEVEL SELECT)
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("LEVEL")
                return

            # XỬ LÝ NÚT SETTINGS
            if self.settings_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("SETTINGS") 
                return

            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        self.process_answer(i)
                        return

    def process_answer(self, selected_index):
        self.selected_answer_index = selected_index
        
        if selected_index >= 0:
            is_correct = (selected_index == self.current_question["correct_index"])
            self.answer_is_correct = is_correct
            
            if is_correct:
                self.score += POINTS_CORRECT 
            else:
                self.score += POINTS_WRONG 
        else: # Hết giờ
            self.answer_is_correct = False
            self.score += POINTS_WRONG 

        self.show_feedback_until = time.time() + 1.5 

    def update(self):
        if self.game_over:
            return

        current_time = time.time()
        
        if self.selected_answer_index is None:
            time_spent = current_time - self.start_time
            self.time_left = int(self.time_limit - time_spent)
            
            if self.time_left <= 0:
                self.time_left = 0
                self.process_answer(-2) 
        
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            self.load_next_question()
            
    def draw(self): 
        surface = self.game_manager._current_surface
        if surface is None:
            return
            
        self.button_rects = []
        
        # 0. VẼ NỀN CHÍNH
        surface.blit(self.assets['nen_chinh'], (0, 0))
        
        # 1. VẼ ĐIỂM SỐ VÀ TIMER
        if 'thanh_tiendo' in self.assets:
            tiendo_rect = self.assets['thanh_tiendo'].get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(self.assets['thanh_tiendo'], tiendo_rect)
            
            timer_color = COLOR_INFO if self.time_left > 5 else COLOR_WRONG
            timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
            timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(timer_text, timer_text_rect)

        # Cập nhật vị trí điểm số để nhường chỗ cho nút Settings
        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 120 - score_text.get_width(), 20)) 
        
        # 2. VẼ NÚT BACK/LEVEL SELECT
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        # 2b. VẼ NÚT SETTINGS
        surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft)
        
        # Thêm chữ "Cài đặt" nếu đang dùng fallback Surface
        if self.assets['is_settings_fallback']:
             setting_text = self.font_small.render("Cài đặt", True, COLOR_WHITE)
             setting_rect = setting_text.get_rect(center=self.settings_button_rect.center)
             surface.blit(setting_text, setting_rect)
        
        if not self.game_over and self.current_question:
            # 3. VẼ CÂU HỎI (Dùng nen_cauhoi)
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
            nen_dapan = self.assets['nen_dapan']
            
            x_pos_left = SCREEN_WIDTH // 2 - 250
            x_pos_right = SCREEN_WIDTH // 2 + 250 

            for i, answer in enumerate(self.current_question["answers"]):
                if i % 2 == 0: 
                    x_pos = x_pos_left
                    y_pos = self.answer_start_y + (i // 2) * self.answer_spacing
                else: 
                    x_pos = x_pos_right
                    y_pos = self.answer_start_y + (i // 2) * self.answer_spacing

                button_width, button_height = self.ANSWER_BUTTON_SIZE 
                button_rect = pygame.Rect(0, 0, button_width, button_height)
                button_rect.center = (x_pos, y_pos)
                self.button_rects.append(button_rect) 
                
                # --- XỬ LÝ MÀU ĐÁP ÁN ---
                temp_dapan_surf = nen_dapan.copy() 
                color_overlay = None

                if self.selected_answer_index is not None:
                    if i == self.current_question["correct_index"]:
                        color_overlay = COLOR_CORRECT
                    elif i == self.selected_answer_index:
                        color_overlay = COLOR_WRONG
                
                if color_overlay:
                    overlay_surf = pygame.Surface(temp_dapan_surf.get_size(), pygame.SRCALPHA)
                    overlay_surf.fill((color_overlay[0], color_overlay[1], color_overlay[2], 150))
                    temp_dapan_surf.blit(overlay_surf, (0, 0))
                
                # VẼ NỀN ĐÁP ÁN
                surface.blit(temp_dapan_surf, button_rect.topleft)
                
                # VẼ VĂN BẢN ĐÁP ÁN
                answer_display = f"{chr(65 + i)}. {answer}"
                answer_text = self.font_medium.render(answer_display, True, COLOR_TEXT) 
                answer_text_rect = answer_text.get_rect(center=button_rect.center) 
                surface.blit(answer_text, answer_text_rect)
            
        # 5. VẼ THÔNG BÁO GAME OVER
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            surface.blit(overlay, (0, 0))
            
            go_image = self.assets['game_over_image']
            go_rect = go_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            surface.blit(go_image, go_rect)
            
            # VẼ SAO ĐẠT ĐƯỢC
            star_asset = self.assets.get('sao_large', None)
            star_width = self.STAR_SIZE
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
                    
            # Nút Quay lại Menu (NEXT)
            if 'nut_next' in self.assets:
                surface.blit(self.assets['nut_next'], self.game_over_button_rect.topleft)
            else:
                pygame.draw.rect(surface, COLOR_CORRECT, self.game_over_button_rect, border_radius=10)