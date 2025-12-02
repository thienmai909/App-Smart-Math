import pygame
import os
import time
import random 
from src.screens.base_screen import BaseScreen
from src.config import * 
VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')

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
        self.STAR_BAR_SIZE = (300, 60)
        # Settings/Home button
        self.settings_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 100, 40) 
        
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

        # --- KHỞI TẠO SETTINGS POP-UP 
        self.show_settings = False
        # Giả định kích thước nền settings
        self.settings_rect = self.assets['nen_caidat'].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) 
        self.close_rect = pygame.Rect(self.settings_rect.right - 40, self.settings_rect.y + 10, 30, 30)
        self.sound_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 120, 300, 50)
        self.bgm_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 190, 300, 50)
        self.home_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 280, 300, 50) 
        self.replay_rect = pygame.Rect(self.settings_rect.x + 50, self.settings_rect.y + 360, 300, 50) 
        
        self.sound_on = True 
        self.bgm_on = True 
        
    def _load_assets(self):
        assets = {}
        assets['is_settings_fallback'] = False 
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
                assets['game_over_image'] = pygame.transform.scale(assets['game_over_image'], (1200, 600)) 
            except pygame.error:
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)
                text_go = self.font_title.render("GAME OVER", True, COLOR_TITLE)
                text_score = self.font_large.render("Score", True, COLOR_TEXT)
                assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
                assets['game_over_image'].blit(text_score, text_score.get_rect(center=(200, 100)))

            # 5. NÚT SETTINGS (nutcaidat.png)
            try:
                assets['nutcaidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutcaidat.png')).convert_alpha() 
                assets['nutcaidat'] = pygame.transform.scale(assets['nutcaidat'], (40, 40))
            except pygame.error:
                assets['nutcaidat'] = pygame.Surface((40, 40)); assets['nutcaidat'].fill(COLOR_INFO) 
                assets['is_settings_fallback'] = True
            
            self.settings_button_rect.size = assets['nutcaidat'].get_size()
            self.settings_button_rect.topright = (SCREEN_WIDTH - 20, 20) 

            # 6. NÚT NEXT (nut_next.png)
            try:
                assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
                assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.GAME_OVER_BUTTON_SIZE)
            except pygame.error:
                assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
                
            # 7. THANH TIẾN ĐỘ (thanh_tiendo.png)
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            assets['thanh_tiendo'] = pygame.transform.scale(assets['thanh_tiendo'], (300, 40))
            
            # 8. THANH SAO & SAO
            # Sao lớn (
            star_surf = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE), pygame.SRCALPHA)
            pygame.draw.polygon(star_surf, (255, 223, 0), [(25, 0), (33, 17), (50, 19), (38, 30), (41, 50), (25, 38), (9, 50), (12, 30), (0, 19), (17, 17)], 0)
            assets['sao_large'] = star_surf
            
            # Tải 4 thanh sao: thanh_sao_0.png, thanh_sao_1.png, thanh_sao_2.png, thanh_sao_3.png
            for i in range(4):
                    filename = f'thanh_sao_{i}.png'
                    try:
                        star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, filename)).convert_alpha()
                        assets[f'thanh_sao_{i}'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)
                    except pygame.error:
                        fallback_surf = pygame.Surface(self.STAR_BAR_SIZE, pygame.SRCALPHA)
                        fallback_surf.fill((200, 200, 200, 150))
                        assets[f'thanh_sao_{i}'] = fallback_surf
            
            # 9. ASSETS SETTINGS POP-UP
            assets['nen_caidat'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'anvao_caidat.png')).convert_alpha()
            assets['nen_caidat'] = pygame.transform.scale(assets['nen_caidat'], (400, 450)) 
            assets['on'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'on.png')).convert_alpha(), (50, 30))
            assets['off'] = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'off.png')).convert_alpha(), (50, 30))

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
                
            # 10. TẢI ÂM THANH 
            assets['sound'] = {}
            # Nhạc nền 
            assets['sound']['bgm'] = os.path.join(ASSETS_SOUND_DIR, 'nhacnen.mp3') 
            # Hiệu ứng âm thanh 
            try:
                assets['sound']['click'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, 'click_dapan.wav'))
                assets['sound']['correct'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, 'yes.mp3'))
                assets['sound']['wrong'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, 'no.mp3'))
            except pygame.error as e:
                print(f"Lỗi tải âm thanh hiệu ứng: {e}. Âm thanh sẽ không được phát.")
                assets['sound']['click'] = None
                assets['sound']['correct'] = None
                assets['sound']['wrong'] = None

        except pygame.error as e:
            print(f"Lỗi tải hình ảnh: {e}. Sử dụng Surface màu mặc định cho các thành phần bị thiếu.")
            # FALLBACK CHO ẢNH
            assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)
            assets['nen_cauhoi'] = pygame.Surface((650, 150), pygame.SRCALPHA); assets['nen_cauhoi'].fill((255, 255, 255, 150))
            assets['nen_dapan'] = pygame.Surface(self.ANSWER_BUTTON_SIZE, pygame.SRCALPHA); assets['nen_dapan'].fill(COLOR_ACCENT) 
            assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
            assets['thanh_tiendo'] = pygame.Surface((300, 40)); assets['thanh_tiendo'].fill((200, 200, 200))
            assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA); 
            text_go = self.font_title.render("GAME OVER", True, COLOR_TITLE)
            assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
            assets['sao_large'] = None
            assets['nutcaidat'] = pygame.Surface((80, 30)); assets['nutcaidat'].fill(COLOR_INFO) 
            assets['is_settings_fallback'] = True 
            for i in range(4):
                    assets[f'thanh_sao_{i}'] = pygame.Surface(self.STAR_BAR_SIZE); assets[f'thanh_sao_{i}'].fill((200, 200, 200))
            # FALLBACK CHO SETTINGS
            assets['nen_caidat'] = pygame.Surface((400, 450)); assets['nen_caidat'].fill((200, 150, 150))
            assets['on'] = pygame.Surface((50, 30)); assets['on'].fill(COLOR_CORRECT)
            assets['off'] = pygame.Surface((50, 30)); assets['off'].fill(COLOR_WRONG)
            assets['nut_back_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_back_icon'].fill(COLOR_ACCENT)
            assets['nut_play_icon'] = pygame.Surface(ACTION_BUTTON_SIZE); assets['nut_play_icon'].fill(COLOR_CORRECT)
            # FALLBACK CHO SOUND
            assets['sound'] = {'bgm': None, 'click': None, 'correct': None, 'wrong': None}

        return assets

    def on_enter(self):
        """Khởi động trò chơi khi màn hình này được kích hoạt."""
        # 1. Reset trạng thái trò chơi
        self.reset_game()
        
        # 2. Tải câu hỏi đầu tiên
        self.load_next_question()

        # 3. KHỞI ĐỘNG NHẠC NỀN
        if self.bgm_on and 'bgm' in self.assets['sound'] and self.assets['sound']['bgm']:
            try:
                pygame.mixer.music.load(self.assets['sound']['bgm'])
                pygame.mixer.music.play(-1) # Phát lặp lại
            except pygame.error as e:
                print(f"Lỗi phát nhạc nền: {e}")

    def reset_game(self):
        self.score = 0
        self.current_question = None
        self.game_over = False
        self.time_left = self.time_limit
        self.selected_answer_index = None
        self.final_stars = 0
        self.start_time = time.time()
        self.show_settings = False
        
        # DỪNG NHẠC NỀN
        pygame.mixer.music.stop()

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
        
        else:
            # Hết câu hỏi -> GAME OVER
            self.game_over = True
            self.final_stars = self.game_manager.calculate_stars(self.score)
            self.game_manager.save_score(self.score) 
            
            # DỪNG NHẠC NỀN KHI GAME OVER 
            pygame.mixer.music.stop()

    def handle_input(self, event):   
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # --- ƯU TIÊN 1: XỬ LÝ POP-UP SETTINGS NẾU ĐANG MỞ ---
            if self.show_settings:
                if self.close_rect.collidepoint(mouse_pos):
                    self.show_settings = False
                    return
                
                # Logic click bên trong pop-up
                if self.sound_rect.collidepoint(mouse_pos):
                    self.sound_on = not self.sound_on
                    
                elif self.bgm_rect.collidepoint(mouse_pos):
                    self.bgm_on = not self.bgm_on
                    # LOGIC BẬT/TẮT NHẠC NỀN 
                    if self.bgm_on:
                        if 'bgm' in self.assets['sound'] and self.assets['sound']['bgm']:
                             try:
                                pygame.mixer.music.load(self.assets['sound']['bgm'])
                                pygame.mixer.music.play(-1)
                             except pygame.error as e:
                                print(f"Lỗi phát nhạc nền: {e}")
                    else:
                        pygame.mixer.music.stop()
                        
                elif self.home_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("LEVEL") 
                    self.show_settings = False
                    self.reset_game() 
                elif self.replay_rect.collidepoint(mouse_pos):
                    # Chơi lại level hiện tại
                    # Để chơi lại level hiện tại, ta cần reset index về đầu level
                    self.game_manager.question_index = 0
                    self.reset_game()
                    self.load_next_question() 
                    self.show_settings = False
                return 
            
            # --- ƯU TIÊN 2: XỬ LÝ TRƯỜNG HỢP GAME OVER ---
            if self.game_over:
                if self.game_over_button_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("LEVEL") 
                    self.reset_game() 
                return 
            
            # --- ƯU TIÊN 3: XỬ LÝ GAMEPLAY BÌNH THƯỜNG ---
            
            # XỬ LÝ NÚT SETTINGS (MỞ POP-UP)
            if self.settings_button_rect.collidepoint(mouse_pos):
                self.show_settings = True 
                return

            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        self.process_answer(i)
                        return

    def process_answer(self, selected_index):
        # PHÁT ÂM THANH CLICK KHI CHỌN 
        if selected_index >= 0 and self.assets['sound']['click'] and self.sound_on:
             self.assets['sound']['click'].play()
             
        self.selected_answer_index = selected_index
        
        if selected_index >= 0:
            is_correct = (selected_index == self.current_question["correct_index"])
            self.answer_is_correct = is_correct
            
            if is_correct:
                self.score += POINTS_CORRECT 
                # PHÁT ÂM THANH ĐÚNG 
                if self.assets['sound']['correct'] and self.sound_on:
                     self.assets['sound']['correct'].play()
            else:
                self.score += POINTS_WRONG 
                # PHÁT ÂM THANH SAI 
                if self.assets['sound']['wrong'] and self.sound_on:
                     self.assets['sound']['wrong'].play()
        else: # Hết giờ (Xử lý như đáp án sai)
            self.answer_is_correct = False
            self.score += POINTS_WRONG 
            # PHÁT ÂM THANH SAI 
            if self.assets['sound']['wrong'] and self.sound_on:
                 self.assets['sound']['wrong'].play()

        self.show_feedback_until = time.time() + 1.5 

    def update(self):
        # Logic settings
        if self.show_settings:
            # Điều chỉnh mixer dựa trên self.sound_on 
            if self.sound_on:
                pygame.mixer.set_reserved(0) 
            else:
                pygame.mixer.set_reserved(1)
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

    """Vẽ pop-up cài đặt lên trên màn hình."""         
    def _draw_settings_popup(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) 
        surface.blit(overlay, (0, 0))   
        
        # Vẽ nền pop-up
        surface.blit(self.assets['nen_caidat'], self.settings_rect.topleft)
        
        # --- VẼ CÁC THÔNG TIN/NÚT BÊN TRONG POPUP ---
        
        # Sound FX
        sound_icon = self.assets['on'] if self.sound_on else self.assets['off']
        sound_icon_rect = sound_icon.get_rect(midright=(self.settings_rect.right - 40, self.sound_rect.centery))
        surface.blit(sound_icon, sound_icon_rect.topleft)
        sound_text = self.font_medium.render("Âm thanh FX", True, COLOR_TEXT)
        surface.blit(sound_text, (self.sound_rect.x + 10, self.sound_rect.centery - sound_text.get_height() // 2))

        # BGM
        bgm_icon = self.assets['on'] if self.bgm_on else self.assets['off']
        bgm_icon_rect = bgm_icon.get_rect(midright=(self.settings_rect.right - 40, self.bgm_rect.centery))
        surface.blit(bgm_icon, bgm_icon_rect.topleft)
        bgm_text = self.font_medium.render("Nhạc nền", True, COLOR_TEXT)
        surface.blit(bgm_text, (self.bgm_rect.x + 10, self.bgm_rect.centery - bgm_text.get_height() // 2))

        # Home (Chọn Level)
        home_text = self.font_medium.render("Trang chủ", True, COLOR_TEXT)
        surface.blit(home_text, (self.home_rect.x + 10, self.home_rect.centery - home_text.get_height() // 2))
        if 'nut_back_icon' in self.assets:
            icon_asset = self.assets['nut_back_icon']
            icon_rect = icon_asset.get_rect(midright=(self.home_rect.right - 40, self.home_rect.centery))
            surface.blit(icon_asset, icon_rect.topleft)


        # Replay (Chơi lại level hiện tại)
        replay_text = self.font_medium.render("Chơi lại", True, COLOR_TEXT)
        surface.blit(replay_text, (self.replay_rect.x + 10, self.replay_rect.centery - replay_text.get_height() // 2))
        if 'nut_play_icon' in self.assets:
            icon_asset = self.assets['nut_play_icon']
            icon_rect = icon_asset.get_rect(midright=(self.replay_rect.right - 40, self.replay_rect.centery))
            surface.blit(icon_asset, icon_rect.topleft)

        # Nút đóng pop-up (X)
        pygame.draw.circle(surface, COLOR_WRONG, self.close_rect.center, 15)
        close_text = self.font_small.render("X", True, COLOR_WHITE)
        close_text_rect = close_text.get_rect(center=self.close_rect.center)
        surface.blit(close_text, close_text_rect)
            
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
            
            TIME_PADDING = 50 # Khoảng cách từ lề trái màn hình
            timer_text_rect = timer_text.get_rect(midleft=(TIME_PADDING, 30)) 
            surface.blit(timer_text, timer_text_rect)

        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 120 - score_text.get_width(), 20)) 
          
        # 2. VẼ NÚT SETTINGS
        surface.blit(self.assets['nutcaidat'], self.settings_button_rect.topleft)
        
        if self.assets['is_settings_fallback']:
             setting_text = self.font_small.render("Cài đặt", True, COLOR_WHITE)
             setting_rect = setting_text.get_rect(center=self.settings_button_rect.center)
             surface.blit(setting_text, setting_rect)
        
         # 3. VẼ CÂU HỎI (Dùng nen_cauhoi)
        if not self.game_over and self.current_question:
            if 'nen_cauhoi' in self.assets: 
                question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
                surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
                question_rect_center = question_bg_rect.center
            else:
                question_rect_center = self.question_pos

            #=== VẼ CÂU HỎI CÓ SỐ THỨ TỰ ) ===
            
            # 1. Chuẩn bị nội dung
            question_num = self.current_question.get("question_number", self.game_manager.question_index)
            question_content = self.current_question["question"]
            
            # 2. Render phần IN ĐẬM: "Câu N: "
            bold_text = f"Câu {question_num}: "
            bold_surface = self.font_large.render(bold_text, True, COLOR_TEXT) 
            
            # 3. Render phần còn lại: Nội dung câu hỏi
            content_surface = self.font_large.render(question_content, True, COLOR_TEXT)
            
            # 4. Tính toán vị trí để căn giữa và đặt liền kề
            
            # Tính tổng chiều rộng
            total_width = bold_surface.get_width() + content_surface.get_width()
            
            # Tính vị trí bắt đầu (để đảm bảo toàn bộ chuỗi được căn giữa)
            start_x = question_rect_center[0] - total_width // 2
            start_y = question_rect_center[1]
            
            # VẼ PHẦN IN ĐẬM
            bold_rect = bold_surface.get_rect(midleft=(start_x, start_y))
            surface.blit(bold_surface, bold_rect.topleft)
            
            # VẼ PHẦN NỘI DUNG (bắt đầu ngay sau phần in đậm)
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
            go_rect = go_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 ))
            surface.blit(go_image, go_rect)
            

            # Nút Quay lại Menu (NEXT)
            if 'nut_next' in self.assets:
                surface.blit(self.assets['nut_next'], self.game_over_button_rect.topleft)
            else:
                pygame.draw.rect(surface, COLOR_CORRECT, self.game_over_button_rect, border_radius=0)

        # 6. VẼ POP-UP CÀI ĐẶT
        if self.show_settings:
            self._draw_settings_popup(surface)