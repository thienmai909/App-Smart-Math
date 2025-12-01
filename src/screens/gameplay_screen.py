import pygame
import os
import time
import random 

# --- KHU VỰC CÁC HẰNG SỐ CƠ BẢN (GIẢ ĐỊNH TỪ src/config.py) ---
# Dùng các giá trị mặc định cho mục đích hiển thị
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
COLOR_BG = (255, 240, 245)
COLOR_TEXT = (50, 50, 50)
COLOR_WHITE = (255, 255, 255)
COLOR_ACCENT = (255, 182, 193) # Màu hồng nhạt (Màu nút đáp án mặc định)
COLOR_CORRECT = (144, 238, 144) 
COLOR_WRONG = (255, 99, 71) 
FONT_SIZE_TITLE = 60
FONT_SIZE_LARGE = 40
FONT_SIZE_MEDIUM = 28
FONT_SIZE_SMALL = 20
TIME_LIMIT = 30 
POINTS_CORRECT = 10
POINTS_WRONG = -5

# Định nghĩa các thư mục tài nguyên (Giả định cấu trúc thư mục)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, '..', '..') 
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets')
ASSETS_FONT_DIR = os.path.join(ASSETS_DIR, 'fonts')
ASSETS_IMG_DIR = os.path.join(ASSETS_DIR, 'images')
VIETNAMESE_FONT_PATH = os.path.join(ASSETS_FONT_DIR, 'UTM-Avo.ttf')
# -------------------------------------------------------------------

# --- ĐỊNH NGHĨA CÁC LỚP GIẢ LẬP ĐỂ KHẮC PHỤC LỖI "IS NOT DEFINED" ---
class BaseScreen:
    def __init__(self, game_manager):
        self.game_manager = game_manager

class DummyGameManager:
    """Lớp giả lập môi trường GameManager để chạy file này độc lập."""
    def __init__(self, surface):
        self._current_surface = surface
        self.sound_assets = {}
        # Các thuộc tính cần thiết để GameplayScreen chạy
        self.question_index = 0
        self.questions_pool = self._initialize_dummy_questions() 

    def _initialize_dummy_questions(self):
        return [
            {"question": "Đơn vị cơ bản của mọi vật chất là gì?", "options": ["Phân tử", "Nguyên tử", "Tế bào", "Electron"], "answer": "Nguyên tử"},
            {"question": "Loài vật nào là biểu tượng của nước Úc?", "options": ["Hổ", "Gấu trúc", "Kangaroo", "Voi"], "answer": "Kangaroo"}
        ]
    def switch_screen(self, screen_name): print(f"Chuyển màn hình sang: {screen_name}")
    def calculate_stars(self, score):
        if score >= 20: return 3
        if score >= 10: return 2
        return 1
    def save_score(self, score): print(f"Lưu điểm: {score}")

# --- LỚP GameplayScreen THỰC TẾ ---

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # --- KHỞI TẠO FONT ---
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
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
        
        # Kích thước cố định
        self.ANSWER_BUTTON_SIZE = (450, 60)
        self.STAR_SIZE = 50 

        self.back_button_rect = pygame.Rect(20, 20, 100, 40) 
        self.game_over_button_rect = pygame.Rect(0, 0, 250, 60)
        
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

        self.question_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 - 20)
        self.answer_start_y = SCREEN_HEIGHT // 2 + 50
        self.answer_spacing = 100 
        
        self.assets = self._load_assets() 
        
        self.game_over_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
        
        self.load_next_question()

    def _load_assets(self):
        assets = {}
        try:
            # 1. NỀN MÀN HÌNH CHÍNH (Surface màu)
            assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)

            # 2. NỀN CÂU HỎI (nen_cauhoi)
            assets['nen_cauhoi'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nen_cauhoi.png')).convert_alpha()
            assets['nen_cauhoi'] = pygame.transform.scale(assets['nen_cauhoi'], (650, 150))
            
            # 3. GAME OVER IMAGE (game_over.png)
            try:
                assets['game_over_image'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'game_over.png')).convert_alpha()
                assets['game_over_image'] = pygame.transform.scale(assets['game_over_image'], (600, 400)) 
            except pygame.error:
                # Fallback Surface Game Over
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)
                text_go = self.font_title.render("GAME OVER", True, (255, 223, 0))
                text_score = self.font_large.render("Score", True, COLOR_TEXT)
                assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
                assets['game_over_image'].blit(text_score, text_score.get_rect(center=(200, 100)))

            # 4. NÚT BACK (nut_back)
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
            assets['nut_back'] = pygame.transform.scale(assets['nut_back'], (150, 60))
            self.back_button_rect.size = assets['nut_back'].get_size() 
            self.back_button_rect.topleft = (20, 20)

            # 5. THANH TIẾN ĐỘ (thanh_tiendo)
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            assets['thanh_tiendo'] = pygame.transform.scale(assets['thanh_tiendo'], (300, 40))

            # 6. SAO (Surface vẽ Pygame)
            star_surf = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE), pygame.SRCALPHA)
            star_surf.fill((0, 0, 0, 0))
            pygame.draw.polygon(star_surf, (255, 223, 0), [(25, 0), (33, 17), (50, 19), (38, 30), (41, 50), (25, 38), (9, 50), (12, 30), (0, 19), (17, 17)], 0)
            assets['sao_large'] = star_surf
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh: {e}. Sử dụng Surface màu mặc định cho các thành phần bị thiếu.")
            
            # Tạo Fallback Surface nếu lỗi
            assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)
            assets['nen_cauhoi'] = pygame.Surface((650, 150), pygame.SRCALPHA); assets['nen_cauhoi'].fill((255, 255, 255, 150))
            assets['nut_back'] = pygame.Surface((150, 60)); assets['nut_back'].fill(COLOR_WRONG)
            assets['thanh_tiendo'] = pygame.Surface((300, 40)); assets['thanh_tiendo'].fill((200, 200, 200))
            assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA); 
            text_go = self.font_title.render("GAME OVER", True, (255, 223, 0))
            assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
            assets['sao_large'] = None
            
        return assets

    def reset_game(self):
        self.score = 0
        self.current_question = None
        self.game_over = False
        self.time_left = self.time_limit
        self.selected_answer_index = None
        self.final_stars = 0

    def load_next_question(self):
        
        if self.game_manager.question_index < len(self.game_manager.questions_pool):
            q_data = self.game_manager.questions_pool[self.game_manager.question_index]
            
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
                # Xử lý nút "NEXT" / "VỀ MENU"
                if self.game_over_button_rect.collidepoint(mouse_pos):
                    self.game_manager.switch_screen("MENU")
            return 
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # XỬ LÝ NÚT BACK (QUAY VỀ MENU) - BẮT BUỘC CLICK ĐƯỢC
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game_manager.switch_screen("MENU")
                return

            if self.selected_answer_index is None:
                for i, rect in enumerate(self.button_rects):
                    if rect.collidepoint(mouse_pos):
                        # if self.game_manager.sound_assets.get('click_dapan'): self.game_manager.sound_assets['click_dapan'].play()
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
            self.time_left = self.time_limit - int(current_time - self.start_time)
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
        
        # 0. VẼ NỀN CHÍNH (QUAN TRỌNG: để xóa frame trước đó)
        surface.blit(self.assets['nen_chinh'], (0, 0))
        
        # 1. VẼ ĐIỂM SỐ VÀ TIMER
        if 'thanh_tiendo' in self.assets:
            tiendo_rect = self.assets['thanh_tiendo'].get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(self.assets['thanh_tiendo'], tiendo_rect)
            
            timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
            timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
            timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(timer_text, timer_text_rect)

        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 20 - score_text.get_width(), 20))
        
        # 2. VẼ NÚT BACK/MENU
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        if self.current_question:
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

            # 4. VẼ 4 ĐÁP ÁN (Dùng pygame.draw.rect cho khung màu hồng)
            for i, answer in enumerate(self.current_question["answers"]):
                # Sắp xếp 2x2:
                if i % 2 == 0: 
                    x_pos = SCREEN_WIDTH // 2 - 250
                    y_pos = self.answer_start_y + (i // 2) * self.answer_spacing
                else: 
                    x_pos = SCREEN_WIDTH // 2 + 250
                    y_pos = self.answer_start_y + (i // 2) * self.answer_spacing

                button_width, button_height = self.ANSWER_BUTTON_SIZE 
                button_rect = pygame.Rect(0, 0, button_width, button_height)
                button_rect.center = (x_pos, y_pos)
                self.button_rects.append(button_rect) 
                
                button_color = COLOR_ACCENT 
                
                # Logic tô màu phản hồi
                if self.selected_answer_index is not None:
                    if i == self.current_question["correct_index"]:
                        button_color = COLOR_CORRECT
                    elif i == self.selected_answer_index and not self.answer_is_correct:
                        button_color = COLOR_WRONG
                
                # VẼ HÌNH CHỮ NHẬT ĐÁP ÁN (Khung màu hồng)
                pygame.draw.rect(surface, button_color, button_rect, border_radius=10)
                
                # VẼ VĂN BẢN ĐÁP ÁN (SỬ DỤNG COLOR_TEXT và căn giữa)
                answer_display = f"{chr(65 + i)}. {answer}"
                answer_text = self.font_medium.render(answer_display, True, COLOR_TEXT) 
                answer_text_rect = answer_text.get_rect(center=button_rect.center) 
                surface.blit(answer_text, answer_text_rect)
            
        # 5. VẼ THÔNG BÁO GAME OVER
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            surface.blit(overlay, (0, 0))
            
            # VẼ HÌNH ẢNH GAME OVER (Game Over Image)
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
                    
            # Nút Quay lại Menu (NEXT trong hình ảnh)
            pygame.draw.rect(surface, COLOR_CORRECT, self.game_over_button_rect, border_radius=10)
            menu_text = self.font_small.render("NEXT", True, COLOR_WHITE) 
            menu_text_rect = menu_text.get_rect(center=self.game_over_button_rect.center)
            surface.blit(menu_text, menu_text_rect)

# --- KHU VỰC CHẠY THỬ NGHIỆM ĐỘC LẬP (TÙY CHỌN) ---
if __name__ == '__main__':
    pygame.init()
    
    # Thiết lập môi trường test cần thiết
    SCREEN_WIDTH = 1024 
    SCREEN_HEIGHT = 768
    COLOR_BG = (255, 240, 245)
    COLOR_TEXT = (50, 50, 50)
    COLOR_WHITE = (255, 255, 255)
    COLOR_ACCENT = (255, 182, 193)
    COLOR_CORRECT = (144, 238, 144) 
    COLOR_WRONG = (255, 99, 71) 
    TIME_LIMIT = 30 
    POINTS_CORRECT = 10
    POINTS_WRONG = -5
    FONT_SIZE_TITLE = 60
    FONT_SIZE_LARGE = 40
    FONT_SIZE_SMALL = 20
    FONT_SIZE_MEDIUM = 28
    
    if not os.path.exists(ASSETS_IMG_DIR): os.makedirs(ASSETS_IMG_DIR)
        
    def create_dummy_image(name, size, color):
        path = os.path.join(ASSETS_IMG_DIR, name)
        if not os.path.exists(path):
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill(color)
            pygame.image.save(surf, path)

    create_dummy_image('nen_cauhoi.png', (650, 150), (255, 255, 255, 150))
    create_dummy_image('nut_back.png', (150, 60), COLOR_WRONG)
    create_dummy_image('thanh_tiendo.png', (300, 40), (200, 200, 200))
    create_dummy_image('game_over.png', (600, 400), (255, 255, 255, 150)) 

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Lớp DummyGameManager đã được định nghĩa ở trên để khắc phục lỗi
    game_manager = DummyGameManager(screen)
    game_screen = GameplayScreen(game_manager)
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_screen.handle_input(event)

        game_screen.update()
        game_screen.draw()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()