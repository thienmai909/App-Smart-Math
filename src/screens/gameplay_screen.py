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
# Sử dụng font Nunito-ExtraBold đã được chọn
QUESTION_FONT_FILE = 'Nunito-ExtraBold.ttf' 
QUESTION_FONT_PATH = os.path.join(ASSETS_FONT_DIR, QUESTION_FONT_FILE)

# --- KHAI BÁO FONT MỚI CHO ĐIỂM SỐ/THỜI GIAN ---
SCORE_TIMER_FONT_FILE = 'Pacific.ttf'
SCORE_TIMER_FONT_PATH = os.path.join(ASSETS_FONT_DIR, SCORE_TIMER_FONT_FILE)
# --------------------------------------------------

# --- ĐỊNH NGHĨA TỶ LỆ SAO ---
STAR_THRESHOLDS = {
    3: 0.95, 
    2: 0.75, 
    1: 0.50, 
    0: 0.00
}
# MAX_SCORE_PER_LEVEL (Cần được định nghĩa trong src.config)

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
        
        # --- Cấu hình Padding cho thanh tiến trình ---
        self.PROGRESS_FILL_PADDING = 3 # Giảm padding để fit hơn với viền
        
        # --- Vị trí mới cho bố cục ---
        self.top_padding = 20
    
    def get_level_best_score(self, level_key):
        """Lấy điểm cao nhất của level hiện tại."""
        scores_data = self.game_manager.game_data.get('scores', {})
        if level_key in scores_data and "high_score" in scores_data[level_key]:
            return scores_data[level_key]["high_score"]
        return 0


    def calculate_stars(self, score):
        # Đảm bảo MAX_SCORE_PER_LEVEL được định nghĩa và lớn hơn 0
        if 'MAX_SCORE_PER_LEVEL' not in globals() or MAX_SCORE_PER_LEVEL <= 0:
            return 0
        
        score_ratio = score / MAX_SCORE_PER_LEVEL
        
        # Sử dụng STAR_THRESHOLDS 
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
            pass # Không tìm thấy level
            
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

            # 6. NÚT NEXT (Quay lại)
            try:
                assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
                assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.GAME_OVER_BUTTON_SIZE)
            except pygame.error:
                assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
                
            # 7. THANH TIẾN ĐỘ (Nền)
            assets['thanh_tiendo'] = pygame.Surface((PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), pygame.SRCALPHA)
            assets['thanh_tiendo'].fill((50, 50, 50, 150)) 
            
            # 8. THANH SAO & SAO
            try:
                star_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha() 
                assets['sao_large'] = pygame.transform.scale(star_img, (self.STAR_SIZE, self.STAR_SIZE))
            except pygame.error:
                # Fallback cho sao
                star_surf = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE), pygame.SRCALPHA)
                pygame.draw.polygon(star_surf, (255, 223, 0), [(25, 0), (33, 17), (50, 19), (38, 30), (41, 50), (25, 38), (9, 50), (12, 30), (0, 19), (17, 17)], 0)
                assets['sao_large'] = star_surf


            # Tải 4 thanh sao (0, 1, 2, 3) 
            for i in range(4):
                filename = None
                if i == 0:
                    filename = 'thanh_tiendo.png' 
                else:
                    filename = f'thanh{i}sao.png'
                
                try:
                    if filename and os.path.exists(os.path.join(ASSETS_IMG_DIR, filename)):
                        star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, filename)).convert_alpha()
                        assets[f'thanh_sao_{i}'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)
                    else:
                        raise FileNotFoundError 
                        
                except (pygame.error, FileNotFoundError):
                    # Fallback cho thanh sao (Dùng thanh tiến độ trơn)
                    fallback_surf = pygame.Surface(self.STAR_BAR_SIZE, pygame.SRCALPHA)
                    fallback_color = (100, 100, 100, 150) 
                    fallback_surf.fill(fallback_color)
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
            for i in range(4):
                    assets[f'thanh_sao_{i}'] = pygame.Surface(self.STAR_BAR_SIZE); assets[f'thanh_sao_{i}'].fill((200, 200, 200))
            
        return assets

    def on_enter(self):
        """Khởi động trò chơi khi màn hình này được kích hoạt."""
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
        # Đảm bảo bạn có biến 'show_settings' trong menu
        self.game_manager.menu.show_settings = False 
        

    def load_next_question(self):
        
        if self.game_manager.question_index < len(self.game_manager.questions_pool):
            q_data = self.game_manager.questions_pool[self.game_manager.question_index]
            
            answers = [str(o) for o in q_data["options"]]
            correct_answer = str(q_data["answer"])
            
            # Trộn đáp án nếu cần
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
                # Xử lý nếu đáp án đúng không có trong options (Lỗi dữ liệu)
                print(f"Lỗi: Không tìm thấy đáp án đúng '{correct_answer}' trong options: {answers}")
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
                # Nút Quay lại/NEXT
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
        # Phát âm thanh click chung (nếu có)
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
        else: # Hết giờ (selected_index = -2)
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
                self.process_answer(-2) # -2 là đại diện cho hết giờ
                
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            self.load_next_question()
            
    def draw(self, surface):
        self.button_rects = []
        
        # 0. VẼ NỀN CHÍNH
        surface.blit(self.assets['nen_chinh'], (0, 0))
        
        # --- BỐ CỤC TOP BAR ---

        # 1. VẼ NÚT SETTINGS (Top Right)
        surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft) 
        if self.assets['is_settings_fallback']:
            setting_text = self.font_small.render("Cài đặt", True, COLOR_WHITE)
            setting_rect = setting_text.get_rect(center=self.settings_button_rect.center)
            surface.blit(setting_text, setting_rect)
        
        # 2. VẼ THANH TIẾN TRÌNH VÀ SAO (Bên trái nút settings)
        
        # 2A. VẼ NỀN THANH TIẾN TRÌNH CƠ BẢN (thanh_sao_0)
        progress_bar_bg = self.assets.get('thanh_sao_0', self.assets.get('thanh_tiendo'))
        
        # Đặt vị trí thanh tiến trình 
        bar_rect = progress_bar_bg.get_rect(right=self.settings_button_rect.left - 20, centery=self.settings_button_rect.centery)
        surface.blit(progress_bar_bg, bar_rect.topleft)

        # 2B. TÍNH TOÁN VÀ VẼ TIẾN ĐỘ (Lấp đầy)
        current_score_ratio = 0
        # Đảm bảo MAX_SCORE_PER_LEVEL được định nghĩa
        if 'MAX_SCORE_PER_LEVEL' in globals() and MAX_SCORE_PER_LEVEL > 0:
            current_score_ratio = min(1.0, self.score / MAX_SCORE_PER_LEVEL)
            
        PADDING = self.PROGRESS_FILL_PADDING 
        fill_width_max = bar_rect.width - (2 * PADDING)
        fill_width = int(fill_width_max * current_score_ratio)
        
        fill_color = (255, 223, 0) # Màu vàng/gold
        
        fill_rect = pygame.Rect(bar_rect.x + PADDING, bar_rect.y + PADDING, 
                                 fill_width, bar_rect.height - (2 * PADDING))
        
        if fill_width > 0:
            pygame.draw.rect(surface, fill_color, fill_rect) 

        # 2C. VẼ NGƯỠNG SAO
        star_image = self.assets.get('sao_large')
        if star_image:
            star_size = 20
            scaled_star = pygame.transform.scale(star_image, (star_size, star_size))
            
            star_threshold_data = {
                1: STAR_THRESHOLDS.get(1, 0.50), 
                2: STAR_THRESHOLDS.get(2, 0.75), 
                3: STAR_THRESHOLDS.get(3, 0.95), 
            }
            
            for stars, ratio in star_threshold_data.items():
                star_center_x_absolute = bar_rect.x + PADDING + int(fill_width_max * ratio)
                
                # Kiểm tra điều kiện: Vẽ sao nếu điểm đã đạt ngưỡng 
                if fill_rect.x + fill_width >= star_center_x_absolute: 
                    star_rect = scaled_star.get_rect(center=(star_center_x_absolute, bar_rect.centery))
                    surface.blit(scaled_star, star_rect.topleft)

        # 3. VẼ BEST SCORE (Left Top, bên trái Thanh tiến trình)
        best_score_value = self.font_score_timer.render(f"{self.best_score}", True, COLOR_ACCENT)
        best_score_value_rect = best_score_value.get_rect(right=bar_rect.left - 20, centery=bar_rect.centery) 
        surface.blit(best_score_value, best_score_value_rect.topleft)
        
        best_score_label = self.font_large.render("ĐIỂM CAO:", True, COLOR_ACCENT) 
        best_score_label_rect = best_score_label.get_rect(right=best_score_value_rect.left - 5, centery=best_score_value_rect.centery)
        surface.blit(best_score_label, best_score_label_rect.topleft)

        # 4. VẼ THỜI GIAN CÒN LẠI (Left Top)
        time_label = self.font_large.render("TG:", True, COLOR_ACCENT)
        time_label_rect = time_label.get_rect(topleft=(20, 20))
        surface.blit(time_label, time_label_rect.topleft)
        
        timer_text_content = self.font_score_timer.render(f"{self.time_left}", True, COLOR_ACCENT) 
        timer_text_rect = timer_text_content.get_rect(left=time_label_rect.right + 5, centery=time_label_rect.centery) 
        surface.blit(timer_text_content, timer_text_rect.topleft)
        
        # 5. VẼ CÂU HỎI & ĐÁP ÁN (Chỉ khi game đang chạy)
        if not self.game_over and self.current_question:
            # Vẽ nền câu hỏi
            if 'nen_cauhoi' in self.assets: 
                question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
                surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
                question_rect_center = question_bg_rect.center
            else:
                question_rect_center = self.question_pos
            
            question_num = self.current_question.get("question_number", self.game_manager.question_index)
            question_content = self.current_question["question"]
            question_prefix = self.current_question.get("prefix", "Hãy tính toán phép toán sau:")
            
            # --- TẠO VÀ VẼ CÂU HỎI 
            prefix_full_text = f"Câu {question_num}: {question_prefix}"
            prefix_surface = self.font_question.render(prefix_full_text, True, COLOR_BLACK) 
            content_surface = self.font_question.render(question_content, True, COLOR_BLACK)
            line_height = prefix_surface.get_height()
            
            center_y = question_rect_center[1]
            prefix_y = center_y - line_height // 2 - 20
            content_y = center_y + line_height // 2 + 10

            # VẼ PHẦN MỞ ĐẦU (Dòng 1)
            prefix_rect = prefix_surface.get_rect(center=(question_rect_center[0], prefix_y))
            surface.blit(prefix_surface, prefix_rect.topleft)
            
            # VẼ PHẦN PHÉP TOÁN (Dòng 2)
            content_rect = content_surface.get_rect(center=(question_rect_center[0], content_y))
            surface.blit(content_surface, content_rect.topleft)

            # 6. VẼ 4 ĐÁP ÁN
            nen_dapan = self.assets['nen_dapan']
            x_pos_left = SCREEN_WIDTH // 2 - 250
            x_pos_right = SCREEN_WIDTH // 2 + 250 
            self.button_rects = [] # Reset button rects
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
                
                # --- THÊM NHÃN A, B, C, D VÀO TRƯỚC ĐÁP ÁN ---
                label = chr(65 + i)
                full_answer_content = f"{label}. {answer}"
                answer_text = self.font_medium.render(full_answer_content, True, COLOR_BLACK) 
                answer_text_rect = answer_text.get_rect(center=button_rect.center) 
                surface.blit(answer_text, answer_text_rect)
            
        # 7. VẼ THÔNG BÁO GAME OVER
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            surface.blit(overlay, (0, 0)) 
            
            # Nền game over
            go_image = self.assets['game_over_image']
            go_rect = go_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
            surface.blit(go_image, go_rect)
            
            # --- HIỂN THỊ SỐ SAO ĐẠT ĐƯỢC ---
            star_size_final = 60
            final_star_image = pygame.transform.scale(self.assets.get('sao_large'), (star_size_final, star_size_final))
            star_spacing = star_size_final + 10
            total_width = 3 * star_size_final + 2 * 10
            start_x = SCREEN_WIDTH // 2 - total_width // 2
            
            for i in range(3):
                star_x = start_x + i * star_spacing
                star_y = go_rect.centery + 100
                star_rect = final_star_image.get_rect(topleft=(star_x, star_y))
                
                # Tô màu sao (Vàng nếu đạt, Xám nếu không)
                if i < self.final_stars:
                    surface.blit(final_star_image, star_rect.topleft)
                else:
                    # Tạo phiên bản xám của sao (Tối ưu: nên tạo sẵn asset)
                    gray_star = final_star_image.copy()
                    # Vẽ một lớp phủ xám lên trên để làm mờ hiệu ứng vàng
                    gray_color = (100, 100, 100, 200) 
                    gray_surf = pygame.Surface(gray_star.get_size(), pygame.SRCALPHA)
                    gray_surf.fill(gray_color)
                    gray_star.blit(gray_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    
                    surface.blit(gray_star, star_rect.topleft)

            # --- HIỂN THỊ ĐIỂM KẾT THÚC ---
            current_score_label = self.font_large.render("ĐIỂM SỐ CỦA BẠN:", True, COLOR_TEXT)
            current_score_value = self.font_title.render(f"{self.score}", True, COLOR_TITLE)
            
            current_score_value_rect = current_score_value.get_rect(center=(SCREEN_WIDTH // 2, go_rect.centery - 20))
            current_score_label_rect = current_score_label.get_rect(center=(SCREEN_WIDTH // 2, current_score_value_rect.top - 30)) 
            
            surface.blit(current_score_label, current_score_label_rect.topleft)
            surface.blit(current_score_value, current_score_value_rect.topleft)
            
            # Nút Quay lại Home (NEXT) 
            nut_next_rect = self.assets['nut_next'].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            surface.blit(self.assets['nut_next'], nut_next_rect.topleft)
            self.game_over_button_rect.topleft = nut_next_rect.topleft 
            
            # Thêm chữ vào nút
            button_text = self.font_large.render("Quay lại", True, COLOR_WHITE)
            button_text_rect = button_text.get_rect(center=nut_next_rect.center)
            surface.blit(button_text, button_text_rect.topleft)
        
        # 8. VẼ POP-UP CÀI ĐẶT (trên cùng)
        if self.game_manager.menu.show_settings:
            self.game_manager.menu.draw(surface)