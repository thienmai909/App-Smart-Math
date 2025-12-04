import pygame
import os
import time
import random 
from src.screens.base_screen import BaseScreen
from src.config import * 
from data.save_manager import save_game_data 

LEVELS = [
    {"name": "LEVEL 1", "key": "LEVEL_1", "image_key": "lv1"},
    {"name": "LEVEL 2", "key": "LEVEL_2", "image_key": "lv2"},
    {"name": "LEVEL 3", "key": "LEVEL_3", "image_key": "lv3"},
    {"name": "LEVEL 4", "key": "LEVEL_4", "image_key": "lv4"},
    {"name": "LEVEL 5", "key": "LEVEL_5", "image_key": "lv5"},
    {"name": "LEVEL 6", "key": "LEVEL_6", "image_key": "lv6"},
]

VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'Sniglet-Regular.ttf')

# Kích thước cố định cho nút hành động 
PROGRESS_BAR_WIDTH = 400
PROGRESS_BAR_HEIGHT = 40
PROGRESS_BAR_PADDING = 5
ACTION_BUTTON_SIZE = (40, 40) 

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager) 

        # --- KHỞI TẠO FONT 
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
        self.STAR_BAR_SIZE = (300, 40)
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 20 - 40, 20, 40, 40) 
        
        self.GAME_OVER_BUTTON_SIZE = (250, 60) 
        self.game_over_button_rect = pygame.Rect(0, 0, *self.GAME_OVER_BUTTON_SIZE)
        
        self.score = 0
        self.best_score = 0 
        self.current_question = None 
        self.button_rects = [] 
        
        self.time_limit = TIME_LIMIT
        self.start_time = time.time()
        self.time_left = self.time_limit
        self.game_over = False
        self.final_stars = 0 

        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30) 
        self.answer_start_y = SCREEN_HEIGHT // 2 + 50 
        self.answer_spacing = 140       
        self.assets = self._load_assets() 
        
        self.game_over_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)

        
        self.timer_progress_rect = pygame.Rect(0, 0, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT)
        self.timer_progress_rect.center = (SCREEN_WIDTH // 2, 35) 
    
    def get_level_best_score(self, level_key):
        """Lấy điểm cao nhất của level hiện tại."""
        # Giả định game_data là dictionary lưu điểm: {"scores": {"LEVEL_1": {"high_score": 150}, ...}
        scores_data = self.game_manager.game_data.get('scores', {})
        if level_key in scores_data and "high_score" in scores_data[level_key]:
            return scores_data[level_key]["high_score"]
        return 0


    def calculate_stars(self, score):
        if MAX_SCORE_PER_LEVEL <= 0:
            return 0
        
        score_ratio = score / MAX_SCORE_PER_LEVEL
        
        sorted_thresholds = sorted(STAR_THRESHOLDS.items(), key=lambda item: item[0], reverse=True)
        
        for stars, threshold in sorted_thresholds:
            if score_ratio >= threshold:
                return stars
        return 0

    def save_score(self, new_score):
        if not self.game_manager.current_level_key:
            return

        current_data = self.game_manager.game_data.get('scores', {})
        current_stars = self.game_manager.game_data.get('stars', [0] * len(LEVELS))
        
        new_stars = self.calculate_stars(new_score)
        
        level_data = current_data.get(self.game_manager.current_level_key, {'high_score': 0})
        if new_score > level_data['high_score']:
            level_data['high_score'] = new_score
            current_data[self.game_manager.current_level_key] = level_data
        
        try:
            level_index = next(i for i, level in enumerate(LEVELS) if level['key'] == self.game_manager.current_level_key)
            if new_stars > current_stars[level_index]:
                current_stars[level_index] = new_stars
                self.game_manager.game_data['stars'] = current_stars
                
        except StopIteration:
            return
            
        self.game_manager.game_data['scores'] = current_data
        save_game_data(self.game_manager.game_data)

    def _load_assets(self):
        assets = {}
        assets['is_settings_fallback'] = False 
        try:
            # 1. NỀN MÀN HÌNH CHÍNH 
            try:
                assets['nen_chinh'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nenchinh.png')).convert()
                assets['nen_chinh'] = pygame.transform.scale(assets['nen_chinh'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)

            # 2. NỀN CÂU HỎI 
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nencauhoi.png')).convert_alpha()
            assets['nen_cauhoi'] = pygame.transform.scale(assets['nen_cauhoi'], (750, 200))
            
            # 3. NỀN ĐÁP ÁN 
            assets['nen_dapan'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nendapan.png')).convert_alpha()
            assets['nen_dapan'] = pygame.transform.scale(assets['nen_dapan'], self.ANSWER_BUTTON_SIZE)
            
            # 4. GAME OVER IMAGE 
            try:
                assets['game_over_image'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
                assets['game_over_image'] = pygame.transform.scale(assets['game_over_image'], (1200, 600)) 
            except pygame.error:
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)
                text_go = self.font_title.render("GAME OVER", True, COLOR_TITLE)
                text_score = self.font_large.render("Score", True, COLOR_TEXT)
                assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
                assets['game_over_image'].blit(text_score, text_score.get_rect(center=(200, 100)))

            # 5. NÚT SETTINGS 
            try:
                assets['nutcaidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha() 
                assets['nutcaidat'] = pygame.transform.scale(assets['nutcaidat'], (40, 40))
            except pygame.error:
                assets['nutcaidat'] = pygame.Surface((40, 40)); assets['nutcaidat'].fill(COLOR_INFO) 
                assets['is_settings_fallback'] = True
            
            self.settings_button_rect.size = assets['nutcaidat'].get_size()
            self.settings_button_rect.topright = (SCREEN_WIDTH - 20, 20) 

            # 6. NÚT NEXT 
            try:
                assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
                assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.GAME_OVER_BUTTON_SIZE)
            except pygame.error:
                assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
                
            # 7. THANH TIẾN ĐỘ 
            assets['thanh_tiendo'] = pygame.Surface((PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), pygame.SRCALPHA)
            assets['thanh_tiendo'].fill((50, 50, 50, 150)) 
            
            # 8. THANH SAO & SAO
            star_surf = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE), pygame.SRCALPHA)
            pygame.draw.polygon(star_surf, (255, 223, 0), [(25, 0), (33, 17), (50, 19), (38, 30), (41, 50), (25, 38), (9, 50), (12, 30), (0, 19), (17, 17)], 0)
            assets['sao_large'] = star_surf
            
            # Tải 4 thanh sao (0, 1, 2, 3)
            for i in range(4):
                    filename = None
                    if i == 0:
                        filename = None
                    else:
                        filename = f'thanh{i}sao.png'
                    
                    try:
                        if filename:
                            star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, filename)).convert_alpha()
                            assets[f'thanh_sao_{i}'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)
                        else:
                            raise FileNotFoundError 
                            
                    except (pygame.error, FileNotFoundError):
                        fallback_surf = pygame.Surface(self.STAR_BAR_SIZE, pygame.SRCALPHA)
                        fallback_surf.fill((200, 200, 200, 150))
                        assets[f'thanh_sao_{i}'] = fallback_surf
            
            try:
                assets['nut_back_icon'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
                assets['nut_back_icon'] = pygame.transform.scale(assets['nut_back_icon'], ACTION_BUTTON_SIZE)
            except pygame.error:
                assets['nut_back_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_back_icon'].fill(COLOR_ACCENT)

            try:
                assets['nut_play_icon'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_play.png')).convert_alpha()
                assets['nut_play_icon'] = pygame.transform.scale(assets['nut_play_icon'], ACTION_BUTTON_SIZE)
            except pygame.error:
                assets['nut_play_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_play_icon'].fill(COLOR_CORRECT)
                
        except pygame.error as e:
            # FALLBACK LỚN 
            assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)
            assets['nen_cauhoi'] = pygame.Surface((650, 150), pygame.SRCALPHA); assets['nen_cauhoi'].fill((255, 255, 255, 150))
            assets['nen_dapan'] = pygame.Surface(self.ANSWER_BUTTON_SIZE, pygame.SRCALPHA); assets['nen_dapan'].fill(COLOR_ACCENT) 
            assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
            assets['thanh_tiendo'] = pygame.Surface((300, 40)); assets['thanh_tiendo'].fill((200, 200, 200))
            assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA); 
            text_go = self.font_title.render("GAME OVER", True, COLOR_TITLE)
            assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
            assets['sao_large'] = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE)); assets['sao_large'].fill((255, 223, 0))
            assets['nutcaidat'] = pygame.Surface((80, 30)); assets['nutcaidat'].fill(COLOR_INFO) 
            assets['is_settings_fallback'] = True 
            for i in range(4):
                    assets[f'thanh_sao_{i}'] = pygame.Surface(self.STAR_BAR_SIZE); assets[f'thanh_sao_{i}'].fill((200, 200, 200))
        return assets

    def on_enter(self):
        """Khởi động trò chơi khi màn hình này được kích hoạt."""
        # Lấy điểm cao nhất cho level hiện tại
        if self.game_manager.current_level_key:
             self.best_score = self.get_level_best_score(self.game_manager.current_level_key)
        else:
             self.best_score = 0
             
        self.reset_game()
        self.load_next_question()

    def reset_game(self):
        self.score = 0
        self.current_question = None
        self.game_over = False
        self.time_left = self.time_limit
        self.selected_answer_index = None
        self.final_stars = 0
        self.start_time = time.time()
        self.game_manager.menu.show_setting = False
        

    def load_next_question(self):
        
        if self.game_manager.question_index < len(self.game_manager.questions_pool):
            q_data = self.game_manager.questions_pool[self.game_manager.question_index]
            
            answers = [str(o) for o in q_data["options"]]
            correct_answer = str(q_data["answer"])
            
            if "answer_index" not in q_data:
                 random.shuffle(answers)

            self.current_question = {
                "question": q_data["question"],
                "answers": answers, 
                "correct_answer": correct_answer,
                "question_number": self.game_manager.question_index + 1
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
            
            self.game_manager.question_index += 1
        
        else:
            self.game_over = True
            self.final_stars = self.calculate_stars(self.score)
            self.save_score(self.score) 
            

    def handle_input(self, event):   
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.game_manager.menu.show_settings:
                self.game_manager.menu.handle_input(event)
                return
            
            if self.game_over:
                if self.game_over_button_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("LEVEL") 
                    self.reset_game() 
                return 
            
            if self.settings_button_rect.collidepoint(mouse_pos):
                self.game_manager.menu.show_settings = True 
                return

            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        self.process_answer(i)
                        return

    def process_answer(self, selected_index):
        if selected_index >= 0 and self.game_manager.sounds['click'] and self.game_manager.menu.sound_setting:
            self.game_manager.sounds['click'].play()
             
        self.selected_answer_index = selected_index
        
        if selected_index >= 0:
            is_correct = (selected_index == self.current_question["correct_index"])
            self.answer_is_correct = is_correct
            
            if is_correct:
                self.score += POINTS_CORRECT 
                if self.game_manager.sounds['yes'] and self.game_manager.menu.sound_setting:
                     self.game_manager.sounds['yes'].play()
            else:
                self.score = max(0, self.score + POINTS_WRONG)
                if self.game_manager.sounds['no'] and self.game_manager.menu.sound_setting:
                     self.game_manager.sounds['no'].play()
        else:
            self.answer_is_correct = False
            self.score = max(0, self.score + POINTS_WRONG)
            if self.game_manager.sounds['no'] and self.game_manager.menu.sound_setting:
                 self.game_manager.sounds['no'].play()

        self.show_feedback_until = time.time() + 1.5 

    def update(self):
        if self.game_manager.menu.show_settings:            
            # Điều khiển âm thanh
            self.game_manager.menu.update()

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

    def _draw_settings_popup(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        surface.blit(overlay, (0, 0))   
        
        surface.blit(self.assets['nen_caidat'], self.settings_rect.topleft)
        
        sound_icon = self.assets['on'] if self.sound_on else self.assets['off']
        sound_icon_rect = sound_icon.get_rect(midright=(self.settings_rect.right - 40, self.sound_rect.centery))
        surface.blit(sound_icon, sound_icon_rect.topleft)

        bgm_icon = self.assets['on'] if self.bgm_on else self.assets['off']
        bgm_icon_rect = bgm_icon.get_rect(midright=(self.settings_rect.right - 40, self.bgm_rect.centery))
        surface.blit(bgm_icon, bgm_icon_rect.topleft)

        if 'nut_back_icon' in self.assets:
            icon_asset = self.assets['nut_back_icon']
            icon_rect = icon_asset.get_rect(midright=(self.home_rect.right - 5, self.home_rect.centery))
            surface.blit(icon_asset, icon_rect.topleft)

        if 'nut_play_icon' in self.assets:
            icon_asset = self.assets['nut_play_icon']
            icon_rect = icon_asset.get_rect(midright=(self.replay_rect.right - 5, self.replay_rect.centery))
            surface.blit(icon_asset, icon_rect.topleft)

        pygame.draw.circle(surface, COLOR_WRONG, self.close_rect.center, 15)
        close_text = self.font_small.render("X", True, COLOR_WHITE)
        close_text_rect = close_text.get_rect(center=self.close_rect.center)
        surface.blit(close_text, close_text_rect)

    def draw(self, surface):      
        self.button_rects = []
        
        # 0. VẼ NỀN CHÍNH
        surface.blit(self.assets['nen_chinh'], (0, 0))
        
        # 1. VẼ ĐIỂM SỐ VÀ TIMER 
     
        # VẼ THỜI GIAN CÒN LẠI (SỐ GIÂY) - Center Top
        timer_text_content = self.font_large.render(f"Thời gian:{self.time_left}", True, COLOR_ACCENT) 
        timer_text_rect = timer_text_content.get_rect(center=(SCREEN_WIDTH // 2, 35)) 
        surface.blit(timer_text_content, timer_text_rect)
        
        # VẼ ĐIỂM SỐ HIỆN TẠI (Top Left)
        score_label = self.font_small.render(f"ĐIỂM: {self.score}", True, COLOR_BLACK) 
        score_label_rect = score_label.get_rect(topleft=(20, 20))
        surface.blit(score_label, score_label_rect.topleft) 

        # 2. VẼ NÚT SETTINGS
        surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft)       
        if self.assets['is_settings_fallback']:
             setting_text = self.font_small.render("Cài đặt", True, COLOR_WHITE)
             setting_rect = setting_text.get_rect(center=self.settings_button_rect.center)
             surface.blit(setting_text, setting_rect)

        # 3. VẼ CÂU HỎI
        if not self.game_over and self.current_question:
            if 'nen_cauhoi' in self.assets: 
                question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
                surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
                question_rect_center = question_bg_rect.center
            else:
                question_rect_center = self.question_pos
            question_num = self.current_question.get("question_number", self.game_manager.question_index)
            question_content = self.current_question["question"]
            
            # Màu chữ câu hỏi là màu đen
            bold_text = f"Câu {question_num}: "
            bold_surface = self.font_large.render(bold_text, True, COLOR_BLACK) 
            content_surface = self.font_large.render(question_content, True, COLOR_BLACK)            
            total_width = bold_surface.get_width() + content_surface.get_width()
            start_x = question_rect_center[0] - total_width // 2
            start_y = question_rect_center[1]           
            bold_rect = bold_surface.get_rect(midleft=(start_x, start_y))
            surface.blit(bold_surface, bold_rect.topleft)
            content_rect = content_surface.get_rect(midleft=(bold_rect.right, start_y))
            surface.blit(content_surface, content_rect.topleft)

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
                surface.blit(temp_dapan_surf, button_rect.topleft)               
                # Màu chữ đáp án là màu đen, chỉ giữ lại đáp án
                answer_text = self.font_medium.render(f"{answer}", True, COLOR_BLACK) 
                answer_text_rect = answer_text.get_rect(center=button_rect.center) 
                surface.blit(answer_text, answer_text_rect)
            
        # 5. VẼ THÔNG BÁO GAME OVER
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            surface.blit(overlay, (0, 0))          
            go_image = self.assets['game_over_image']
            go_rect = go_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
            surface.blit(go_image, go_rect)
            
            # --- HIỂN THỊ ĐIỂM HIỆN TẠI ---
            current_score_label = self.font_large.render("", True, COLOR_BLACK)
            current_score_value = self.font_title.render(f"{self.score}", True, COLOR_BLACK)           
            current_score_label_rect = current_score_label.get_rect(center=(SCREEN_WIDTH // 2, go_rect.centery - 90 )) 
            current_score_value_rect = current_score_value.get_rect(center=(SCREEN_WIDTH // 2, current_score_label_rect.bottom + 40))      
            surface.blit(current_score_label, current_score_label_rect.topleft)
            surface.blit(current_score_value, current_score_value_rect.topleft)
            
            # --- HIỂN THỊ ĐIỂM CAO NHẤT ---
            best_score_label = self.font_large.render("", True, COLOR_BLACK)
            best_score_value = self.font_title.render(f"{self.best_score}", True, COLOR_BLACK)
            best_score_label_rect = best_score_label.get_rect(center=(SCREEN_WIDTH // 2, current_score_value_rect.bottom + 90))
            best_score_value_rect = best_score_value.get_rect(center=(SCREEN_WIDTH // 2, best_score_label_rect.bottom -20))
            surface.blit(best_score_label, best_score_label_rect.topleft)
            surface.blit(best_score_value, best_score_value_rect.topleft)

            # Nút Quay lại Home (NEXT) 
            if 'nut_next' in self.assets:
                nut_next_rect = self.assets['nut_next'].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                surface.blit(self.assets['nut_next'], nut_next_rect.topleft)
                self.game_over_button_rect.topleft = nut_next_rect.topleft 
            else:
                pygame.draw.rect(surface, COLOR_CORRECT, self.game_over_button_rect, border_radius=0)

        # 7. VẼ POP-UP CÀI ĐẶT
        if self.game_manager.menu.show_settings:
            self.game_manager.menu.draw(surface)