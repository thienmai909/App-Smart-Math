import pygame
import os
import time
import random 
from src.screens.base_screen import BaseScreen
from src.config import *
from data.save_manager import save_game_data 

# Danh sách các cấp độ
LEVELS = [
    {"name": "LEVEL 1", "key": "LEVEL_1", "image_key": "lv1"},
    {"name": "LEVEL 2", "key": "LEVEL_2", "image_key": "lv2"},
    {"name": "LEVEL 3", "key": "LEVEL_3", "image_key": "lv3"},
    {"name": "LEVEL 4", "key": "LEVEL_4", "image_key": "lv4"},
    {"name": "LEVEL 5", "key": "LEVEL_5", "image_key": "lv5"},
    {"name": "LEVEL 6", "key": "LEVEL_6", "image_key": "lv6"},
]

VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'Nunito-ExtraBold.ttf')

# Kích thước cố định cho nút hành động 
PROGRESS_BAR_WIDTH = 400
PROGRESS_BAR_HEIGHT = 40
PROGRESS_BAR_PADDING = 5
ACTION_BUTTON_SIZE = (40, 40) 

# --- KHAI BÁO FONT CHO CÂU HỎI ---
QUESTION_FONT_FILE = 'Nunito-ExtraBold.ttf' 
QUESTION_FONT_PATH = os.path.join(ASSETS_FONT_DIR, QUESTION_FONT_FILE)

# --- KHAI BÁO FONT MỚI CHO ĐIỂM SỐ/THỜI GIAN ---
SCORE_TIMER_FONT_FILE = 'Pacific.ttf'
SCORE_TIMER_FONT_PATH = os.path.join(ASSETS_FONT_DIR, SCORE_TIMER_FONT_FILE)

# --- ĐỊNH NGHĨA TỶ LỆ SAO ---
STAR_THRESHOLDS = {
    3: 0.95, 
    2: 0.75, 
    1: 0.50, 
    0: 0.00
}

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
                
                if os.path.exists(SCORE_TIMER_FONT_PATH):
                    self.font_score_timer = pygame.font.Font(SCORE_TIMER_FONT_PATH, FONT_SIZE_LARGE + 10) 
                else:
                    self.font_score_timer = self.font_large 
                
                if os.path.exists(QUESTION_FONT_PATH):
                    self.font_question = pygame.font.Font(QUESTION_FONT_PATH, FONT_SIZE_LARGE) 
                else:
                    self.font_question = self.font_large 
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
                self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
                self.font_score_timer = self.font_large
                self.font_question = self.font_large
        except pygame.error:
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
            self.font_score_timer = self.font_large
            self.font_question = self.font_large
        
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
        self.PROGRESS_FILL_PADDING = 3 

    def get_level_best_score(self, level_key):
        scores_data = self.game_manager.game_data.get('scores', {})
        if level_key in scores_data and "high_score" in scores_data[level_key]:
            return scores_data[level_key]["high_score"]
        return 0

    def calculate_stars(self, score):
        if 'MAX_SCORE_PER_LEVEL' not in globals() or MAX_SCORE_PER_LEVEL <= 0:
            return 0
        score_ratio = score / MAX_SCORE_PER_LEVEL
        sorted_thresholds = sorted(STAR_THRESHOLDS.items(), key=lambda item: item[1], reverse=True)
        for stars, threshold in sorted_thresholds:
            if score_ratio >= threshold:
                return min(stars, 3) 
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
            pass
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
            assets['nen_cauhoi'] = pygame.transform.scale(assets['nen_cauhoi'], (950, 200))
            
            # 3. NỀN ĐÁP ÁN 
            assets['nen_dapan'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nendapan.png')).convert_alpha()
            assets['nen_dapan'] = pygame.transform.scale(assets['nen_dapan'], self.ANSWER_BUTTON_SIZE)
            
            # 4. GAME OVER IMAGE 
            try:
                assets['game_over_image'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
                assets['game_over_image'] = pygame.transform.scale(assets['game_over_image'], (1200, 600)) 
            except pygame.error:
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)

            # 5. NÚT SETTINGS 
            try:
                assets['nutcaidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha() 
                assets['nutcaidat'] = pygame.transform.scale(assets['nutcaidat'], (45, 45))
            except pygame.error:
                assets['nutcaidat'] = pygame.Surface((45, 45)); assets['nutcaidat'].fill(COLOR_INFO) 

            # 6. KHUNG TIME THEO YÊU CẦU
            try:
                assets['khung_time'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'khung_time.png')).convert_alpha()
                assets['khung_time'] = pygame.transform.scale(assets['khung_time'], (140, 50))
            except:
                assets['khung_time'] = pygame.Surface((140, 50), pygame.SRCALPHA)
                pygame.draw.rect(assets['khung_time'], (255, 255, 255, 100), assets['khung_time'].get_rect(), border_radius=10)

            # 7. NÚT NEXT (Quay lại)
            try:
                assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
                assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.GAME_OVER_BUTTON_SIZE)
            except pygame.error:
                assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
                
            # 8. THANH TIẾN ĐỘ (Nền)
            assets['thanh_tiendo'] = pygame.Surface((PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), pygame.SRCALPHA)
            assets['thanh_tiendo'].fill((50, 50, 50, 150)) 
            
            # 9. SAO
            try:
                star_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha() 
                assets['sao_large'] = pygame.transform.scale(star_img, (self.STAR_SIZE, self.STAR_SIZE))
            except pygame.error:
                assets['sao_large'] = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE))

            # 10. THANH SAO (0, 1, 2, 3) 
            for i in range(4):
                filename = 'thanh_tiendo.png' if i == 0 else f'thanh{i}sao.png'
                try:
                    star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, filename)).convert_alpha()
                    assets[f'thanh_sao_{i}'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)
                except:
                    assets[f'thanh_sao_{i}'] = pygame.Surface(self.STAR_BAR_SIZE, pygame.SRCALPHA)

        except pygame.error:
            pass # Fallback đã xử lý trong từng bước
            
        return assets

    def on_enter(self):
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
        self.game_manager.menu.show_settings = False 

    def load_next_question(self):
        if self.game_manager.question_index < len(self.game_manager.questions_pool):
            q_data = self.game_manager.questions_pool[self.game_manager.question_index]
            answers = [str(o) for o in q_data["options"]]
            correct_answer = str(q_data["answer"])
            if "answer_index" not in q_data:
                random.shuffle(answers)

            self.current_question = {
                "prefix": q_data.get("prefix", "Hãy trả lời câu hỏi sau:"), 
                "question": q_data["question"],
                "answers": answers, 
                "correct_answer": correct_answer,
                "question_number": self.game_manager.question_index + 1
            }
            try:
                self.current_question["correct_index"] = self.current_question["answers"].index(correct_answer)
            except ValueError:
                self.game_manager.question_index += 1
                self.load_next_question() 
                return
            
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
        if selected_index >= 0 and self.game_manager.sounds and 'click' in self.game_manager.sounds and self.game_manager.menu.sound_setting:
            self.game_manager.sounds['click'].play()
        self.selected_answer_index = selected_index
        if selected_index >= 0:
            is_correct = (selected_index == self.current_question["correct_index"])
            self.answer_is_correct = is_correct
            if is_correct:
                self.score += POINTS_CORRECT 
                if self.game_manager.sounds and 'yes' in self.game_manager.sounds and self.game_manager.menu.sound_setting:
                    self.game_manager.sounds['yes'].play()
            else:
                self.score = max(0, self.score + POINTS_WRONG)
                if self.game_manager.sounds and 'no' in self.game_manager.sounds and self.game_manager.menu.sound_setting:
                    self.game_manager.sounds['no'].play()
        else: 
            self.answer_is_correct = False
            self.score = max(0, self.score + POINTS_WRONG)
            if self.game_manager.sounds and 'no' in self.game_manager.sounds and self.game_manager.menu.sound_setting:
                self.game_manager.sounds['no'].play()
        self.show_feedback_until = time.time() + 1.5 

    def update(self):
        if self.game_manager.menu.show_settings:
            self.game_manager.menu.update()
            return
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
            
    def draw(self, surface):
        self.button_rects = []
        surface.blit(self.assets['nen_chinh'], (0, 0))
        
        # --- BỐ CỤC TOP BAR THEO YÊU CẦU ---

        # 1. BÊN PHẢI: Nút Cài đặt và Khung Thời gian
        self.settings_button_rect.topright = (SCREEN_WIDTH - 20, 20)
        surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft)
        
        # Khung thời gian (Nằm sát bên trái nút cài đặt)
        time_frame_rect = self.assets['khung_time'].get_rect(right=self.settings_button_rect.left - 10, centery=self.settings_button_rect.centery)
        surface.blit(self.assets['khung_time'], time_frame_rect.topleft)
        
        # Chữ thời gian và nhãn "TG:"
        timer_text_content = self.font_score_timer.render(f"{self.time_left}", True, COLOR_ACCENT) 
        timer_text_rect = timer_text_content.get_rect(center=time_frame_rect.center)
        surface.blit(timer_text_content, timer_text_rect.topleft)
        
        time_label = self.font_large.render("Thời gian:", True, COLOR_ACCENT)
        surface.blit(time_label, time_label.get_rect(right=time_frame_rect.left - 5, centery=time_frame_rect.centery))

        # 2. CHÍNH GIỮA: Thanh tiến độ
        progress_bar_bg = self.assets.get('thanh_sao_0', self.assets.get('thanh_tiendo'))
        bar_rect = progress_bar_bg.get_rect(center=(SCREEN_WIDTH // 2, self.settings_button_rect.centery))
        surface.blit(progress_bar_bg, bar_rect.topleft)

        # Vẽ phần lấp đầy thanh tiến độ
        current_score_ratio = min(1.0, self.score / MAX_SCORE_PER_LEVEL) if MAX_SCORE_PER_LEVEL > 0 else 0
        fill_width_max = bar_rect.width - (2 * self.PROGRESS_FILL_PADDING)
        fill_width = int(fill_width_max * current_score_ratio)
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_rect.x + self.PROGRESS_FILL_PADDING, bar_rect.y + self.PROGRESS_FILL_PADDING, fill_width, bar_rect.height - (2 * self.PROGRESS_FILL_PADDING))
            pygame.draw.rect(surface, (255, 223, 0), fill_rect) 

        # 3. BÊN TRÁI: Điểm cao (Đặt sau vị trí vương miện)
        # crown_x_offset: Khoảng cách để dành cho icon vương miện (ví dụ 80px từ lề trái)
        crown_x_offset = 80 
        best_score_label = self.font_large.render("", True, COLOR_ACCENT) 
        best_score_label_rect = best_score_label.get_rect(left=crown_x_offset, centery=bar_rect.centery)
        surface.blit(best_score_label, best_score_label_rect.topleft)

        best_score_value = self.font_score_timer.render(f"{self.best_score}", True, COLOR_ACCENT)
        surface.blit(best_score_value, (best_score_label_rect.right + 20, best_score_label_rect.y + 10))

        # --- PHẦN CÂU HỎI VÀ ĐÁP ÁN ---
        if not self.game_over and self.current_question:
            q_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
            surface.blit(self.assets['nen_cauhoi'], q_bg_rect)
            
            question_num = self.current_question.get("question_number")
            prefix_full_text = f"Câu {question_num}: {self.current_question.get('prefix')}"
            prefix_surface = self.font_question.render(prefix_full_text, True, COLOR_BLACK) 
            content_surface = self.font_question.render(self.current_question["question"], True, COLOR_BLACK)
            
            surface.blit(prefix_surface, prefix_surface.get_rect(center=(q_bg_rect.centerx, q_bg_rect.centery - 25)))
            surface.blit(content_surface, content_surface.get_rect(center=(q_bg_rect.centerx, q_bg_rect.centery + 25)))

            # Vẽ 4 đáp án
            nen_dapan = self.assets['nen_dapan']
            for i, answer in enumerate(self.current_question["answers"]):
                x_pos = SCREEN_WIDTH // 2 - 250 if i % 2 == 0 else SCREEN_WIDTH // 2 + 250
                y_pos = self.answer_start_y + (i // 2) * self.answer_spacing
                button_rect = pygame.Rect(0, 0, *self.ANSWER_BUTTON_SIZE)
                button_rect.center = (x_pos, y_pos)
                self.button_rects.append(button_rect) 
                
                temp_dapan_surf = nen_dapan.copy() 
                if self.selected_answer_index is not None:
                    color_overlay = None
                    if i == self.current_question["correct_index"]: color_overlay = COLOR_CORRECT
                    elif i == self.selected_answer_index: color_overlay = COLOR_WRONG
                    if color_overlay:
                        overlay_surf = pygame.Surface(temp_dapan_surf.get_size(), pygame.SRCALPHA)
                        overlay_surf.fill((*color_overlay, 150))
                        temp_dapan_surf.blit(overlay_surf, (0, 0))
                
                surface.blit(temp_dapan_surf, button_rect.topleft)
                label = chr(65 + i)
                answer_text = self.font_medium.render(f"{label}. {answer}", True, COLOR_BLACK) 
                surface.blit(answer_text, answer_text.get_rect(center=button_rect.center))

        # --- MÀN HÌNH KẾT THÚC ---
        if self.game_over:
            # Làm mờ nền
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200)); surface.blit(overlay, (0, 0))
            
            # Ảnh Game Over
            go_rect = self.assets['game_over_image'].get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            surface.blit(self.assets['game_over_image'], go_rect)
            
            # Vẽ SAO dựa trên final_stars
            star_start_x = SCREEN_WIDTH // 2 - 120
            for i in range(1, 4):
                s_img = pygame.transform.scale(self.assets['s_img' if 's_img' in self.assets else 'sao_img'], (80, 80))
                if i > self.final_stars:
                    # Tạo sao tối nếu chưa đạt mốc
                    dark = pygame.Surface(s_img.get_size(), pygame.SRCALPHA); dark.fill((40, 40, 40, 200))
                    s_img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                surface.blit(s_img, (star_start_x + (i-1)*90, go_rect.centery + 100))

            # Điểm số và Nút Quay lại
            sc_txt = self.font_title.render(f"ĐIỂM: {self.score}", True, (255, 255, 255))
            surface.blit(sc_txt, sc_txt.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery - 20)))
            
            btn_next = self.assets['nut_next'].get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 80))
            surface.blit(self.assets['nut_next'], btn_next)
            self.game_over_button_rect.topleft = btn_next.topleft
            surface.blit(self.font_medium.render("", True, (255,255,255)), (btn_next.centerx-50, btn_next.centery-15))

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if self.game_over:
                if self.game_over_button_rect.collidepoint(pos): self.game_manager.switch_screen("LEVEL")
            elif self.settings_button_rect.collidepoint(pos):
                self.game_manager.menu.show_settings = True
            elif self.selected_answer_index is None:
                for i, r in enumerate(self.button_rects):
                    if r.collidepoint(pos): self.process_answer(i)