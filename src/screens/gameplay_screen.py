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

SCORE_TIMER_FONT_FILE = 'Pacific.ttf'
SCORE_TIMER_FONT_PATH = os.path.join(ASSETS_FONT_DIR, SCORE_TIMER_FONT_FILE)

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager) 

        # --- KHỞI TẠO HỆ THỐNG FONT CHI TIẾT ---
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
        except pygame.error as e:
            print(f"Lỗi khởi tạo font: {e}")
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
            self.font_score_timer = self.font_large
            self.font_question = self.font_large
        
        # --- KHAI BÁO CÁC BIẾN KÍCH THƯỚC VÀ TRẠNG THÁI ---
        self.ANSWER_BUTTON_SIZE = (350, 80)
        self.STAR_SIZE = 50 
        self.STAR_BAR_SIZE = (300, 40)
        # Sửa hitbox cho khớp với ảnh (45x45)
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 65, 20, 45, 45) 
         # Trong __init__
        self.NEXT_BUTTON_SIZE = (220, 60)   # Nút Next dài hơn
        self.REPLAY_BUTTON_SIZE = (80, 80)  # Nút Replay hình tròn/vuông gọn hơn
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
                assets['img_new_best'] = pygame.transform.scale(assets['img_new_best'], (450, 120))
                assets['img_perfect'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'perfect_score.png')).convert_alpha()
                assets['img_perfect'] = pygame.transform.scale(assets['img_perfect'], (500, 150))
            except: pass

            assets['nutcaidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha() 
            assets['nutcaidat'] = pygame.transform.scale(assets['nutcaidat'], (45, 45))

            try:
                assets['khung_time'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'khung_time.png')).convert_alpha()
                assets['khung_time'] = pygame.transform.scale(assets['khung_time'], (140, 50))
            except:
                assets['khung_time'] = pygame.Surface((140, 50), pygame.SRCALPHA)
                pygame.draw.rect(assets['khung_time'], (255, 255, 255, 100), assets['khung_time'].get_rect(), border_radius=10)

            assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
            assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.NEXT_BUTTON_SIZE)
            
            star_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'sao.png')).convert_alpha() 
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
        """
        Khởi tạo lại trạng thái màn chơi.
        Nếu keep_score=True, điểm số (self.score) sẽ được giữ lại.
        """
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
        
        # Đặt lại chỉ số câu hỏi về đầu danh sách của màn chơi hiện tại
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
            
            # 1. ƯU TIÊN MENU CÀI ĐẶT: Nếu đang mở, chỉ Menu được nhận click
            if hasattr(self.game_manager, 'menu') and self.game_manager.menu.show_settings:
                self.game_manager.menu.handle_input(event)
                return 

            # 2. NẾU MENU ĐÓNG: Xử lý nút mở Cài đặt
            if self.settings_button_rect.collidepoint(mouse_pos):
                self._play_sound('click')
                self.game_manager.menu.show_settings = True
                return 

            # 3. XỬ LÝ KHI KẾT THÚC GAME
            if self.game_over:
                # Nút Next/Level
                if self.next_button_rect.collidepoint(mouse_pos):
                    self._play_sound('click')
                    self.game_manager.switch_screen("LEVEL") 
                    return
                # Nút Replay
                if self.replay_button_rect.collidepoint(mouse_pos):
                    self._play_sound('click')
                    self.on_enter()
                    return
                return 

            # 4. XỬ LÝ CHỌN ĐÁP ÁN
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
        
        time_frame_rect = self.assets['khung_time'].get_rect(right=self.settings_button_rect.left - 10, centery=self.settings_button_rect.centery)
        surface.blit(self.assets['khung_time'], time_frame_rect.topleft)
        
        timer_text_content = self.font_score_timer.render(f"{self.time_left}", True, COLOR_ACCENT) 
        surface.blit(timer_text_content, timer_text_content.get_rect(center=time_frame_rect.center))

        # --- THANH TIẾN ĐỘ ---
        progress_bar_bg = self.assets['thanh_sao_0']
        bar_pos_rect = progress_bar_bg.get_rect(center=(SCREEN_WIDTH // 2, self.settings_button_rect.centery))
        surface.blit(progress_bar_bg, bar_pos_rect.topleft)

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
        if not self.game_over and self.current_question:
            q_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
            surface.blit(self.assets['nen_cauhoi'], q_bg_rect)
            p_surf = self.font_question.render(f"Câu {self.current_question['question_number']}: {self.current_question['prefix']}", True, COLOR_BLACK) 
            c_surf = self.font_question.render(self.current_question["question"], True, COLOR_BLACK)
            surface.blit(p_surf, p_surf.get_rect(center=(q_bg_rect.centerx, q_bg_rect.centery - 25)))
            surface.blit(c_surf, c_surf.get_rect(center=(q_bg_rect.centerx, q_bg_rect.centery + 25)))

            for i, opt_text in enumerate(self.current_question["answers"]):
                pos_x = SCREEN_WIDTH // 2 + (-255 if i % 2 == 0 else 255)
                pos_y = self.answer_start_y + (i // 2) * self.answer_spacing
                rect = pygame.Rect(0, 0, 350, 80)
                rect.center = (pos_x, pos_y)
                self.button_rects.append(rect)
                ans_img = self.assets['nen_dapan'].copy()
                if self.selected_answer_index is not None:
                    color = COLOR_CORRECT if i == self.current_question["correct_index"] else (COLOR_WRONG if i == self.selected_answer_index else None)
                    if color:
                        overlay = pygame.Surface((342, 77), pygame.SRCALPHA)
                        pygame.draw.rect(overlay, (*color, 155), overlay.get_rect(), border_radius=23)
                        ans_img.blit(overlay, (4, 2))
                surface.blit(ans_img, rect.topleft)
                ans_surf = self.font_medium.render(f"{chr(65+i)}. {opt_text}", True, COLOR_BLACK)
                surface.blit(ans_surf, ans_surf.get_rect(center=rect.center))

        elif self.game_over:
            # --- MÀN HÌNH KẾT QUẢ ---
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200)); surface.blit(overlay, (0, 0))
            
            go_rect = self.assets['game_over_image'].get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            surface.blit(self.assets['game_over_image'], go_rect)
            
            res_img = None
            if self.is_perfect: res_img = self.assets['img_perfect']
            elif self.is_new_best: res_img = self.assets['img_new_best']
            
            if res_img:
                res_rect = res_img.get_rect(center=(SCREEN_WIDTH//2, go_rect.top + 20))
                offset_y = int(pygame.time.get_ticks() / 200) % 10
                surface.blit(res_img, (res_rect.x, res_rect.y - 70 + offset_y))

            score_txt = self.font_title.render(f"{self.score}", True, (255, 0, 0))
            surface.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery)))
            
            star_base_x = SCREEN_WIDTH // 2 - 90 
            for i in range(1, 4):
                single_star = self.assets['sao_result'].copy()
                if i > self.final_stars:
                    gray_filter = pygame.Surface(single_star.get_size(), pygame.SRCALPHA)
                    gray_filter.fill((40, 40, 40, 190)) 
                    single_star.blit(gray_filter, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(single_star, (star_base_x + (i-1)*90 - 40, go_rect.centery + 80))

            # --- VẼ CỤM NÚT NEXT & REPLAY GỌN GÀNG ---
            spacing = 50 
            total_width = self.NEXT_BUTTON_SIZE[0] + spacing + self.REPLAY_BUTTON_SIZE[0]
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 150

            # Vẽ Next
            self.next_button_rect.topleft = (start_x, button_y)
            img_next = pygame.transform.smoothscale(self.assets['nut_next'], self.NEXT_BUTTON_SIZE)
            surface.blit(img_next, self.next_button_rect.topleft)

            # Vẽ Replay
            self.replay_button_rect.topleft = (start_x + self.NEXT_BUTTON_SIZE[0] + spacing, button_y - 10)
            img_replay = pygame.transform.smoothscale(self.assets['nut_relay'], self.REPLAY_BUTTON_SIZE)
            surface.blit(img_replay, self.replay_button_rect.topleft)

        if hasattr(self.game_manager, 'menu') and self.game_manager.menu.show_settings:
            self.game_manager.menu.draw(surface)