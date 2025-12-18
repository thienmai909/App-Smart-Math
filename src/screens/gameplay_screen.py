import pygame
import os
import time
import random 
from src.screens.base_screen import BaseScreen
from src.config import *
from data.save_manager import save_game_data 

# =============================================================================
# DANH SÁCH CẤP ĐỘ VÀ CẤU HÌNH HỆ THỐNG
# =============================================================================
LEVELS = [
    {"name": "LEVEL 1", "key": "LEVEL_1", "image_key": "lv1"},
    {"name": "LEVEL 2", "key": "LEVEL_2", "image_key": "lv2"},
    {"name": "LEVEL 3", "key": "LEVEL_3", "image_key": "lv3"},
    {"name": "LEVEL 4", "key": "LEVEL_4", "image_key": "lv4"},
    {"name": "LEVEL 5", "key": "LEVEL_5", "image_key": "lv5"},
    {"name": "LEVEL 6", "key": "LEVEL_6", "image_key": "lv6"},
]

VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'Nunito-ExtraBold.ttf')
PROGRESS_BAR_WIDTH = 400
PROGRESS_BAR_HEIGHT = 40
PROGRESS_BAR_PADDING = 5
ACTION_BUTTON_SIZE = (40, 40) 

QUESTION_FONT_FILE = 'Nunito-ExtraBold.ttf' 
QUESTION_FONT_PATH = os.path.join(ASSETS_FONT_DIR, QUESTION_FONT_FILE)

SCORE_TIMER_FONT_FILE = 'Pacifico-Regular.ttf'
SCORE_TIMER_FONT_PATH = os.path.join(ASSETS_FONT_DIR, SCORE_TIMER_FONT_FILE)

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        # --- KHỞI TẠO HỆ THỐNG FONT ---
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
                    self.font_score_timer = pygame.font.Font(SCORE_TIMER_FONT_PATH, FONT_SIZE_LARGE - 10) 
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
        except pygame.error as e:
            print(f"Lỗi khởi tạo font: {e}")
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
            self.font_score_timer = self.font_large
            self.font_question = self.font_large
        
        self.ANSWER_BUTTON_SIZE = (350, 80)
        self.STAR_SIZE = 50 
        self.STAR_BAR_SIZE = (300, 40)
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 65, 20, 45, 45)
        self.NEXT_BUTTON_SIZE = (220, 60)
        self.REPLAY_BUTTON_SIZE = (80, 80)
        self.next_button_rect = pygame.Rect(0, 0, *self.NEXT_BUTTON_SIZE)
        self.replay_button_rect = pygame.Rect(0, 0, *self.REPLAY_BUTTON_SIZE)
        
        self.score = 0
        self.best_score = 0 
        self.current_question = None 
        self.button_rects = [] 
        
        self.time_limit = TIME_LIMIT
        self.start_time = time.time()
        self.time_left = self.time_limit
        self.game_over = False
        self.final_stars = 0 
        self.is_new_best = False
        self.is_perfect = False

        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30) 
        self.answer_start_y = SCREEN_HEIGHT // 2 + 50 
        self.answer_spacing = 140
        self.PROGRESS_FILL_PADDING = 3 

        self.assets = self._load_assets()

    def parse_math_expression(self, expression):
        """
        Phân tích biểu thức toán học thành các thành phần:
        - Phân số (dạng a/b)
        - Toán tử (+, -, ×, :)
        - Số nguyên
        
        Ví dụ: "6/8 + 3/7" -> [("fraction", "6/8"), ("operator", "+"), ("fraction", "3/7")]
        """
        components = []
        i = 0
        expression = expression.strip()
        
        while i < len(expression):
            # Bỏ qua khoảng trắng
            if expression[i].isspace():
                i += 1
                continue
            
            # Kiểm tra toán tử
            if expression[i] in ['+', '-', '×', ':', '−', '÷']:
                components.append(("operator", expression[i]))
                i += 1
                continue
            
            # Tìm số hoặc phân số
            start = i
            # Đọc đến khi gặp toán tử hoặc hết chuỗi
            while i < len(expression) and expression[i] not in ['+', '-', '×', ':', '−', '÷']:
                i += 1
            
            token = expression[start:i].strip()
            
            if '/' in token:
                components.append(("fraction", token))
            elif token:
                components.append(("number", token))
        
        return components

    def draw_fraction(self, surface, text, center_pos, font, color):
        """Hàm hỗ trợ vẽ phân số đơn lẻ"""
        if "/" in text:
            parts = text.split("/")
            if len(parts) >= 2:
                num_surf = font.render(parts[0].strip(), True, color)
                den_surf = font.render(parts[1].strip(), True, color)
                
                max_w = max(num_surf.get_width(), den_surf.get_width())
                line_y = center_pos[1]
                line_width = max_w + 10
                
                # Vẽ tử số, gạch ngang và mẫu số
                surface.blit(num_surf, num_surf.get_rect(center=(center_pos[0], line_y - num_surf.get_height() // 2 - 5)))
                pygame.draw.line(surface, color, (center_pos[0] - line_width // 2, line_y), (center_pos[0] + line_width // 2, line_y), 2)
                surface.blit(den_surf, den_surf.get_rect(center=(center_pos[0], line_y + den_surf.get_height() // 2 + 5)))
                return line_width
        
        # Nếu không có dấu / vẽ văn bản bình thường
        surf = font.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=center_pos))
        return surf.get_width()
    
    def draw_math_expression(self, surface, expression, center_pos, font, color):
        """
        Vẽ biểu thức toán học phức tạp (có nhiều phân số và toán tử)
        Trả về chiều rộng tổng của biểu thức
        """
        components = self.parse_math_expression(expression)
        
        # Tính toán kích thước từng thành phần và tổng chiều rộng
        component_sizes = []
        total_width = 0
        max_height = 0
        
        for comp_type, comp_value in components:
            if comp_type == "fraction":
                # Tính kích thước phân số
                parts = comp_value.split("/")
                if len(parts) >= 2:
                    num_size = font.size(parts[0].strip())
                    den_size = font.size(parts[1].strip())
                    width = max(num_size[0], den_size[0]) + 20
                    height = num_size[1] + den_size[1] + 20
                else:
                    width, height = font.size(comp_value)
            elif comp_type == "operator":
                width, height = font.size(f" {comp_value} ")
            else:  # number
                width, height = font.size(comp_value)
            
            component_sizes.append((comp_type, comp_value, width, height))
            total_width += width
            max_height = max(max_height, height)
        
        # Vẽ từng thành phần
        current_x = center_pos[0] - total_width // 2
        
        for comp_type, comp_value, width, height in component_sizes:
            if comp_type == "fraction":
                # Vẽ phân số
                self.draw_fraction(surface, comp_value, (current_x + width // 2, center_pos[1]), font, color)
            elif comp_type == "operator":
                # Vẽ toán tử
                op_surf = font.render(f" {comp_value} ", True, color)
                surface.blit(op_surf, op_surf.get_rect(center=(current_x + width // 2, center_pos[1])))
            else:  # number
                # Vẽ số
                num_surf = font.render(comp_value, True, color)
                surface.blit(num_surf, num_surf.get_rect(center=(current_x + width // 2, center_pos[1])))
            
            current_x += width
        
        return total_width

    def get_level_best_score(self, level_key):
        scores_data = self.game_manager.game_data.get('scores', {})
        if level_key in scores_data and "high_score" in scores_data[level_key]:
            return scores_data[level_key]["high_score"]
        return 0

    def calculate_stars(self, score):
        max_score = len(self.game_manager.questions_pool) * POINTS_CORRECT
        if max_score <= 0: return 0
        ratio = score / max_score
        if ratio >= 0.95: return 3
        if ratio >= 0.75: return 2
        if ratio >= 0.50: return 1
        return 0

    def save_score(self, new_score):
        if not self.game_manager.current_level_key: return
        max_possible_score = len(self.game_manager.questions_pool) * POINTS_CORRECT
        scores_data = self.game_manager.game_data.get('scores', {})
        level_key = self.game_manager.current_level_key
        level_data = scores_data.get(level_key, {'high_score': 0})
        
        if new_score >= max_possible_score and max_possible_score > 0:
            self.is_perfect = True
            self.is_new_best = False
        elif new_score > level_data['high_score']:
            self.is_new_best = True
            self.is_perfect = False
            
        if new_score > level_data['high_score']:
            level_data['high_score'] = new_score
            scores_data[level_key] = level_data
            self.game_manager.game_data['scores'] = scores_data

        new_stars = self.calculate_stars(new_score)
        current_stars = self.game_manager.game_data.get('stars', [0] * len(LEVELS))
        try:
            idx = next(i for i, lv in enumerate(LEVELS) if lv['key'] == level_key)
            if new_stars > current_stars[idx]:
                current_stars[idx] = new_stars
                self.game_manager.game_data['stars'] = current_stars
        except: pass
        save_game_data(self.game_manager.game_data)

    def _load_assets(self):
        assets = {}
        try:
            try:
                assets['nen_chinh'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nenchinh.png')).convert()
                assets['nen_chinh'] = pygame.transform.scale(assets['nen_chinh'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)

            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nencauhoi.png')).convert_alpha()
            assets['nen_cauhoi'] = pygame.transform.scale(assets['nen_cauhoi'], (950, 200))

            assets['nen_dapan'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nendapan.png')).convert_alpha()
            assets['nen_dapan'] = pygame.transform.scale(assets['nen_dapan'], self.ANSWER_BUTTON_SIZE)
            
            try:
                assets['game_over_image'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
                assets['game_over_image'] = pygame.transform.scale(assets['game_over_image'], (1200, 600)) 
            except:
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)

            try:
                assets['img_new_best'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'new_best_score.png')).convert_alpha()
                assets['img_new_best'] = pygame.transform.scale(assets['img_new_best'], (1200, 600))
                assets['img_perfect'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'perfect_score.png')).convert_alpha()
                assets['img_perfect'] = pygame.transform.scale(assets['img_perfect'], (1200, 600))
            except: pass

            assets['nutcaidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha() 
            assets['nutcaidat'] = pygame.transform.scale(assets['nutcaidat'], (45, 45))

            try:
                assets['khung_time'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'khung_time.png')).convert_alpha()
                assets['khung_time'] = pygame.transform.scale(assets['khung_time'], (80, 60))
            except:
                assets['khung_time'] = pygame.Surface((140, 50), pygame.SRCALPHA)
                pygame.draw.rect(assets['khung_time'], (255, 255, 255, 100), assets['khung_time'].get_rect(), border_radius=10)

            assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
            assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.NEXT_BUTTON_SIZE)
            
            star_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao_ketthuc.png')).convert_alpha() 
            assets['sao_large'] = pygame.transform.scale(star_img, (self.STAR_SIZE, self.STAR_SIZE))
            assets['sao_result'] = pygame.transform.scale(star_img, (80, 80))

            assets['nut_relay'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_relay.png')).convert_alpha()
            assets['nut_relay'] = pygame.transform.scale(assets['nut_relay'], self.REPLAY_BUTTON_SIZE)

            star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            assets['thanh_sao_0'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)

        except Exception as e:
            print(f"Lỗi tải Assets: {e}")

        return assets
    
    def reset_game(self, keep_score=False):
        if not keep_score:
            self.score = 0
            
        self.current_question = None
        self.game_over = False
        self.time_left = self.time_limit
        self.selected_answer_index = None
        self.final_stars = 0
        self.start_time = time.time()
        self.is_new_best = False
        self.is_perfect = False
        
        self.game_manager.question_index = 0 
        
        if hasattr(self.game_manager, 'menu'):
            self.game_manager.menu.show_settings = False

    def on_enter(self):
        if self.game_manager.current_level_key:
            self.best_score = self.get_level_best_score(self.game_manager.current_level_key)
        else:
            self.best_score = 0
        self.reset_game()
        self.load_next_question()

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
                "question_number": self.game_manager.question_index + 1,
                "correct_index": answers.index(correct_answer)
            }
            self.selected_answer_index = None
            self.show_feedback_until = 0
            self.answer_is_correct = False
            self.start_time = time.time()
            self.time_left = self.time_limit
            self.game_manager.question_index += 1
        else:
            self.game_over = True
            self.best_score = self.score
            self.final_stars = self.calculate_stars(self.score)
            self.save_score(self.score)

    def process_answer(self, selected_index):
        if selected_index >= 0 and self.game_manager.sounds:
            if 'click' in self.game_manager.sounds and self.game_manager.menu.sound_setting:
                self.game_manager.sounds['click'].play()
                
        self.selected_answer_index = selected_index
        if selected_index >= 0:
            is_correct = (selected_index == self.current_question["correct_index"])
            if is_correct:
                self.score += POINTS_CORRECT 
                self._play_sound('yes')
            else:
                self.score = max(0, self.score + POINTS_WRONG)
                self._play_sound('no')
        else: 
            self.score = max(0, self.score + POINTS_WRONG)
            self._play_sound('no')
        self.show_feedback_until = time.time() + 1.5

    def _play_sound(self, key):
        if self.game_manager.sounds and key in self.game_manager.sounds:
            if self.game_manager.menu.sound_setting:
                self.game_manager.sounds[key].play()

    def update(self):
        if hasattr(self.game_manager, 'menu') and self.game_manager.menu.show_settings:
            self.game_manager.menu.update()
            return
        if self.game_over: return
        current_time = time.time()
        if self.selected_answer_index is None:
            time_spent = current_time - self.start_time
            self.time_left = max(0, int(self.time_limit - time_spent))
            if self.time_left <= 0: self.process_answer(-2)
        if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
            self.load_next_question()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if hasattr(self.game_manager, 'menu') and self.game_manager.menu.show_settings:
                self.game_manager.menu.handle_input(event)
                return 

            if self.settings_button_rect.collidepoint(mouse_pos):
                self._play_sound('click')
                self.game_manager.menu.show_settings = True
                return 

            if self.game_over:
                if self.next_button_rect.collidepoint(mouse_pos):
                    self._play_sound('click')
                    self.game_manager.switch_screen("LEVEL") 
                    return
                if self.replay_button_rect.collidepoint(mouse_pos):
                    self._play_sound('click')
                    self.on_enter()
                    return
                return 

            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        self.process_answer(i)
                        return
                  
    def draw(self, surface):
        self.button_rects = []
        surface.blit(self.assets['nen_chinh'], (0, 0))
        
        # --- TOP BAR ---
        surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft)
        time_frame_rect = self.assets['khung_time'].get_rect(right=self.settings_button_rect.left, centery=self.settings_button_rect.centery)
        surface.blit(self.assets['khung_time'], time_frame_rect.topleft)
        timer_text_content = self.font_score_timer.render(f"{self.time_left}", True, COLOR_ACCENT) 
        surface.blit(timer_text_content, timer_text_content.get_rect(center=(time_frame_rect.x + 40, time_frame_rect.y + 25)))
        # surface.blit(timer_text_content, timer_text_content.get_rect(center=time_frame_rect.center))

        # --- THANH TIẾN ĐỘ ---
        progress_bar_bg = self.assets['thanh_sao_0']
        bar_pos_rect = progress_bar_bg.get_rect(center=(SCREEN_WIDTH // 2, self.settings_button_rect.centery))
        surface.blit(progress_bar_bg, bar_pos_rect.topleft)
        
        # Logic tính toán thanh tiến độ giữ nguyên
        max_level_score = len(self.game_manager.questions_pool) * POINTS_CORRECT
        score_ratio = min(1.0, self.score / max_level_score) if max_level_score > 0 else 0
        INNER_PADDING_X, INNER_PADDING_Y = 15, 10
        fill_max_w = bar_pos_rect.width - (2 * INNER_PADDING_X)
        current_fill_w = int(fill_max_w * score_ratio)

        if current_fill_w > 0:
            fill_color = (255, 215, 0)
            fill_height = bar_pos_rect.height - (2 * INNER_PADDING_Y)
            radius = fill_height // 2
            start_x, start_y = bar_pos_rect.x + INNER_PADDING_X, bar_pos_rect.y + INNER_PADDING_Y
            pygame.draw.circle(surface, fill_color, (start_x + radius, start_y + radius), radius)
            if current_fill_w > radius:
                pygame.draw.rect(surface, fill_color, pygame.Rect(start_x, start_y, current_fill_w, fill_height), border_radius=radius)

        star_icon_small = pygame.transform.scale(self.assets['sao_large'], (30, 30))
        star_milestones = [0.50, 0.75, 0.95]
        for milestone in star_milestones:
            star_x = bar_pos_rect.x + INNER_PADDING_X + int(fill_max_w * milestone)
            star_rect = star_icon_small.get_rect(center=(star_x, bar_pos_rect.centery))
            if score_ratio >= milestone:
                surface.blit(star_icon_small, star_rect)
            else:
                dark_star = star_icon_small.copy()
                dark_star.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
                surface.blit(dark_star, star_rect)

        best_score_value = self.font_score_timer.render(f"{self.best_score}", True, COLOR_ACCENT)
        surface.blit(best_score_value, (100, bar_pos_rect.y))

        # --- CÂU HỎI VÀ ĐÁP ÁN ---
        # --- CÂU HỎI (TỰ ĐỘNG GIÃN CHIỀU RỘNG & CHIỀU CAO) ---
        if not self.game_over and self.current_question:
            q_text = self.current_question["question"]
            
            # LEVEL 4 và LEVEL 6 (tìm X) đã có dấu "=" trong câu hỏi, không cần thêm "= ?"
            # Các level khác cần thêm "= ?" sau biểu thức
            current_level = self.game_manager.current_level_key
            is_find_x_level = current_level in ["LEVEL_4", "LEVEL_6"]
            
            if is_find_x_level:
                # Hiển thị toàn bộ câu hỏi cho Level tìm X
                math_part = q_text
                eq_text = ""
            else:
                # Cắt phần sau "=" và thêm "= ?" cho các level khác
                math_part = q_text.split("=")[0].strip() if "=" in q_text else q_text
                eq_text = "= ?" if "=" in q_text else ""
            
            eq_surf = self.font_question.render(eq_text, True, COLOR_BLACK)
            
            # 1. Tính toán kích thước nội dung câu hỏi bằng parser mới
            components = self.parse_math_expression(math_part)
            
            f_w = 0
            f_h = 0
            
            # Tính tổng chiều rộng và chiều cao từ các thành phần
            for comp_type, comp_value in components:
                if comp_type == "fraction":
                    parts = comp_value.split("/")
                    if len(parts) >= 2:
                        num_size = self.font_question.size(parts[0].strip())
                        den_size = self.font_question.size(parts[1].strip())
                        comp_w = max(num_size[0], den_size[0]) + 20
                        comp_h = num_size[1] + den_size[1] + 20
                    else:
                        comp_w, comp_h = self.font_question.size(comp_value)
                elif comp_type == "operator":
                    comp_w, comp_h = self.font_question.size(f" {comp_value} ")
                else:  # number
                    comp_w, comp_h = self.font_question.size(comp_value)
                
                f_w += comp_w
                f_h = max(f_h, comp_h)
            
            # Nếu không có thành phần nào, dùng logic cũ
            if f_w == 0:
                f_w = self.font_question.size(math_part)[0]
                f_h = self.font_question.size(math_part)[1]

            total_content_w = f_w + (25 if eq_text else 0) + eq_surf.get_width()
            
            # 2. Điều chỉnh khung câu hỏi linh hoạt
            dynamic_q_width = max(950, total_content_w + 120)
            # Chiều cao tối thiểu 200, nếu phân số cao quá thì tăng thêm
            dynamic_q_height = max(200, f_h + 100) 
            
            q_bg_img = pygame.transform.smoothscale(self.assets['nen_cauhoi'], (int(dynamic_q_width), int(dynamic_q_height)))
            q_bg_rect = q_bg_img.get_rect(center=self.question_pos)
            surface.blit(q_bg_img, q_bg_rect)
            
            # Vẽ tiêu đề "Câu X: ..."
            p_surf = self.font_question.render(f"Câu {self.current_question['question_number']}: {self.current_question['prefix']}", True, COLOR_BLACK)
            surface.blit(p_surf, p_surf.get_rect(center=(q_bg_rect.centerx, q_bg_rect.top + 65)))

            # Vẽ biểu thức toán học phức tạp ở giữa vùng trống còn lại của khung
            draw_y = q_bg_rect.top + (dynamic_q_height + 45) // 2 + 20
            
            # Sử dụng hàm vẽ biểu thức mới
            expr_center_x = q_bg_rect.centerx - (eq_surf.get_width() + 25) // 2
            self.draw_math_expression(surface, math_part, (expr_center_x, draw_y), self.font_question, COLOR_BLACK)
            
            # Vẽ "= ?" 
            if eq_text:
                eq_x = expr_center_x + f_w // 2 + 20
                surface.blit(eq_surf, eq_surf.get_rect(left=eq_x, centery=draw_y))

            # --- ĐÁP ÁN (TỰ ĐỘNG GIÃN CHIỀU RỘNG & CHIỀU CAO) ---
            for i, opt_text in enumerate(self.current_question["answers"]):
                # 1. Tính toán kích thước nội dung đáp án
                opt_w = 0
                opt_h = 0
                if "/" in opt_text:
                    opt_parts = opt_text.split("/")
                    if len(opt_parts) >= 2:
                        num_size_ans = self.font_medium.size(opt_parts[0].strip())
                        den_size_ans = self.font_medium.size(opt_parts[1].strip())
                        opt_w = max(num_size_ans[0], den_size_ans[0])
                        opt_h = num_size_ans[1] + den_size_ans[1]
                
                if opt_w == 0: 
                    opt_w = self.font_medium.size(opt_text)[0]
                    opt_h = self.font_medium.size(opt_text)[1]

                # 2. Điều chỉnh kích thước nút đáp án (Min 350x80)
                dynamic_ans_width = max(350, opt_w + 100)
                dynamic_ans_height = max(80, opt_h + 20)
                
                pos_x = SCREEN_WIDTH // 2 + (-255 if i % 2 == 0 else 255)
                # Tăng khoảng cách Y nếu các nút quá cao để tránh đè nhau
                y_offset = (i // 2) * max(self.answer_spacing, dynamic_ans_height + 20)
                pos_y = self.answer_start_y + y_offset + 30
                
                rect = pygame.Rect(0, 0, int(dynamic_ans_width), int(dynamic_ans_height))
                rect.center = (pos_x, pos_y)
                self.button_rects.append(rect)
                
                # 3. Vẽ khung đáp án co giãn
                ans_img = pygame.transform.smoothscale(self.assets['nen_dapan'], (rect.width, rect.height))
                
                if self.selected_answer_index is not None:
                    color = COLOR_CORRECT if i == self.current_question["correct_index"] else (COLOR_WRONG if i == self.selected_answer_index else None)
                    if color:
                        overlay = pygame.Surface((rect.width - 8, rect.height - 6), pygame.SRCALPHA)
                        pygame.draw.rect(overlay, (*color, 155), overlay.get_rect(), border_radius=23)
                        ans_img.blit(overlay, (4, 3))
                
                surface.blit(ans_img, rect.topleft)
                
                # 4. Vẽ nhãn A, B... và phân số
                label_surf = self.font_medium.render(f"{chr(65+i)}.", True, COLOR_BLACK)
                surface.blit(label_surf, (rect.left + 25, rect.centery - label_surf.get_height() // 2))
                self.draw_fraction(surface, opt_text, (rect.centerx + 15, rect.centery), self.font_medium, COLOR_BLACK)


        elif self.game_over:
            # Màn hình kết quả giữ nguyên
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200)); surface.blit(overlay, (0, 0))
            go_rect = self.assets['game_over_image'].get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            surface.blit(self.assets['game_over_image'], go_rect)
            
            res_img = None
            if self.is_perfect: res_img = self.assets['img_perfect']
            elif self.is_new_best: res_img = self.assets['img_new_best']

            if res_img:
                target_center_y = go_rect.centery
                res_rect = res_img.get_rect(center=(SCREEN_WIDTH//2, target_center_y))
                surface.blit(res_img, (res_rect.x, res_rect.y))

            score_txt = self.font_title.render(f"{self.score}", True, (255, 0, 0))
            surface.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery)))
            
            best_score_txt = self.font_title.render(f"{self.best_score}", True, (55, 55, 55))
            surface.blit(best_score_txt, best_score_txt.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery + 130)))

            if not self.is_perfect or not self.is_new_best:
                star_base_x = SCREEN_WIDTH // 2 - 90 
                for i in range(1, 4):
                    single_star = self.assets['sao_result'].copy()
                    if i > self.final_stars:
                        gray_filter = pygame.Surface(single_star.get_size(), pygame.SRCALPHA)
                        gray_filter.fill((40, 40, 40, 190)) 
                        single_star.blit(gray_filter, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    surface.blit(single_star, (star_base_x + (i-1)*90 - 40, go_rect.centery - 170))

            spacing = 50 
            total_width = self.NEXT_BUTTON_SIZE[0] + spacing + self.REPLAY_BUTTON_SIZE[0]
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 100

            self.next_button_rect.topleft = (start_x, button_y)
            surface.blit(self.assets['nut_next'], self.next_button_rect.topleft)

            self.replay_button_rect.topleft = (start_x + self.NEXT_BUTTON_SIZE[0] + spacing, button_y - 10)
            surface.blit(self.assets['nut_relay'], self.replay_button_rect.topleft)

            # Vẽ lại nút cài đặt
            surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft)


        if hasattr(self.game_manager, 'menu') and self.game_manager.menu.show_settings:
            self.game_manager.menu.draw(surface)