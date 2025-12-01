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
            {"question": "Loài vật nào là biểu tượng của nước Úc?", "options": ["Hổ", "Gấu trúc", "Kangaroo", "Voi"], "answer": "Kangaroo"},
            {"question": "Thủ đô của Nhật Bản là gì?", "options": ["Seoul", "Bắc Kinh", "Tokyo", "Bangkok"], "answer": "Tokyo"},
            {"question": "Ai là người phát minh ra bóng đèn?", "options": ["Tesla", "Edison", "Newton", "Galileo"], "answer": "Edison"}
        ]
    
    # KHẮC PHỤC LỖI 3: Xóa phần code sử dụng STAR_THRESHOLD_X chưa được định nghĩa
    def calculate_stars(self, score):
        if score >= 20: return 3
        if score >= 10: return 2
        return 1
        
    def switch_screen(self, screen_name): print(f"Chuyển màn hình sang: {screen_name}")
    def save_score(self, score): print(f"Lưu điểm: {score}")

# --- LỚP GameplayScreen THỰC TẾ ---

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # --- KHỞI TẠO FONT (ĐÃ TỐI ƯU HỖ TRỢ UNICODE) ---
        try:
            selected_font_path = None
            
            # 1. Ưu tiên sử dụng font .ttf Việt hóa
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                selected_font_path = VIETNAMESE_FONT_PATH
            else:
                # 2. Tìm kiếm font hệ thống hỗ trợ Unicode tốt
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
                # Fallback cuối cùng
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
                self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
                
        except pygame.error as e:
            # Fallback nếu có lỗi Pygame khi tạo font
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_large = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
            self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
        
        # Kích thước cố định 
        self.ANSWER_BUTTON_SIZE = (350, 80)
        self.STAR_SIZE = 50 
        self.STAR_BAR_SIZE = (300, 60)
        self.back_button_rect = pygame.Rect(20, 20, 100, 40) 
        
        # KHẮC PHỤC LỖI 1: Khai báo self.GAME_OVER_BUTTON_SIZE trước khi gọi _load_assets
        self.GAME_OVER_BUTTON_SIZE = (250, 60) # Kích thước nút NEXT/MENU
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
        self.answer_spacing = 140 # Khoảng cách dọc giữa 2 hàng đáp án
        
        self.assets = self._load_assets() 
        
        self.game_over_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
        
        self.load_next_question()

    def _load_assets(self):
        assets = {}
        try:
            # 1. NỀN MÀN HÌNH CHÍNH (nenchinh.png)
            try:
                assets['nen_chinh'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nenchinh.png')).convert()
                assets['nen_chinh'] = pygame.transform.scale(assets['nen_chinh'], (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)

            # 2. NỀN CÂU HỎI (nen_cauhoi.png)
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
                # Fallback Surface Game Over
                assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA)
                text_go = self.font_title.render("GAME OVER", True, (255, 223, 0))
                text_score = self.font_large.render("Score", True, COLOR_TEXT)
                assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
                assets['game_over_image'].blit(text_score, text_score.get_rect(center=(200, 100)))

            # 5. NÚT BACK (nut_back)
            assets['nut_back'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_back.png')).convert_alpha()
            assets['nut_back'] = pygame.transform.scale(assets['nut_back'], (80, 30))
            self.back_button_rect.size = assets['nut_back'].get_size() 
            self.back_button_rect.topleft = (20, 20)

            # 6. NÚT NEXT (nut_next.png)
            try:
                assets['nut_next'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nut_next.png')).convert_alpha()
                # SỬ DỤNG THUỘC TÍNH self.GAME_OVER_BUTTON_SIZE ĐÃ KHẮC PHỤC
                assets['nut_next'] = pygame.transform.scale(assets['nut_next'], self.GAME_OVER_BUTTON_SIZE)
            except pygame.error:
                assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
                
            # 7. THANH TIẾN ĐỘ (thanh_tiendo)
            assets['thanh_tiendo'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'thanh_tiendo.png')).convert_alpha()
            assets['thanh_tiendo'] = pygame.transform.scale(assets['thanh_tiendo'], (300, 40))
            
            # 8. THANH SAO (MỚI) - Giả định file ảnh có tên rõ ràng
            for i in range(4):
                    filename = f'thanh_sao_{i}.png' # Ví dụ: thanh_sao_0.png, thanh_sao_1.png, ...
                    try:
                        star_bar_img = pygame.image.load(os.path.join(ASSETS_IMG_DIR, filename)).convert_alpha()
                        assets[f'thanh_sao_{i}'] = pygame.transform.scale(star_bar_img, self.STAR_BAR_SIZE)
                    except pygame.error:
                        # Fallback nếu không tìm thấy ảnh thanh sao
                        fallback_surf = pygame.Surface(self.STAR_BAR_SIZE, pygame.SRCALPHA)
                        fallback_surf.fill((200, 200, 200, 150))
                        if i > 0:
                            # Vẽ sao tượng trưng lên fallback
                            star_fill = i * (self.STAR_BAR_SIZE[0] // 3)
                            pygame.draw.rect(fallback_surf, (255, 223, 0, 200), (0, 0, star_fill, self.STAR_BAR_SIZE[1]))
                        assets[f'thanh_sao_{i}'] = fallback_surf
            # 9. SAO (Surface vẽ Pygame)
            star_surf = pygame.Surface((self.STAR_SIZE, self.STAR_SIZE), pygame.SRCALPHA)
            star_surf.fill((0, 0, 0, 0))
            pygame.draw.polygon(star_surf, (255, 223, 0), [(25, 0), (33, 17), (50, 19), (38, 30), (41, 50), (25, 38), (9, 50), (12, 30), (0, 19), (17, 17)], 0)
            assets['sao_large'] = star_surf
            assets['sao_small'] = pygame.transform.scale(star_surf.copy(), (30, 30))
            
        except pygame.error as e:
            print(f"Lỗi tải hình ảnh: {e}. Sử dụng Surface màu mặc định cho các thành phần bị thiếu.")
            
            # Tạo Fallback Surface nếu lỗi
            assets['nen_chinh'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); assets['nen_chinh'].fill(COLOR_BG)
            assets['nen_cauhoi'] = pygame.Surface((650, 150), pygame.SRCALPHA); assets['nen_cauhoi'].fill((255, 255, 255, 150))
            assets['nen_dapan'] = pygame.Surface(self.ANSWER_BUTTON_SIZE, pygame.SRCALPHA); assets['nen_dapan'].fill(COLOR_ACCENT) 
            assets['nut_back'] = pygame.Surface((150, 60)); assets['nut_back'].fill(COLOR_WRONG)
            assets['nut_next'] = pygame.Surface(self.GAME_OVER_BUTTON_SIZE); assets['nut_next'].fill(COLOR_CORRECT)
            assets['thanh_tiendo'] = pygame.Surface((300, 40)); assets['thanh_tiendo'].fill((200, 200, 200))
            assets['game_over_image'] = pygame.Surface((400, 150), pygame.SRCALPHA); 
            text_go = self.font_title.render("GAME OVER", True, (255, 223, 0))
            assets['game_over_image'].blit(text_go, text_go.get_rect(center=(200, 40)))
            assets['sao_large'] = None
            assets['sao_small'] = None
            for i in range(4):
                    assets[f'thanh_sao_{i}'] = pygame.Surface(self.STAR_BAR_SIZE) 
                    assets[f'thanh_sao_{i}'].fill((200, 200, 200))
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
        
        # Chỉ đánh giá là đúng/sai khi người chơi chọn
        if selected_index >= 0:
            is_correct = (selected_index == self.current_question["correct_index"])
            self.answer_is_correct = is_correct
            
            if is_correct:
                self.score += POINTS_CORRECT 
            else:
                self.score += POINTS_WRONG 
        else: # Hết giờ
            self.answer_is_correct = False
            self.score += POINTS_WRONG # Trừ điểm nếu hết giờ (giả định)

        self.show_feedback_until = time.time() + 1.5 

    def update(self):
        if self.game_over:
            return

        current_time = time.time()
        
        if self.selected_answer_index is None:
            self.time_left = self.time_limit - int(current_time - self.start_time)
            if self.time_left <= 0:
                self.time_left = 0
                self.process_answer(-2) # -2: mã lỗi hết giờ
        
        # Chờ phản hồi kết thúc rồi load câu hỏi mới
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
            
            timer_color = COLOR_ACCENT if self.time_left > 5 else COLOR_WRONG
            timer_text = self.font_small.render(f"Thời gian: {self.time_left}", True, timer_color)
            timer_text_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
            surface.blit(timer_text, timer_text_rect)

        score_text = self.font_small.render(f"Điểm: {self.score}", True, COLOR_TEXT)
        surface.blit(score_text, (SCREEN_WIDTH - 20 - score_text.get_width(), 20))
        
        # 2. VẼ NÚT BACK/MENU
        surface.blit(self.assets['nut_back'], self.back_button_rect.topleft)
        
        if not self.game_over and self.current_question:
            # 3. VẼ CÂU HỎI (Dùng nen_cauhoi)
            # KHẮC PHỤC LỖI 2: Dùng key 'nen_cauhoi' thay vì 'nencauhoi'
            if 'nen_cauhoi' in self.assets: 
                question_bg_rect = self.assets['nen_cauhoi'].get_rect(center=self.question_pos)
                surface.blit(self.assets['nen_cauhoi'], question_bg_rect)
                question_rect_center = question_bg_rect.center
            else:
                question_rect_center = self.question_pos

            question_text = self.font_large.render(self.current_question["question"], True, COLOR_TEXT)
            question_rect = question_text.get_rect(center=question_rect_center)
            surface.blit(question_text, question_rect)

            # 4. VẼ 4 ĐÁP ÁN (Sử dụng nendapan.png)
            nen_dapan = self.assets['nen_dapan']
            
            # Vị trí các cột
            x_pos_left = SCREEN_WIDTH // 2 - 250
            x_pos_right = SCREEN_WIDTH // 2 + 250 

            for i, answer in enumerate(self.current_question["answers"]):
                # Sắp xếp 2x2:
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
                
                if self.selected_answer_index is not None:
                    if i == self.current_question["correct_index"]:
                        color_overlay = COLOR_CORRECT
                    elif i == self.selected_answer_index: # Nếu chọn sai
                        color_overlay = COLOR_WRONG
                    else:
                        color_overlay = None # Giữ màu nền mặc định/ảnh
                else:
                    color_overlay = None
                
                if color_overlay:
                    # Tạo overlay màu với độ trong suốt nhất định
                    overlay_surf = pygame.Surface(temp_dapan_surf.get_size(), pygame.SRCALPHA)
                    overlay_surf.fill((color_overlay[0], color_overlay[1], color_overlay[2], 150)) # 150 là độ trong suốt
                    temp_dapan_surf.blit(overlay_surf, (0, 0))
                
                # VẼ NỀN ĐÁP ÁN (Hình ảnh nendapan.png đã được xử lý màu)
                surface.blit(temp_dapan_surf, button_rect.topleft)
                
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
                    # Vẽ khung hình tròn xám nếu chưa đạt sao
                    pygame.draw.circle(surface, (150, 150, 150), (star_x + star_width//2, star_y + star_width//2), star_width//2, 2)
                    
            # Nút Quay lại Menu (NEXT)
            if 'nut_next' in self.assets:
                # VẼ HÌNH ẢNH NÚT NEXT
                surface.blit(self.assets['nut_next'], self.game_over_button_rect.topleft)
            else:
                pygame.draw.rect(surface, COLOR_CORRECT, self.game_over_button_rect, border_radius=10)
                
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
    
    # Kích thước nút đáp án đã điều chỉnh để thống nhất trong code
    ANSWER_BUTTON_SIZE = (350, 80)
    GAME_OVER_BUTTON_SIZE = (250, 60)
    STAR_BAR_SIZE = (300, 60)
    
    if not os.path.exists(ASSETS_IMG_DIR): os.makedirs(ASSETS_IMG_DIR)
    if not os.path.exists(ASSETS_FONT_DIR): os.makedirs(ASSETS_FONT_DIR)
        
    def create_dummy_image(name, size, color):
        path = os.path.join(ASSETS_IMG_DIR, name)
        if not os.path.exists(path):
            surf = pygame.Surface(size, pygame.SRCALPHA)
            if len(color) == 3: # Xử lý màu RGB
                surf.fill(color)
            elif len(color) == 4: # Xử lý màu RGBA
                temp_surf = pygame.Surface(size)
                temp_surf.set_colorkey((0, 0, 0)) # Đảm bảo trong suốt
                temp_surf.fill(color[:3])
                temp_surf.set_alpha(color[3])
                surf.blit(temp_surf, (0, 0))
                
            pygame.image.save(surf, path)

    # ĐẢM BẢO TẠO DUMMY CHO CÁC THANH SAO MỚI (CHỈ ĐỂ CHẠY TEST KHÔNG BỊ LỖI FILE)
    create_dummy_image('nenchinh.png', (SCREEN_WIDTH, SCREEN_HEIGHT), (255, 240, 245)) 
    create_dummy_image('nencauhoi.png', (750, 200), (255, 255, 255, 150)) # Kích thước lớn hơn cho câu hỏi
    create_dummy_image('nendapan.png', ANSWER_BUTTON_SIZE, (255, 182, 193, 200)) # Dùng biến ANSWER_BUTTON_SIZE
    create_dummy_image('nut_back.png', (80, 30), COLOR_WRONG) # Kích thước nhỏ hơn
    create_dummy_image('nut_next.png', GAME_OVER_BUTTON_SIZE, COLOR_CORRECT) # Dùng biến GAME_OVER_BUTTON_SIZE
    create_dummy_image('thanh_tiendo.png', (300, 40), (200, 200, 200)) 
    create_dummy_image('game_over.png', (600, 400), (255, 255, 255, 150)) 
    
    # DUMMY CHO THANH SAO
    for i in range(4):
        create_dummy_image(f'thanh_sao_{i}.png', STAR_BAR_SIZE, (100 + i*30, 100 + i*30, 255, 200)) # Thêm độ trong suốt

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