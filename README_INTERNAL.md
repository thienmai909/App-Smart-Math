# 📘 HƯỚNG DẪN TRIỂN KHAI DỰ ÁN: QUIZ GAME MASTER

Chào mọi người, đây là tài liệu hướng dẫn kỹ thuật để chúng ta cùng triển khai dự án. Leader đã dựng xong khung sườn (Framework). Nhiệm vụ của mọi người là điền nội dung (Code & Tài nguyên) vào đúng vị trí được phân công.

## 🛠️ 1. Cài đặt & Chạy thử (Dành cho tất cả)

Trước khi code, hãy đảm bảo máy bạn chạy được dự án:

1.  Cài đặt Python.
2.  Cài đặt thư viện Pygame:
    ```bash
    pip install pygame
    ```
3.  Mở thư mục `QuizGame_Final` bằng VS Code.
4.  Chạy thử file `main.py`. Nếu hiện lên cửa sổ game (dù màn hình đen) là thành công.

-----

## 📂 2. Cấu trúc Dự án (Lưu ý vị trí file của bạn)

```text
QuizGame_Final/
├── assets/                 # [Supporter A] Để ảnh, nhạc, font vào đây
├── data/
│   ├── questions.py        # [Supporter A] Code tạo câu hỏi
│   └── save_manager.py     # [Supporter B] Code lưu điểm
├── src/
│   ├── config.py           # Cấu hình chung (Màu, kích thước...)
│   ├── core/               # [Leader] Đừng sửa file trong này
│   ├── ui/                 # [Improver A & B] Code nút bấm chung
│   └── screens/            # [Improver A & B] Code màn hình chính
│       ├── menu_screen.py          # [Improver A]
│       ├── level_select_screen.py  # [Improver A]
│       └── gameplay_screen.py      # [Improver B]
└── main.py                 # File chạy chính
```

-----

## 👩‍💻 3. HƯỚNG DẪN CHI TIẾT TỪNG VAI TRÒ

### 🟢 IMPROVER A: Màn hình Menu & Chọn Level

**Nhiệm vụ:** Bạn phụ trách dẫn người chơi vào game.
**Files cần làm:** `src/screens/menu_screen.py` và `src/screens/level_select_screen.py`.

**Cách làm:**
Bạn phải kế thừa lớp `BaseScreen`. Copy mẫu dưới đây vào file của bạn và sửa lại phần `draw` và `handle_input`.

**Ví dụ cho `menu_screen.py`:**

```python
import pygame
from src.screens.base_screen import BaseScreen
from src.config import * # Lấy màu sắc, kích thước

class MenuScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # Tải ảnh nút Play/Setting ở đây (dùng pygame.image.load)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra tọa độ chuột có click vào nút Play không
            # Nếu có, chuyển sang màn hình chọn Level:
            self.game_manager.switch_screen("LEVEL_SELECT") 

    def update(self):
        pass # Nếu có hiệu ứng động thì viết vào đây

    def draw(self, surface):
        surface.fill(COLOR_BG)
        # Vẽ ảnh nền, vẽ nút Play lên 'surface'
        # surface.blit(anh_nut_play, (x, y))
```

*Làm tương tự cho `level_select_screen.py` (Vẽ 6 ô level).*

-----

### 🔵 IMPROVER B: Màn hình Chơi Game (Gameplay)

**Nhiệm vụ:** Bạn phụ trách màn hình chính nơi người chơi trả lời câu hỏi.
**Files cần làm:** `src/screens/gameplay_screen.py`.

**Cách làm:**
Tương tự Improver A, bạn kế thừa `BaseScreen`.

**Logic cần nhớ:**

1.  Khi màn hình khởi động, cần lấy câu hỏi (nếu chưa có câu hỏi tạm thời bạn cứ tự tạo dữ liệu giả `mock_question` để hiển thị cho đẹp trước).
2.  Vẽ 4 nút đáp án.
3.  Xử lý sự kiện Click.

**Mẫu code:**

```python
import pygame
from src.screens.base_screen import BaseScreen
from src.config import *

class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # Khởi tạo font, load ảnh nút đáp án...

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem click vào đáp án nào
            # Nếu chọn đáp án, báo lại cho Logic (sau này Leader sẽ ráp nối)
            # Nếu nhấn nút Back/Thoát:
            self.gm.switch_screen("MENU")

    def update(self):
        pass 

    def draw(self, surface):
        surface.fill(COLOR_BG)
        # Vẽ câu hỏi, 4 đáp án, điểm số...
```

-----

### 🟠 SUPPORTER A: Tài nguyên & Tạo Câu hỏi

**Nhiệm vụ 1: Assets (Tài nguyên)**

  * Tìm ảnh đẹp (nền, nút, icon), âm thanh, font chữ.
  * Đặt tên file tiếng Anh, viết thường, không dấu (ví dụ: `btn_play.png`, `bg_menu.jpg`).
  * Copy vào thư mục `assets/images`, `assets/sounds`, `assets/fonts`.

**Nhiệm vụ 2: Code Logic (Quan trọng)**

  * **File:** `data/questions.py`
  * **Yêu cầu:** Viết hàm tạo câu hỏi ngẫu nhiên. KHÔNG dùng `pygame` trong file này.
  * **Mẫu code:**

<!-- end list -->

```python
import random

def get_level_1_questions(amount=20):
    """Level 1: Cộng trừ"""
    questions = []
    for _ in range(amount):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        correct = a + b
        # ... logic tạo đáp án sai ...
        questions.append({
            "question": f"{a} + {b} = ?",
            "options": [correct, 1, 2, 3], # Nhớ trộn ngẫu nhiên
            "answer": correct
        })
    return questions

# Hãy viết tiếp get_level_2, get_level_3...
# Test bằng cách thêm: if __name__ == "__main__": print(get_level_1_questions())
```

-----

### 🟣 SUPPORTER B: Lưu trữ & Tài liệu

**Nhiệm vụ 1: Hệ thống Save/Load**

  * **File:** `data/save_manager.py`
  * **Yêu cầu:** Dùng thư viện `json` để đọc/ghi file.
  * **Mẫu code:**

<!-- end list -->

```python
import json
import os

SAVE_FILE = "data/save.json"

def load_game_data():
    if not os.path.exists(SAVE_FILE):
        return {"highscores": [0]*6, "stars": [0]*6} # Mặc định
    try:
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"highscores": [0]*6, "stars": [0]*6}

def save_game_data(data):
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)
```

**Nhiệm vụ 2: Tester & Docs**

  * Viết báo cáo Word và Slide thuyết trình.
  * Chạy thử game của các bạn Improver, cố gắng tìm lỗi (bug) và báo lại cho Leader.

-----

## ⚠️ QUY TẮC LÀM VIỆC CHUNG

1.  **Không sửa file của người khác:** Improver A chỉ sửa file menu, Improver B chỉ sửa file gameplay.
2.  **Không sửa `main.py` và thư mục `src/core/`:** Đây là phần Leader quản lý, sửa vào sẽ hỏng game.
3.  **Code xong nhớ Test:** Trước khi gửi code, hãy chạy thử xem có lỗi cú pháp (Syntax Error) không.
4.  **Giao tiếp:** Nếu gặp lỗi `ImportError` hoặc không biết cách dùng `self.game_manager.switch_screen`, hãy hỏi Leader ngay.

**Chúc nhóm chúng ta hoàn thành xuất sắc bài tập lớn\! 🚀**