# BÁO CÁO DỰ ÁN: SMART MATH - ỨNG DỤNG HỌC TOÁN THÔNG MINH

---

## 1. GIỚI THIỆU VẤN ĐỀ

### 1.1. Bối cảnh

Trong thời đại công nghệ 4.0, việc ứng dụng công nghệ vào giáo dục đang trở thành xu hướng tất yếu. Việc học toán - môn học nền tảng quan trọng - thường gặp những khó khăn như:

- **Thiếu tính tương tác**: Phương pháp học truyền thống qua sách vở khiến học sinh dễ cảm thấy nhàm chán
- **Không tùy chỉnh theo trình độ**: Các bài tập thường có độ khó cố định, không phù hợp với mọi đối tượng
- **Thiếu động lực học tập**: Học sinh không có phản hồi tức thì và thiếu yếu tố khuyến khích

### 1.2. Mục tiêu dự án

**Smart Math** được phát triển nhằm giải quyết các vấn đề trên thông qua một ứng dụng game học toán với các mục tiêu cụ thể:

✅ **Tăng tính tương tác**: Giao diện game hóa, âm thanh sống động  
✅ **Phân cấp độ khó**: 6 cấp độ từ cơ bản đến nâng cao  
✅ **Tạo động lực**: Hệ thống điểm số, sao, và thời gian tạo thử thách  
✅ **Luyện tập đa dạng**: Bao gồm cộng trừ nhân chia, phân số, tìm X, và phương trình

### 1.3. Đối tượng sử dụng

- Học sinh tiểu học (lớp 1-5): Level 1-3
- Học sinh THCS (lớp 6-9): Level 4-6
- Người muốn rèn luyện tư duy toán học

### 1.4. Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích sử dụng |
|-----------|-----------|------------------|
| **Python** | 3.x | Ngôn ngữ lập trình chính |
| **Pygame** | 2.x | Framework phát triển game 2D, xử lý đồ họa và âm thanh |
| **Pillow** | 10.x | Xử lý và render ảnh GIF animation |
| **JSON** | Built-in | Lưu trữ dữ liệu điểm số và tiến trình (save.json) |
| **Fractions** | Built-in | Xử lý phân số trong Level 5-6 (tự động rút gọn) |
| **Random** | Built-in | Tạo câu hỏi ngẫu nhiên và trộn đáp án |
| **Time** | Built-in | Quản lý bộ đếm thời gian realtime |
| **OS** | Built-in | Xử lý đường dẫn file cross-platform |
| **Math** | Built-in | Tính toán GCD (Greatest Common Divisor) |

### 1.5. Cấu trúc dự án

```
Du-an-phan-mem-hoc-tap-Smart-Math/
│
├── 📄 main.py                       # File khởi chạy chính
├── 📄 requirements.txt              # Danh sách thư viện (pygame, Pillow)
├── 📄 README.md                     # Báo cáo dự án
│
├── 📁 src/                          # Mã nguồn chính
│   ├── 📄 config.py                 # Cấu hình toàn cục
│   │
│   ├── 📁 core/                     # Lõi xử lý game
│   │   ├── game_manager.py          # Bộ não điều khiển game (67 dòng)
│   │   └── load_sounds.py           # Load âm thanh
│   │
│   ├── 📁 screens/                  # Các màn hình
│   │   ├── base_screen.py           # Lớp cơ sở
│   │   ├── home_screen.py           # Màn hình chào mừng
│   │   ├── level_select_screen.py  # Màn chọn level (263 dòng)
│   │   ├── gameplay_screen.py       # Màn chơi chính (668 dòng)
│   │   └── menu_screen.py           # Popup cài đặt (157 dòng)
│   │
│   └── 📁 effects/                  # Hiệu ứng đồ họa (9 files)
│       ├── animation_utils.py       # Tiện ích animation
│       ├── base_effect.py           # Lớp cơ sở effect
│       ├── button_effects.py        # Hiệu ứng nút bấm
│       ├── effect_manager.py        # Quản lý effects
│       ├── gif_animation.py         # Xử lý GIF animation
│       ├── progress_effects.py      # Hiệu ứng thanh tiến độ
│       └── transitions.py           # Chuyển cảnh
│
├── 📁 data/                         # Dữ liệu game
│   ├── questions.py                 # Generator câu hỏi 6 level (391 dòng)
│   ├── save_manager.py              # Lưu/tải JSON (35 dòng)
│   └── save.json                    # File lưu điểm (tự động tạo)
│
└── 📁 assets/                       # Tài nguyên
    ├── 📁 fonts/                    # 4 font chữ
    ├── 📁 images/                   # 40 hình ảnh PNG/GIF
    └── 📁 sounds/                   # 4 file âm thanh MP3
```

**Thống kê:**
- **Tổng số file Python**: 19 files (~1,581 dòng code chính)
- **Tổng tài nguyên**: 48 files (4 fonts + 40 images + 4 sounds)
- **File phức tạp nhất**: `gameplay_screen.py` (668 dòng)
---

## 2. CÁC MODULE CHÍNH

Dự án được tổ chức thành 9 module chính, mỗi module đảm nhiệm một chức năng cụ thể:

| Module | File | Dòng code | Chức năng chính |
|--------|------|-----------|-----------------|
| **Game Manager** | `src/core/game_manager.py` | 67 | Bộ não điều khiển toàn bộ luồng game, quản lý chuyển màn hình |
| **Effect Manager** | `src/effects/effect_manager.py` | 439 | Quản lý hiệu ứng chuyển cảnh (fade, slide, zoom transitions) |
| **Questions Generator** | `data/questions.py` | 391 | Tạo câu hỏi ngẫu nhiên cho 6 cấp độ |
| **Gameplay Screen** | `src/screens/gameplay_screen.py` | 668 | Màn hình chơi chính - phức tạp nhất trong dự án |
| **Level Select Screen** | `src/screens/level_select_screen.py` | 263 | Màn hình chọn level với logic khóa |
| **Home Screen** | `src/screens/home_screen.py` | 54 | Màn hình chào mừng với nút bắt đầu |
| **Menu Screen** | `src/screens/menu_screen.py` | 157 | Popup cài đặt overlay (không phải màn hình độc lập) |
| **Save Manager** | `data/save_manager.py` | 35 | Lưu và tải dữ liệu JSON |
| **Load Sounds** | `src/core/load_sounds.py` | 17 | Load âm thanh vào bộ nhớ (click, yes, no, bgm) |

**Tổng cộng**: ~2,091 dòng code logic chính

---

### 2.1. Module Game Manager (`src/core/game_manager.py`)

**Vai trò**: Bộ não trung tâm điều khiển toàn bộ luồng game

#### Chức năng chính:

```python
class GameManager:
    sounds = _load_sound()  # Load sounds trước khi khởi tạo
    
    def __init__(self):        
        # Khởi tạo 3 màn hình chính
        self.screens = {
            "HOME": HomeScreen(self),
            "LEVEL": LevelSelectScreen(self),
            "GAMEPLAY": GameplayScreen(self),
        }
        
        # Màn hình hiện tại
        self.active_screen_key = "HOME"
        self.active_screen = self.screens[self.active_screen_key]
        self.current_level_key = None  # Level đã chọn (VD: "LEVEL_1")
        
        # Menu Settings (popup, không phải screen)
        self.menu = MenuScreen(self)
        
        # Tải dữ liệu điểm và sao đã lưu
        self.game_data = load_game_data()
        
        # Phát nhạc nền lặp lại
        pygame.mixer.music.play(loops=-1)
        
        # Bộ câu hỏi cho level hiện tại
        self.questions_pool = [] 
        self.question_index = 0
```

**Giải thích**:
- `menu`: MenuScreen là POPUP overlay, không phải màn hình độc lập
- `sounds`: Được load ở class level, dùng chung cho toàn bộ game
- `questions_pool`: Chứa 20 câu hỏi được tạo khi chọn level

#### Chuyển màn hình và tạo câu hỏi:

```python
def switch_screen(self, screen_key):
    if screen_key in self.screens:
        # Khi chuyển đến màn hình chơi, tạo câu hỏi
        if screen_key == "GAMEPLAY" and self.current_level_key:
            generator = QUESTION_GENERATORS.get(self.current_level_key)
            if generator:
                # Tạo 20 câu hỏi ngẫu nhiên
                generated_questions = generator(MAX_QUESTIONS)
                self.questions_pool = generated_questions
                self.question_index = 0
            else:
                print(f"Không tìm thấy generator cho level: {self.current_level_key}")
                self. = []
                
            # Gọi on_enter() để reset trạng thái gameplay
            self.screens[screen_key].on_enter()
                
        self.active_screen_key = screen_key
        self.active_screen = self.screens[self.active_screen_key]
```

**Điểm quan trọng**:
- Generator được lấy từ dictionary `QUESTION_GENERATORS` trong `questions.py`
- `on_enter()` được gọi để reset điểm, timer, và load câu hỏi đầu tiên

---

### 2.2. Module Questions Generator (`data/questions.py`)

**Vai trò**: Tạo câu hỏi toán học ngẫu nhiên cho 6 cấp độ

#### Cấu trúc Level:

Mỗi câu hỏi được trả về dạng dictionary:

```python
{
    "prefix": "Hãy thực hiện phép toán sau:",  # Tiêu đề câu hỏi
    "question": "45 + 67 = ?",                 # Nội dung câu hỏi
    "options": [112, 100, 120, 95],            # 4 đáp án (đã shuffle)
    "answer": 112                               # Đáp án đúng
}
```

#### Level 1 - Cộng Trừ với độ khó tăng dần

```python
def get_level_1_questions(num_questions=20):
    questions = []
    prefix = "Hãy thực hiện phép toán sau:"
    
    for i in range(num_questions):
        # Độ khó tăng dần theo chỉ số
        if i < 10:
            a = random.randint(1, 20)
            b = random.randint(1, 20)
            max_for_options = 50
        elif i >= 10 and i < 17:
            a = random.randint(10, 25)
            b = random.randint(10, 25)
            max_for_options = 70
        else:
            a = random.randint(40, 99)
            b = random.randint(40, 99)
            max_for_options = 200
            
        if random.choice([True, False]):
            question_content = f"{a} + {b} = ?"
            correct_answer = a + b
        else:
            # Đảm bảo kết quả không âm
            if a < b:
                a, b = b, a
            question_content = f"{a} - {b} = ?"
            correct_answer = a - b
        
        options = _create_options(correct_answer, min_val=0, max_val=max_for_options)
        
        questions.append({
            "prefix": prefix,
            "question": question_content,
            "options": options,
            "answer": correct_answer
        })
    return questions
```

**Điểm nổi bật**:
- Câu đầu dễ (1-20), càng về sau càng khó (đến 40-99)
- Đảm bảo kết quả phép trừ không âm bằng cách swap `a` và `b`

#### Level 5 - Phân số với `answer_index`

```python
def get_level_5_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        type_q = random.choice(["rutgon", "cong", "tru", "nhan", "chia"])
        
        if type_q == "cong":
            f1 = Fraction(random.randint(1, 12), random.randint(2, 12))
            f2 = Fraction(random.randint(1, 12), random.randint(2, 12))
            result = f1 + f2  # Python tự quy đồng và rút gọn
            question_content = f"{f1.numerator}/{f1.denominator} + {f2.numerator}/{f2.denominator} = ?"
            correct_str = f"{result.numerator}/{result.denominator}"
        
        # ... các type khác tương tự
        
        options = _create_fraction_options(Fraction(correct_str))
        
        questions.append({
            "prefix": "Hãy thực hiện phân số sau:",
            "question": question_content,
            "options": options,  # VD: ["3/4", "2/3", "5/8", "1/2"]
            "answer": correct_str,
            "answer_index": options.index(correct_str)  # QUAN TRỌNG!
        })
    return questions
```

**Điểm đặc biệt**:
- Trường `answer_index` giúp GameplayScreen biết KHÔNG SHUFFLE đáp án
- Thư viện `Fraction` tự động rút gọn phân số

---

### 2.3. Module Gameplay Screen (`src/screens/gameplay_screen.py`)

**Vai trò**: Màn hình chơi chính - 668 dòng code, phức tạp nhất trong dự án

#### 2.3.1. Khởi tạo màn hình

```python
class GameplayScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # Khởi tạo hệ thống font với fallback
        try:
            if os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_question = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_LARGE)
                self.font_medium = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_MEDIUM)
            else:
                # Fallback sang system font
                self.font_question = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
                self.font_medium = pygame.font.SysFont("Arial", FONT_SIZE_MEDIUM)
        except:
            self.font_question = pygame.font.SysFont("Arial", FONT_SIZE_LARGE)
        
        # Trạng thái game
        self.score = 0
        self.best_score = 0
        self.time_left = TIME_LIMIT  # 30 giây
        self.game_over = False
        self.is_new_best = False  # Phá kỷ lục (nhưng không perfect)
        self.is_perfect = False   # Điểm tuyệt đối (200/200)
        
        self.assets = self._load_assets()
```

#### 2.3.2. Tải câu hỏi với logic trộn có điều kiện

```python
def load_next_question(self):
    if self.game_manager.question_index < len(self.game_manager.questions_pool):
        q_data = self.game_manager.questions_pool[self.game_manager.question_index]
        answers = [str(o) for o in q_data["options"]]
        correct_answer = str(q_data["answer"])
        
        # CHỈ SHUFFLE NẾU KHÔNG CÓ answer_index
        # Level 5 (phân số) có answer_index → giữ nguyên thứ tự
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
        
        # Reset timer
        self.start_time = time.time()
        self.time_left = self.time_limit
        self.game_manager.question_index += 1
    else:
        # Hết câu hỏi
        self.game_over = True
        self.final_stars = self.calculate_stars(self.score)
        self.save_score(self.score)
```

**Giải thích**:
- `if "answer_index" not in q_data`: Kiểm tra có phải Level 5 không
- Level 5 không shuffle để giữ nguyên thứ tự đáp án phân số

#### 2.3.3. Xử lý đáp án với phản hồi không bị chặn

```python
def process_answer(self, selected_index):
    # Phát âm click
    if selected_index >= 0 and self.game_manager.sounds:
        if 'click' in self.game_manager.sounds and self.game_manager.menu.sound_setting:
            self.game_manager.sounds['click'].play()
            
    self.selected_answer_index = selected_index
    
    if selected_index >= 0:
        is_correct = (selected_index == self.current_question["correct_index"])
        if is_correct:
            self.score += POINTS_CORRECT  # +10
            self._play_sound('yes')
        else:
            self.score = max(0, self.score + POINTS_WRONG)  # -5, không âm
            self._play_sound('no')
    else:  # Hết giờ (selected_index = -2)
        self.score = max(0, self.score + POINTS_WRONG)
        self._play_sound('no')
    
    # ĐẶT THỜI ĐIỂM KẾT THÚC FEEDBACK (NON-BLOCKING!)
    self.show_feedback_until = time.time() + 1.5  # 1.5 giây
```

**Điểm quan trọng**:
- KHÔNG dùng `pygame.time.delay()` vì nó block toàn bộ game
- Dùng `show_feedback_until` và kiểm tra trong `update()`

#### 2.3.4. Update loop với bộ điếm thời gian thực
```python
def update(self):
    # Nếu popup settings đang mở, chỉ update popup
    if hasattr(self.game_manager, 'menu') and self.game_manager.menu.show_settings:
        self.game_manager.menu.update()
        return
    
    if self.game_over: 
        return
    
    current_time = time.time()
    
    # Đếm ngược thời gian (REALTIME, không phải frame-based)
    if self.selected_answer_index is None:
        time_spent = current_time - self.start_time
        self.time_left = max(0, int(self.time_limit - time_spent))
        
        # Hết giờ → tự động trả lời sai
        if self.time_left <= 0: 
            self.process_answer(-2)
    
    # Tự động chuyển câu sau khi hiển thị feedback đủ 1.5s
    if self.selected_answer_index is not None and current_time >= self.show_feedback_until:
        self.load_next_question()
```

**Giải thích**:
- `time.time()`: Thời gian thực (giây), không phụ thuộc FPS
- Tự động chuyển câu khi `current_time >= show_feedback_until`

#### 2.3.5. Parsing biểu thức toán học

```python
def parse_math_expression(self, expression):
    """
    Phân tích biểu thức thành [(type, value), ...]
    VD: "6/8 + 3/7" → [("fraction", "6/8"), ("operator", "+"), ("fraction", "3/7")]
    """
    components = []
    i = 0
    expression = expression.strip()
    
    while i < len(expression):
        # Bỏ qua khoảng trắng
        if expression[i].isspace():
            i += 1
            continue
        
        # Kiểm tra toán tử (hỗ trợ cả − và ÷)
        if expression[i] in ['+', '-', '×', ':', '−', '÷']:
            components.append(("operator", expression[i]))
            i += 1
            continue
        
        # Tìm token số hoặc phân số
        start = i
        while i < len(expression) and expression[i] not in ['+', '-', '×', ':', '−', '÷']:
            i += 1
        
        token = expression[start:i].strip()
        
        if '/' in token:
            components.append(("fraction", token))
        elif token:
            components.append(("number", token))
    
    return components
```

**Điểm nổi bật**:
- Duyệt từng ký tự, không dùng `split()`
- Hỗ trợ toán tử đặc biệt: `−` (minus sign Unicode), `÷` (division sign)

#### 2.3.6. Vẽ câu hỏi với logic đặc biệt cho Level 4/6

```python
def draw(self, surface):
    if not self.game_over and self.current_question:
        q_text = self.current_question["question"]
        
        # LOGIC ĐẶC BIỆT CHO LEVEL TÌM X
        current_level = self.game_manager.current_level_key
        is_find_x_level = current_level in ["LEVEL_4", "LEVEL_6"]
        
        if is_find_x_level:
            # Hiển thị toàn bộ: "3x + 5 = 20" (không thêm "= ?")
            math_part = q_text
            eq_text = ""
        else:
            # Cắt phần sau "=" và thêm "= ?"
            # "45 + 67 = 112" → vẽ "45 + 67" + "= ?"
            math_part = q_text.split("=")[0].strip() if "=" in q_text else q_text
            eq_text = "= ?" if "=" in q_text else ""
        
        # Render "= ?"
        eq_surf = self.font_question.render(eq_text, True, COLOR_BLACK)
        
        # Vẽ math_part bằng hàm draw_math_expression()
        self.draw_math_expression(surface, math_part, center_pos, self.font_question, COLOR_BLACK)
        
        # Vẽ "= ?" bên cạnh
        if eq_text:
            surface.blit(eq_surf, ...)
```

**Điểm quan trọng**:
- Level 4và 6 (tìm X): Hiển thị nguyên câu hỏi `"3x + 5 = 20"`
- Các level khác: Cắt sau `=` và thêm `= ?`

#### 2.3.7. Tự động giãn kích thước theo nội dung

```python
def draw(self, surface):
    # ... (tiếp theo phần trên)
    
    # Tính toán kích thước nội dung bằng parser
    components = self.parse_math_expression(math_part)
    
    f_w = 0  # Total width
    f_h = 0  # Max height
    
    for comp_type, comp_value in components:
        if comp_type == "fraction":
            parts = comp_value.split("/")
            num_size = self.font_question.size(parts[0].strip())
            den_size = self.font_question.size(parts[1].strip())
            comp_w = max(num_size[0], den_size[0]) + 20
            comp_h = num_size[1] + den_size[1] + 20
        elif comp_type == "operator":
            comp_w, comp_h = self.font_question.size(f" {comp_value} ")
        else:  # number
            comp_w, comp_h = self.font_question.size(comp_value)
        
        f_w += comp_w
        f_h = max(f_h, comp_h)
    
    # ĐIỀU CHỈNH KHUNG CÂU HỎI LINH HOẠT
    dynamic_q_width = max(950, f_w + eq_surf.get_width() + 120)
    dynamic_q_height = max(200, f_h + 100)
    
    # Scale ảnh nền câu hỏi theo kích thước động
    q_bg_img = pygame.transform.smoothscale(
        self.assets['nen_cauhoi'],
        (int(dynamic_q_width), int(dynamic_q_height))
    )
    q_bg_rect = q_bg_img.get_rect(center=self.question_pos)
    surface.blit(q_bg_img, q_bg_rect)
```

**Tương tự cho đáp án**:

```python
# ĐIỀU CHỈNH NÚT ĐÁP ÁN
for i, opt_text in enumerate(self.current_question["answers"]):
    # Tính kích thước đáp án
    if "/" in opt_text:
        opt_parts = opt_text.split("/")
        num_size = self.font_medium.size(opt_parts[0].strip())
        den_size = self.font_medium.size(opt_parts[1].strip())
        opt_w = max(num_size[0], den_size[0])
        opt_h = num_size[1] + den_size[1]
    else:
        opt_w, opt_h = self.font_medium.size(opt_text)
    
    # Dynamic sizing (min 350x80)
    dynamic_ans_width = max(350, opt_w + 100)
    dynamic_ans_height = max(80, opt_h + 20)
    
    rect = pygame.Rect(0, 0, int(dynamic_ans_width), int(dynamic_ans_height))
    # ... vị trí và vẽ
    
    ans_img = pygame.transform.smoothscale(
        self.assets['nen_dapan'],
        (rect.width, rect.height)
    )
    surface.blit(ans_img, rect.topleft)
```

**Ý nghĩa**:
- Khung câu hỏi và nút đáp án TỰ ĐỘNG GIÃN kích thước
- Phân số cao → khung cao hơn
- Biểu thức dài → khung rộng hơn

#### 2.3.8. Thanh tiến độ với cột mốc sao

```python
def draw(self, surface):
    # ... vẽ thanh tiến độ
    
    progress_bar_bg = self.assets['thanh_sao_0']
    bar_pos_rect = progress_bar_bg.get_rect(center=(SCREEN_WIDTH // 2, ...))
    surface.blit(progress_bar_bg, bar_pos_rect.topleft)
    
    # Tính tỷ lệ điểm
    max_level_score = len(self.game_manager.questions_pool) * POINTS_CORRECT
    score_ratio = min(1.0, self.score / max_level_score) if max_level_score > 0 else 0
    
    # Vẽ phần fill màu vàng
    INNER_PADDING_X, INNER_PADDING_Y = 15, 10
    fill_max_w = bar_pos_rect.width - (2 * INNER_PADDING_X)
    current_fill_w = int(fill_max_w * score_ratio)
    
    if current_fill_w > 0:
        fill_color = (255, 215, 0)  # Vàng
        fill_height = bar_pos_rect.height - (2 * INNER_PADDING_Y)
        radius = fill_height // 2
        start_x = bar_pos_rect.x + INNER_PADDING_X
        start_y = bar_pos_rect.y + INNER_PADDING_Y
        
        # Vẽ với border radius
        pygame.draw.circle(surface, fill_color, (start_x + radius, start_y + radius), radius)
        if current_fill_w > radius:
            pygame.draw.rect(surface, fill_color, 
                           pygame.Rect(start_x, start_y, current_fill_w, fill_height),
                           border_radius=radius)
    
    # VẼ 3 SAO MILESTONE TẠI 50%, 75%, 95%
    star_icon_small = pygame.transform.scale(self.assets['sao_large'], (30, 30))
    star_milestones = [0.50, 0.75, 0.95]
    
    for milestone in star_milestones:
        star_x = bar_pos_rect.x + INNER_PADDING_X + int(fill_max_w * milestone)
        star_rect = star_icon_small.get_rect(center=(star_x, bar_pos_rect.centery))
        
        if score_ratio >= milestone:
            # Sao sáng
            surface.blit(star_icon_small, star_rect)
        else:
            # Sao tối (chưa đạt)
            dark_star = star_icon_small.copy()
            dark_star.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
            surface.blit(dark_star, star_rect)
```

**Điểm nổi bật**:
- 3 milestone: 50% (1 sao), 75% (2 sao), 95% (3 sao)
- Sao tối đen khi chưa đạt mốc

#### 2.3.9. Lưu điểm với is_perfect và is_new_best

```python
def save_score(self, new_score):
    if not self.game_manager.current_level_key: 
        return
    
    max_possible_score = len(self.game_manager.questions_pool) * POINTS_CORRECT
    scores_data = self.game_manager.game_data.get('scores', {})
    level_key = self.game_manager.current_level_key
    level_data = scores_data.get(level_key, {'high_score': 0})
    
    # LOGIC PHÂN BIỆT PERFECT VÀ NEW BEST
    if new_score >= max_possible_score and max_possible_score > 0:
        # Điểm tuyệt đối (200/200)
        self.is_perfect = True
        self.is_new_best = False
    elif new_score > level_data['high_score']:
        # Phá kỷ lục (nhưng không perfect)
        self.is_new_best = True
        self.is_perfect = False
        
    # Lưu điểm cao
    if new_score > level_data['high_score']:
        level_data['high_score'] = new_score
        scores_data[level_key] = level_data
        self.game_manager.game_data['scores'] = scores_data
    
    # Lưu sao
    new_stars = self.calculate_stars(new_score)
    current_stars = self.game_manager.game_data.get('stars', [0] * len(LEVELS))
    try:
        idx = next(i for i, lv in enumerate(LEVELS) if lv['key'] == level_key)
        if new_stars > current_stars[idx]:
            current_stars[idx] = new_stars
            self.game_manager.game_data['stars'] = current_stars
    except: 
        pass
    
    save_game_data(self.game_manager.game_data)
```

**Giải thích**:
- `is_perfect`: Đạt 200/200 điểm → hiện ảnh `perfect_score.png`
- `is_new_best`: Phá kỷ lục cũ (nhưng không perfect) → hiện ảnh `new_best_score.png`

#### 2.3.10. Màn hình kết quả

```python
def draw(self, surface):
    if self.game_over:
        # Overlay tối
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        # Vẽ ảnh game over
        go_rect = self.assets['game_over_image'].get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(self.assets['game_over_image'], go_rect)
        
        # CHỌN HÌNH ẢNH KẾT QUẢ
        res_img = None
        if self.is_perfect: 
            res_img = self.assets['img_perfect']
        elif self.is_new_best: 
            res_img = self.assets['img_new_best']
        
        if res_img:
            res_rect = res_img.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery))
            surface.blit(res_img, res_rect)
        
        # Điểm hiện tại (màu đỏ)
        score_txt = self.font_title.render(f"{self.score}", True, (255, 0, 0))
        surface.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery)))
        
        # Best score (màu xám)
        best_score_txt = self.font_title.render(f"{self.best_score}", True, (55, 55, 55))
        surface.blit(best_score_txt, best_score_txt.get_rect(center=(SCREEN_WIDTH//2, go_rect.centery + 130)))
        
        # VẼ 3 SAO
        if not self.is_perfect or not self.is_new_best:
            star_base_x = SCREEN_WIDTH // 2 - 90
            for i in range(1, 4):
                single_star = self.assets['sao_result'].copy()
                
                # Làm tối sao chưa đạt
                if i > self.final_stars:
                    gray_filter = pygame.Surface(single_star.get_size(), pygame.SRCALPHA)
                    gray_filter.fill((40, 40, 40, 190))
                    single_star.blit(gray_filter, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                
                surface.blit(single_star, (star_base_x + (i-1)*90 - 40, go_rect.centery - 170))
        
        # Nút Next và Replay
        surface.blit(self.assets['nut_next'], self.next_button_rect.topleft)
        surface.blit(self.assets['nut_relay'], self.replay_button_rect.topleft)
```

---

### 2.4. Module Level Select Screen (`src/screens/level_select_screen.py`)

**Vai trò**: Màn hình chọn level - 263 dòng code, quản lý việc hiển thị 6 level với logic khóa

#### 2.4.1. Khởi tạo màn hình

```python
class LevelSelectScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # Khởi tạo font với fallback
        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_title = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_TITLE)
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL)
            else:
                self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        except pygame.error:
            # Fallback cuối cùng
            self.font_title = pygame.font.SysFont("Arial", FONT_SIZE_TITLE)
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        
        # Danh sách rect của các nút level (được tính lại mỗi frame)
        self.level_rects = []
        
        # Nút cài đặt
        self.setting_button_rect = pygame.Rect(0, 0, 1, 1)
        
        # Tải assets
        self.assets = self._load_assets()
```

**Giải thích**:
- `level_rects`: Mảng chứa vị trí và index của 6 nút level, được reset mỗi frame trong `draw()`
- Font system tương tự GameplayScreen với fallback mechanism

#### 2.4.2. Vẽ layout 6 level (2 hàng × 3 cột)

```python
def draw(self, surface):
    self.level_rects = []  # Reset mỗi frame
    
    # Vẽ nền
    surface.blit(self.assets['nen_lv'], (0, 0))
    
    # Lấy dữ liệu sao
    stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS))
    
    # Thông số layout
    level_button_width = 200
    level_button_height = 55
    padding_x = 80  # Khoảng cách ngang giữa các nút
    padding_y = 80  # Khoảng cách dọc giữa các hàng
    
    # Tính toán vị trí bắt đầu để căn giữa màn hình
    # 3 cột × 200px + 2 khoảng cách × 80px
    total_width_row = (level_button_width * 3) + (padding_x * 2)
    start_x = (SCREEN_WIDTH - total_width_row) // 2
    start_y = 250  # Vị trí Y cố định
    
    for i, level in enumerate(LEVELS):
        # Tính vị trí hàng và cột
        row = i // 3  # 0, 0, 0, 1, 1, 1
        col = i % 3   # 0, 1, 2, 0, 1, 2
        
        x_pos = start_x + col * (level_button_width + padding_x)
        y_pos = start_y + row * (level_button_height + padding_y)
        
        button_rect = pygame.Rect(x_pos, y_pos, level_button_width, level_button_height)
        
        # Lưu rect để xử lý click sau
        self.level_rects.append({'index': i, 'rect': button_rect})
        
        # ... vẽ level (tiếp theo)
```

**Giải thích**:
- Layout grid 2×3: `row = i // 3`, `col = i % 3`
- Căn giữa toàn bộ grid bằng cách tính `total_width_row`
- `level_rects` được cập nhật mỗi frame để đảm bảo collision detection chính xác

#### 2.4.3. Logic khóa level

```python
# ... (tiếp theo trong vòng for)

# Level 1 (index 0) luôn mở
# Level 2-6 chỉ mở khi level trước có >= 1 sao
is_locked = (i > 0 and stars_data[i-1] == 0)

# Vẽ icon level bình thường
level_image = self.assets.get(level['image_key'])  # VD: 'lv1', 'lv2'
if level_image:
    surface.blit(level_image, button_rect.topleft)

# Vẽ số sao đã đạt (nếu có)
current_stars_level = stars_data[i]
if current_stars_level > 0:
    star_asset = self.assets.get('star_icon')
    if star_asset:
        star_size = star_asset.get_width()  # 20px
        
        # Tính tổng chiều rộng để căn giữa khối sao
        star_spacing = 4  # Khoảng cách giữa các sao
        total_stars_width = (current_stars_level * star_size) + \
                           ((current_stars_level - 1) * star_spacing)
        
        # Vị trí X bắt đầu (căn giữa)
        start_star_x = button_rect.centerx - (total_stars_width // 2)
        star_y = button_rect.bottom - star_size + 20  # Gần đáy nút
        
        # Vẽ từng sao
        for star_index in range(current_stars_level):
            star_x = start_star_x + star_index * (star_size + star_spacing)
            surface.blit(star_asset, (star_x, star_y))

# Vẽ icon khóa nếu level bị khóa
if is_locked:
    khoa_asset = self.assets['khoalv']
    # Căn giữa icon khóa trong nút
    khoa_rect = khoa_asset.get_rect(center=button_rect.center)
    surface.blit(khoa_asset, khoa_rect.topleft)
```

**Giải thích**:
- `is_locked`: Kiểm tra `i > 0` (không phải level 1) VÀ `stars_data[i-1] == 0` (level trước chưa có sao)
- Sao được căn giữa bằng cách tính `total_stars_width`
- Icon khóa được vẽ đè lên level bị khóa

#### 2.4.4. Xử lý click với hệ thống ưu tiên

```python
def handle_input(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        
        # ƯU TIÊN 1: Nếu popup settings đang mở, chỉ xử lý popup
        if self.game_manager.menu.show_settings:
            self.game_manager.menu.handle_input(event)
            return  # Không xử lý gì khác
        
        # ƯU TIÊN 2: Click nút cài đặt → mở popup
        if self.setting_button_rect.collidepoint(mouse_pos):
            self.game_manager.menu.show_settings = True
            return
        
        # ƯU TIÊN 3: Click vào level
        for rect_data in self.level_rects:
            i = rect_data['index']
            rect = rect_data['rect']
            
            if rect.collidepoint(mouse_pos):
                # Phát âm thanh click
                self.game_manager.sounds['click'].play()
                
                # Lấy dữ liệu sao để kiểm tra khóa
                stars_data = self.game_manager.game_data.get('stars', [0] * len(LEVELS))
                is_locked = (i > 0 and stars_data[i-1] == 0)
                
                if not is_locked:
                    # Level mở → chuyển sang gameplay
                    selected_level = LEVELS[i]
                    self.game_manager.current_level_key = selected_level['key']
                    print(f"Bạn đã chọn: {self.game_manager.current_level_key}")
                    self.game_manager.switch_screen("GAMEPLAY")
                    return
                else:
                    # Level khóa → in thông báo (hoặc phát âm lỗi)
                    print("Level đang bị khóa!")
                    return
```

**Giải thích chi tiết**:
1. **Priority 1 - Popup**: Nếu popup settings đang mở, chỉ xử lý event cho popup, ignore các click khác
2. **Priority 2 - Settings button**: Click nút cài đặt → set `show_settings = True`
3. **Priority 3 - Level selection**: Click level → kiểm tra khóa → chuyển màn hình
4. **Tại sao dùng priority system?** Tránh click xuyên qua popup (click nhầm level khi popup đang mở)

---

### 2.5. Module Menu Screen (`src/screens/menu_screen.py`)

**Vai trò**: POPUP cài đặt overlay - 157 dòng code, không phải màn hình độc lập

#### 2.5.1. Khởi tạo popup

```python
class MenuScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # Trạng thái popup
        self.show_settings = False  # False = ẩn, True = hiện
        self.sound_setting = True   # True = bật âm thanh
        self.bgm_setting = True     # True = bật nhạc nền
        
        # Tải assets (ảnh nền popup, toggle on/off, nút)
        self.assets = self._load_assets()
        
        # Khởi tạo font
        try:
            if VIETNAMESE_FONT_PATH and os.path.exists(VIETNAMESE_FONT_PATH):
                self.font_small = pygame.font.Font(VIETNAMESE_FONT_PATH, FONT_SIZE_SMALL)
            else:
                self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        except pygame.error:
            self.font_small = pygame.font.SysFont("Arial", FONT_SIZE_SMALL)
        
        # Vị trí các thành phần trong popup (400×450px)
        self.settings_rect = self.assets['nen_caidat'].get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        
        # Nút đóng (X) ở góc trên phải
        self.close_rect = pygame.Rect(
            self.settings_rect.right - 40,
            self.settings_rect.y + 10,
            30, 30
        )
        
        # 4 dòng chức năng
        self.sound_rect = pygame.Rect(
            self.settings_rect.x + 50,
            self.settings_rect.y + 120,
            300, 50
        )
        self.bgm_rect = pygame.Rect(
            self.settings_rect.x + 50,
            self.settings_rect.y + 190,
            300, 50
        )
        self.home_rect = pygame.Rect(
            self.settings_rect.x + 50,
            self.settings_rect.y + 280,
            300, 50
        )
        self.replay_rect = pygame.Rect(
            self.settings_rect.x + 50,
            self.settings_rect.y + 360,
            300, 50
        )
```

**Giải thích**:
- `show_settings`: Biến boolean điều khiển hiển thị popup, được set bởi nút cài đặt
- Popup căn giữa màn hình: `center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)`
- 4 rect chức năng: Sound on/off, BGM on/off, Home, Replay

#### 2.5.2. Vẽ popup với lớp phủ tối

```python
def draw(self, surface):
    """Vẽ popup lên trên màn hình hiện tại (không thay thế màn hình)"""
    
    # BƯỚC 1: Vẽ overlay tối phía sau
    # pygame.SRCALPHA = hỗ trợ trong suốt
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # Màu đen, alpha = 150/255 ≈ 59% trong suốt
    surface.blit(overlay, (0, 0))
    
    # BƯỚC 2: Vẽ khung popup (400×450px)
    surface.blit(self.assets['nen_caidat'], self.settings_rect.topleft)
    
    # BƯỚC 3: Vẽ toggle on/off cho Sound
    # Chọn icon dựa trên trạng thái
    sound_icon = self.assets['on'] if self.sound_setting else self.assets['off']
    sound_icon_rect = sound_icon.get_rect(
        midright=(self.settings_rect.right - 40, self.sound_rect.centery)
    )
    surface.blit(sound_icon, sound_icon_rect.topleft)
    
    # BƯỚC 4: Vẽ toggle on/off cho BGM
    bgm_icon = self.assets['on'] if self.bgm_setting else self.assets['off']
    bgm_icon_rect = bgm_icon.get_rect(
        midright=(self.settings_rect.right - 40, self.bgm_rect.centery)
    )
    surface.blit(bgm_icon, bgm_icon_rect.topleft)
    
    # BƯỚC 5: Vẽ icon nút Home (back arrow)
    if 'nut_back_icon' in self.assets:
        icon_asset = self.assets['nut_back_icon']
        icon_rect = icon_asset.get_rect(
            midright=(self.home_rect.right - 0, self.home_rect.centery)
        )
        surface.blit(icon_asset, icon_rect.topleft)
    
    # BƯỚC 6: Vẽ icon nút Replay (play icon)
    if 'nut_play_icon' in self.assets:
        icon_asset = self.assets['nut_play_icon']
        icon_rect = icon_asset.get_rect(
            midright=(self.replay_rect.right - 0, self.replay_rect.centery)
        )
        surface.blit(icon_asset, icon_rect.topleft)
    
    # BƯỚC 7: Vẽ nút đóng (X) bằng hình tròn + text
    pygame.draw.circle(surface, COLOR_WRONG, self.close_rect.center, 15)
    close_text = self.font_small.render("X", True, COLOR_WHITE)
    close_text_rect = close_text.get_rect(center=self.close_rect.center)
    surface.blit(close_text, close_text_rect)
```

**Giải thích chi tiết**:
- **Overlay**: `fill((0, 0, 0, 150))` tạo lớp đen trong suốt che mờ màn hình phía sau
- **Conditional rendering**: `self.assets['on'] if self.sound_setting else self.assets['off']`
- **midright alignment**: Icon toggle căn lề phải trong popup
- **Circle + Text**: Nút X được vẽ bằng `draw.circle()` + render text

#### 2.5.3. Xử lý click trong popup

```python
def handle_input(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        
        # Click nút X → đóng popup
        if self.close_rect.collidepoint(mouse_pos):
            self.show_settings = False
            return
        
        # Click toggle Sound
        if self.sound_rect.collidepoint(mouse_pos):
            self.sound_setting = not self.sound_setting  # Đổi True ↔ False
            # Logic điều khiển sẽ được xử lý trong update()
            return
        
        # Click toggle BGM
        elif self.bgm_rect.collidepoint(mouse_pos):
            self.bgm_setting = not self.bgm_setting
            return
        
        # Click Home → về màn hình chính + đóng popup
        elif self.home_rect.collidepoint(mouse_pos):
            self.game_manager.switch_screen("HOME")
            self.show_settings = False
            
            # Nếu đang trong gameplay, reset game
            if self.game_manager.active_screen_key == "GAMEPLAY":
                self.game_manager.screens[self.game_manager.active_screen_key].reset_game()
            return
        
        # Click Replay → chơi lại từ đầu
        elif self.replay_rect.collidepoint(mouse_pos):
            self.show_settings = False
            
            if self.game_manager.active_screen_key == "GAMEPLAY":
                # Reset index câu hỏi về 0
                self.game_manager.question_index = 0
                # Reset game state
                self.game_manager.screens[self.game_manager.active_screen_key].reset_game()
                # Load câu hỏi đầu tiên
                self.game_manager.screens[self.game_manager.active_screen_key].load_next_question()
            else:
                # Nếu không phải gameplay, về Home
                self.game_manager.switch_screen("HOME")
            return
```

**Giải thích**:
- **Toggle logic**: `not self.sound_setting` đảo ngược True thành False và ngược lại
- **Home button**: Reset game nếu đang trong gameplay để tránh lỗi state
- **Replay button**: Khác nhau tùy màn hình - gameplay thì replay, màn khác thì về Home

#### 2.5.4. Update điều khiển âm thanh thời gian thực

```python
def update(self):
    """Được gọi mỗi frame để cập nhật trạng thái âm thanh"""
    
    # Điều khiển nhạc nền (Background Music)
    if self.bgm_setting:
        pygame.mixer.music.unpause()  # Tiếp tục phát
    else:
        pygame.mixer.music.pause()    # Tạm dừng (không stop, giữ vị trí)
    
    # Điều khiển âm thanh hiệu ứng (Sound Effects)
    if self.sound_setting:
        # Bật âm thanh → volume = 1.0 (100%)
        self.game_manager.sounds['click'].set_volume(1.0)
        # Các sound khác cũng tương tự
    else:
        # Tắt âm thanh → volume = 0.0 (0%, mute)
        self.game_manager.sounds['click'].set_volume(0.0)
```

**Giải thích**:
- **pause() vs stop()**: `pause()` giữ vị trí, `stop()` về đầu track
- **set_volume()**: Điều chỉnh âm lượng từ 0.0 (mute) đến 1.0 (max)
- **Realtime**: Được gọi mỗi frame, thay đổi setting ngay lập tức có hiệu lực

---

### 2.6. Module Save Manager (`data/save_manager.py`)

**Vai trò**: Lưu và tải dữ liệu JSON - 35 dòng code, xử lý persistence

#### 2.6.1. Đường dẫn file save

```python
import json
import os

# Tên file lưu trữ nằm cùng thư mục data/
SAVE_FILE = os.path.join(os.path.dirname(__file__), "save.json")
```

**Giải thích**:
- `__file__`: Đường dẫn tuyệt đối đến file `save_manager.py`
- `os.path.dirname(__file__)`: Lấy thư mục chứa file (thư mục `data/`)
- `os.path.join()`: Nối đường dẫn cross-platform (Windows/Linux/Mac)
- Kết quả: `d:\...\Du-an-phan-mem-hoc-tap-Smart-Math\data\save.json`

#### 2.6.2. Load dữ liệu với error handling

```python
def load_game_data():
    """Tải dữ liệu điểm cao và sao đã lưu. Nếu không có file, trả về mặc định."""
    
    # Dữ liệu mặc định cho lần đầu chạy game
    default_data = {
        "highscores": [0] * 6,  # [0, 0, 0, 0, 0, 0] - deprecated
        "stars": [0] * 6,       # [0, 0, 0, 0, 0, 0]
        "scores": {}            # {} - format mới
    }
    
    # TRƯỜNG HỢP 1: File chưa tồn tại (lần đầu chạy)
    if not os.path.exists(SAVE_FILE):
        return default_data
    
    # TRƯỜNG HỢP 2: File tồn tại, cố gắng đọc
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)  # Parse JSON thành Python dict
        
        # Đảm bảo backward compatibility (file cũ có thể thiếu data)
        # Nếu mảng highscores < 6 phần tử, thêm các số 0 vào cuối
        if len(data.get('highscores', [])) < 6:
            current = data.get('highscores', [])
            missing = 6 - len(current)
            data['highscores'] = current + [0] * missing
        
        # Tương tự cho stars
        if len(data.get('stars', [])) < 6:
            current = data.get('stars', [])
            missing = 6 - len(current)
            data['stars'] = current + [0] * missing
        
        return data
    
    # TRƯỜNG HỢP 3: File bị lỗi (corrupt, format sai, ...)
    except Exception as e:
        print(f"Lỗi khi đọc file save.json: {e}. Trả về dữ liệu mặc định.")
        return default_data
```

**Giải thích chi tiết**:
1. **default_data**: Dữ liệu mặc định khi file không tồn tại hoặc lỗi
2. **`[0] * 6`**: Tạo list 6 phần tử giá trị 0: `[0, 0, 0, 0, 0, 0]`
3. **Backward compatibility**: Nếu file cũ chỉ có 3 level, thêm 3 số 0 cho level 4-6
4. **Exception handling**: Bắt mọi lỗi (JSONDecodeError, IOError, ...) và trả default
5. **Tại sao cần check < 6?** Khi thêm level mới, file save cũ không có dữ liệu

#### 2.6.3. Save dữ liệu với pretty print

```python
def save_game_data(data):
    """Lưu dữ liệu điểm cao và sao."""
    try:
        with open(SAVE_FILE, 'w') as f:
            # indent=4: Format JSON dễ đọc với thụt lề 4 spaces
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Lỗi khi ghi file save.json: {e}")
        # Không raise exception để game không crash
```

**Giải thích**:
- **`json.dump(data, f, indent=4)`**: Ghi dict Python thành JSON file với format đẹp
- **indent=4**: Mỗi cấp thụt 4 spaces, dễ đọc khi mở file save.json
- **Exception không raise**: Nếu save thất bại, chỉ in lỗi, không crash game
- **Mode 'w'**: Ghi đè toàn bộ file (không append)

#### 2.6.4. Cấu trúc file `save.json`

```json
{
    "stars": [3, 2, 1, 0, 0, 0],
    "scores": {
        "LEVEL_1": {"high_score": 190},
        "LEVEL_2": {"high_score": 180},
        "LEVEL_3": {"high_score": 120}
    },
    "highscores": [190, 180, 120, 0, 0, 0]
}
```

**Giải thích cấu trúc**:

| Field | Type | Mô tả | Ví dụ |
|-------|------|-------|-------|
| `stars` | Array[int] | Số sao (0-3) của 6 level | `[3, 2, 1, 0, 0, 0]` |
| `scores` | Dict | Điểm cao của từng level (format mới) | `{"LEVEL_1": {"high_score": 190}}` |
| `highscores` | Array[int] | Điểm cao (format cũ, deprecated) | `[190, 180, 120, 0, 0, 0]` |

**Tại sao có 2 format (scores vs highscores)?**
- `highscores`: Format cũ, mảng đơn giản, dễ truy cập bằng index
- `scores`: Format mới, dictionary, dễ mở rộng (có thể thêm best_time, attempts, ...)
- Giữ cả 2 để backward compatibility với code cũ

**Ví dụ truy cập dữ liệu**:
```python
# Cách cũ (dùng index)
data = load_game_data()
level_1_high_score = data['highscores'][0]  # 190

# Cách mới (dùng key)
level_1_data = data['scores'].get('LEVEL_1', {'high_score': 0})
level_1_high_score = level_1_data['high_score']  # 190
```

---
### 2.7. Module Home Screen (`src/screens/home_screen.py`)

**Vai trò**: Màn hình chào mừng - 54 dòng code, điểm khởi đầu của game

#### 2.7.1. Khởi tạo màn hình

```python
class HomeScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        # KHAI BÁO CÁC RECT TẠM THỜI 
        self.start_button_rect = pygame.Rect(0, 0, 1, 1)
        self.assets = self._load_assets()
        
        # CĂN CHỈNH VỊ TRÍ NÚT PLAY CUỐI CÙNG
        self.start_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180)
```

**Giải thích**:
- `start_button_rect`: Rect tạm thời (0, 0, 1, 1), được resize sau khi load ảnh
- Vị trí nút: Căn giữa màn hình, d dịch xuống 180px

#### 2.7.2. Load assets với fallback

```python
def _load_assets(self):
    assets = {}
    try:
        assets['nen_home'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'giaodiendautien.png')).convert_alpha()
        assets['nen_home'] = pygame.transform.scale(assets['nen_home'], (SCREEN_WIDTH, SCREEN_HEIGHT))     
        assets['nutbatdau'] = pygame.image.load(os.path.join(ASSETS_IMG_DIR, 'nutbatdau.png')).convert_alpha()
        assets['nutbatdau'] = pygame.transform.scale(assets['nutbatdau'], (250, 50)) 
        self.start_button_rect.size = assets['nutbatdau'].get_size() 
        
    except pygame.error as e:
        print(f"Lỗi tải hình ảnh Home: {e}. Vui lòng kiểm tra file ảnh.")
        # Fallback: Tạo surface màu đơn giản
        assets['nen_home'] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        assets['nen_home'].fill(COLOR_BG)
        assets['nutbatdau'] = pygame.Surface((250, 50))
        assets['nutbatdau'].fill(COLOR_CORRECT)
        
    return assets
```

**Điểm nổi bật**:
- Automatic fallback: Nếu load file ảnh lỗi, tạo surface màu đơn giản
- Scale tự động: Nền fit toàn màn hình (1200×600)
- Nút resize: 250×50 pixels

#### 2.7.3. Xử lý click với fade transition

```python
def handle_input(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        
        if self.start_button_rect.collidepoint(mouse_pos):
            # Phát âm click
            self.game_manager.sounds['click'].play()
            
            # Fade transition sang Level Select
            self.game_manager.effect_manager.fade_transition(
                callback=lambda: self.game_manager.switch_screen("LEVEL"),
                fade_out_duration=0.2,
                fade_in_duration=0.2
            )
```

**Giải thích**:
- Kiểm tra collision: `collidepoint(mouse_pos)`
- Effect Manager: Gọi `fade_transition()` với callback
- Callback: `lambda: self.game_manager.switch_screen("LEVEL")` - chuyển màn
- Duration: 0.2s fade out + 0.2s fade in = 0.4s total

---

### 2.8. Module Effect Manager (`src/effects/effect_manager.py`)

**Vai trò**: Quản lý hiệu ứng chuyển cảnh - 439 dòng code, Singleton pattern

#### 2.8.1. Khởi tạo Effect Manager (Singleton)

```python
class EffectManager:
    """Singleton Effect Manager - Quản lý tất cả transitions và effects."""
    _instance = None
    
    def __init__(self, screen_size=(1200, 600)):
        self.screen_size = screen_size
        self.screen_width, self.screen_height = screen_size
        
        # Transition hiện tại
        self.current_transition = None
        self.transition_callback = None
        
        # Danh sách pending callbacks
        self.pending_callbacks = []
```

**Giải thích Singleton**:
- `_instance`: Class variable lưu instance duy nhất
- `get_instance()`: Tạo hoặc trả về instance duy nhất
- Tại sao Singleton? Chỉ 1 effect manager cho toàn bộ game

#### 2.8.2. Fade Transition - Chuyển cảnh mượt mà

```python
def fade_transition(self, 
                   callback: Optional[Callable] = None,
                   fade_out_duration: Optional[float] = None,
                   fade_in_duration: Optional[float] = None,
                   color: Tuple[int, int, int] = (0, 0, 0)):
    """
    Full fade transition: fade out -> callback -> fade in.
    
    Tự động xử lý fade out, gọi callback (chuyển màn), rồi fade in.
    """
    
    fade_out_dur = fade_out_duration if fade_out_duration is not None else 0.3
    fade_in_dur = fade_in_duration if fade_in_duration is not None else 0.3
    
    # Tạo fade transition
    self.current_transition = FadeTransition(
        screen_size=self.screen_size,
        fade_in=False,  # Bắt đầu với fade out
        duration=fade_out_dur,
        color=color
    )
    
    # Lưu callback để gọi sau fade out
    if callback:
        self.pending_callbacks.append({
            'callback': callback,
            'fade_in_duration': fade_in_dur,
            'color': color  
        })
```

**Điểm quan trọng**:
- 3 giai đoạn: Fade out (tối dần) → Callback (chuyển màn) → Fade in (sáng dần)
- `pending_callbacks`: Queue chứa callback chờ thực thi
- Default duration: 0.3s mỗi phase

#### 2.8.3. Slide Transition - Trượt màn hình

```python
def slide_screen(self, direction: str = "left", 
                callback: Optional[Callable] = None,
                duration: Optional[float] = None):
    """
    Slide transition - màn hình mới trượt vào.
    
    Args:
        direction (str): "left", "right", "up", "down"
        callback (Callable): Hàm gọi ngay khi bắt đầu slide (để switch screen)
        duration (float): Thời gian slide (mặc định 0.5)
    """
    
    duration = duration if duration is not None else 0.5
    
    # Gọi callback NGAY (để switch screen trước khi slide)
    if callback:
        callback()
    
    # Tạo slide transition
    self.current_transition = SlideTransition(
        screen_size=self.screen_size,
        direction=direction,
        duration=duration
    )
```

**Giải thích**:
- Callback được gọi TRƯỚC khi slide (khác với fade)
- Direction: 4 hướng (left/right/up/down)
- Màn hình mới "trượt" vào từ hướng chỉ định

#### 2.8.4. Update và Draw loop

```python
def update(self, dt: float):
    """
    Update transition hiện tại.
    
    Args:
        dt (float): Delta time (giây)
    """
    if self.current_transition:
        self.current_transition.update(dt)
        
        # Nếu transition kết thúc
        if self.current_transition.is_done():
            # Xử lý pending callbacks (cho fade transition)
            if self.pending_callbacks:
                cb_data = self.pending_callbacks.pop(0)
                cb_data['callback']()  # Gọi callback (switch screen)
                
                # Bắt đầu fade in
                self.current_transition = FadeTransition(
                    screen_size=self.screen_size,
                    fade_in=True,
                    duration=cb_data['fade_in_duration'],
                    color=cb_data['color']
                )
            else:
                self.current_transition = None

def draw(self, surface: pygame.Surface):
    """Vẽ transition lên màn hình."""
    if self.current_transition:
        self.current_transition.draw(surface)
```

**Workflow fade transition**:
1. **Frame 0**: Bắt đầu fade out
2. **Frame N**: Fade out xong → Gọi callback (switch screen) → Bắt đầu fade in
3. **Frame M**: Fade in xong → Clear transition

---

### 2.9. Module Load Sounds (`src/core/load_sounds.py`)

**Vai trò**: Load âm thanh vào bộ nhớ - 17 dòng code, khởi tạo audio system

#### 2.9.1. Khởi tạo Pygame Mixer

```python
import pygame
import os
from src.config import *

pygame.mixer.init()
# Nhạc nền
pygame.mixer.music.load(os.path.join(ASSETS_SOUND_DIR, "nhacnen.mp3"))
```

**Giải thích**:
- `pygame.mixer.init()`: Khởi tạo audio system
- `pygame.mixer.music`: Kênh riêng cho nhạc nền (chỉ 1 track duy nhất)
- Load nhạc nền: `nhacnen.mp3` (không phát ngay, phát ở GameManager)

#### 2.9.2. Load Sound Effects

```python
def _load_sound():
    sounds = {}
    sounds['click'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, "click_dapan.wav"))
    sounds['no'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, "no.mp3"))
    sounds['yes'] = pygame.mixer.Sound(os.path.join(ASSETS_SOUND_DIR, "yes.mp3"))
    
    return sounds
```

**Giải thích**:
- `pygame.mixer.Sound`: Kênh cho sound effects (phát đồng thời được nhiều sound)
- 3 sound effects:
  - `click`: Âm click nút (WAV format - latency thấp)
  - `yes`: Âm xác nhận đúng
  - `no`: Âm xác nhận sai
- Trả về dictionary để truy cập: `sounds['click'].play()`

#### 2.9.3. Sử dụng trong GameManager

```python
class GameManager:
    sounds = _load_sound()  # Load sounds ở class level
    
    def __init__(self):
        # ...
        pygame.mixer.music.play(loops=-1)  # Phát nhạc nền lặp vô hạn
```

**Điểm nổi bật**:
- Load ở class level: Chỉ load 1 lần cho toàn bộ game
- `loops=-1`: Phát nhạc nền lặp vô hạn
- Các screen khác truy cập: `self.game_manager.sounds['click'].play()`

---

## 3. LUỒNG HOẠT ĐỘNG CHI TIẾT

Dưới đây là luồng hoạt động từ khi khởi động đến khi kết thúc game, chia thành 6 giai đoạn:

### 3.1. Khởi Động **Game** (Startup)

1. User chạy `python main.py`
2. `GameManager.__init__()`: Load save data, khởi tạo screens, phát nhạc nền
3. Hiển thị `Home Screen`

### 3.2. Chọn Level (Level Selection)

4. User click "Bắt đầu" → Chuyển sang `LevelSelectScreen`
5. Vẽ 6 level, kiểm tra khóa:  `is_locked = (i > 0 and stars_data[i-1] == 0)`
6. User click Level 3 → Set `current_level_key = "LEVEL_3"`

### 3.3. Tạo Câu Hỏi (Question Generation)

7. `switch_screen("GAMEPLAY")` gọi `get_level_3_questions(20)`
8. Nhận 20 câu hỏi → Lưu vào `questions_pool`
9. `on_enter()` → `reset_game()` → `load_next_question()`

### 3.4. Vòng Lặp Chơi (Game Loop - 20 câu)

Mỗi frame (~120 FPS):
- **update()**: Đếm timer, kiểm tra hết giờ, tự động chuyển câu sau 1.5s
- **draw()**: Vẽ câu hỏi (dynamic resize), vẽ 4 đáp án, vẽ timer
- **handle_input()**: Khi user click → `process_answer()` → +10 hoặc -5 điểm

### 3.5. Kết Thúc (Game Over)

10. Hết 20 câu → `game_over = True`
11. `calculate_stars()`: Tính 0-3 sao dựa trên % điểm
12. `save_score()`: Kiểm tra perfect/new_best, lưu vào `save.json`
13. Vẽ màn hình kết quả: điểm, sao, 2 nút (Next/Replay)

### 3.6. Menu Settings (Có thể mở bất kỳ lúc nào)

- Click Settings → `show_settings = True` → Vẽ popup overlay
- Toggle Sound/BGM → `update()` điều khiển `set_volume()` / `pause()`/`unpause()`
- Click Home/Replay/X → Thực hiện hành động tương ứng

---

## 4. ĐIỂM NỔI BẬT VÀ KỸ THUẬT ĐẶC BIỆT

### 4.1. Dynamic UI Resizing - Tự giãn kích thước theo nội dung

- Khung câu hỏi và nút đáp án tự giãn theo nội dung  
- Parser toán học tính toán kích thước từng phần tử  
- Hỗ trợ phân số cao, biểu thức dài

### 4.2. Non-blocking Feedback - Phản hồi không bị chặn

- Dùng `show_feedback_until` thay vì `pygame.time.delay()`  
- Game vẫn chạy mượt, timer vẫn đếm được

### 4.3. Realtime Timer - Bộ đếm thời gian thực

- Dùng `time.time()` thay vì đếm frame  
- Chính xác, không bị ảnh hưởng bởi FPS

### 4.4. Conditional Shuffling - Trộn câu hỏi có điều kiện

- Level 5 (phân số) giữ nguyên thứ tự đáp án bằng `answer_index`  
- Các level khác shuffle ngẫu nhiên

### 4.5. Level Unlocking System - Hệ thống mở khóa theo cấp độ

- Level chỉ mở khi level trước đạt >= 1 sao  
- Tạo cảm giác tiến triển

### 4.6. Perfect vs New Best - Điểm hoàn hảo và điểm cao nhất

- `is_perfect`: 200/200 điểm  
- `is_new_best`: Phá kỷ lục (nhưng không perfect)  
- Hiển thị ảnh khác nhau

### 4.7. Progress Bar - Thanh tiến trình

- Thanh tiến độ với 3 mốc sao (50%, 75%, 95%)  
- Sao sáng/tối theo tiến trình

### 4.8. Menu dạng Popup
- MenuScreen là overlay, không phải screen riêng  
- Tiết kiệm bộ nhớ, UX tốt hơn

---

## 5. KẾT LUẬN

**Smart Math** là một ứng dụng game học toán được thiết kế và xây dựng hoàn chỉnh với:

1. **Kiến trúc rõ ràng**: Module chính phân tách hợp lý  
2. **Code chất lượng**: 668 dòng trong GameplayScreen xử lý UI phức tạp  
3. **UX xuất sắc**: Dynamic resizing, non-blocking feedback, realtime timer  
4. **Logic game chặt chẽ**: Unlocking system, perfect/new best, conditional shuffling

**Thống kê dự án**:
- Tổng số file Python: 21 files
- Module lớn nhất: `gameplay_screen.py` (668 dòng)
- Module phức tạp nhất: `gameplay_screen.py` (parsing, rendering, timing)
- Tổng số assets: 42 files (38 ảnh + 4 âm thanh)

**Hướng phát triển**:
- Multiplayer mode
- Bảng xếp hạng trực tuyến
- Thêm level 7-10 (logarit, hình học, ...)
- Animation hiệu ứng đẹp hơn

---

**Nhóm phát triển**: Nhóm 15
**Ngày hoàn thành**: 3/1/2026  
**Công nghệ**: Python 3.x + Pygame 2.x
