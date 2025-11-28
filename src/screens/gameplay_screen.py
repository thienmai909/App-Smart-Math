
import pygame
from src.screens.base_screen import BaseScreen
# Sửa lại cách import nếu bạn chạy từ thư mục gốc
# Giả sử config đã được tạo
from src.config import * # ------------------------------------------------
# DỮ LIỆU GIẢ LẬP (MOCK DATA)
# ------------------------------------------------
MOCK_QUESTION = {
    "question_text": "Cơ quan nào sau đây không thuộc hệ tiêu hóa?",
    "answers": [
        "A. Dạ dày",
        "B. Gan",
        "C. Tim",
        "D. Ruột non"
    ],
    "correct_answer_index": 2  # C. Tim
}


class GameplayScreen(BaseScreen):
    """Màn hình chính nơi người chơi trả lời câu hỏi."""

    def __init__(self, game_manager):
        # Kế thừa khởi tạo từ BaseScreen (sẽ gọi ABC.__init__)
        super().__init__(game_manager)

        # Khởi tạo Font và Load nội dung
        # Khởi tạo font (đảm bảo font có sẵn, ví dụ: Arial)
        self.font_large = pygame.font.SysFont('Arial', 30)
        self.font_medium = pygame.font.SysFont('Arial', 24)

        # Load câu hỏi giả lập
        self.question_data = MOCK_QUESTION
        self.question_text = self.question_data["question_text"]
        self.answers = self.question_data["answers"]

        # Khởi tạo các Rect (hình chữ nhật) cho các nút/đáp án
        self._setup_layout()

    def _setup_layout(self):
        """Thiết lập vị trí và kích thước cho các thành phần."""
        # Thiết lập vị trí câu hỏi 
        self.question_surface = self.font_large.render(self.question_text, True, WHITE)
        self.question_rect = self.question_surface.get_rect(
            center=(SCREEN_WIDTH // 2, 100)
        )

        # Thiết lập vị trí 4 nút đáp án
        padding_y = 60
        start_y = 200
        button_width = 400
        button_height = 50
        
        self.answer_rects = []
        for i, answer in enumerate(self.answers):
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.center = (SCREEN_WIDTH // 2, start_y + i * padding_y)
            self.answer_rects.append(rect)
            
        # Thiết lập nút Back/Thoát
        self.back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 70, 100, 40)


    # ------------------------------------------------
    # @abstractmethod: Xử lý sự kiện (Click/Phím)
    # ------------------------------------------------
    def handle_input(self, event):
        """Xử lý sự kiện chuột/phím."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # 1. Kiểm tra nút Back/Thoát
            if self.back_button_rect.collidepoint(mouse_pos):
                print("Gameplay: Quay lại Menu")
                self.game_manager.switch_screen("MENU")
                return

            # 2. Kiểm tra click vào đáp án
            for i, rect in enumerate(self.answer_rects):
                if rect.collidepoint(mouse_pos):
                    print(f"Gameplay: Người chơi chọn đáp án {self.answers[i]}")
                    self._handle_answer_selection(i)
                    return

    def _handle_answer_selection(self, selected_index):
        """Logic xử lý khi người chơi chọn một đáp án."""
        correct_index = self.question_data["correct_answer_index"]
        
        if selected_index == correct_index:
            print("Chúc mừng! Đáp án đúng.")
        else:
            print("Rất tiếc! Đáp án sai.")
            
    # ------------------------------------------------
    # @abstractmethod: Cập nhật trạng thái
    # ------------------------------------------------
    def update(self):
        """Cập nhật logic (timer, animation)."""
        # Hiện tại không có logic cập nhật phức tạp, giữ nguyên pass.
        pass

    # ------------------------------------------------
    # @abstractmethod: Vẽ màn hình
    # ------------------------------------------------
    def draw(self, screen):
        """Vẽ tất cả các thành phần lên màn hình."""
        # 1. Vẽ nền (ví dụ: màu đen)
        screen.fill(BLACK) 

        # 2. Vẽ câu hỏi
        screen.blit(self.question_surface, self.question_rect)

        # 3. Vẽ 4 nút đáp án
        for i, rect in enumerate(self.answer_rects):
            answer_text = self.answers[i]
            
            # Vẽ hình chữ nhật của đáp án
            pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=5)
            
            # Vẽ chữ đáp án
            answer_surface = self.font_medium.render(answer_text, True, BLACK)
            text_rect = answer_surface.get_rect(center=rect.center)
            screen.blit(answer_surface, text_rect)

        # 4. Vẽ nút Back/Thoát
        pygame.draw.rect(screen, RED, self.back_button_rect, border_radius=5)
        back_text_surface = self.font_medium.render("Back", True, WHITE)
        back_text_rect = back_text_surface.get_rect(center=self.back_button_rect.center)
        screen.blit(back_text_surface, back_text_rect)