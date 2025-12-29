# Hướng Dẫn Sử Dụng Transitions - Smart Math

## 📚 Tổng Quan

**Transitions** là các hiệu ứng chuyển cảnh giữa các màn hình, giúp game mượt mà và chuyên nghiệp hơn.

Module cung cấp **3 loại transition chính**:
1. **FadeTransition** - Làm mờ/hiện màn hình
2. **SlideTransition** - Trượt màn hình từ một hướng
3. **ZoomTransition** - Phóng to/thu nhỏ màn hình

---

## 🎯 1. FadeTransition - Fade In/Out

### Cách Hoạt Động
- **Fade Out**: Màn hình từ trong suốt → đen (che khuất màn cũ)
- **Fade In**: Màn hình từ đen → trong suốt (hiện màn mới)

### Ví Dụ Cơ Bản

```python
from src.effects import FadeTransition

# Tạo fade out (che màn hình cũ)
fade_out = FadeTransition(
    fade_in=False,      # False = fade out, True = fade in
    duration=0.5,       # Thời gian 0.5 giây
    color=(0, 0, 0),    # Màu đen
    screen_size=(1200, 600)
)

# Bắt đầu hiệu ứng
fade_out.start()

# Trong game loop:
# 1. Update
fade_out.update(dt)

# 2. Draw (vẽ CUỐI CÙNG, sau khi vẽ tất cả)
fade_out.draw(surface)
```

### Tích Hợp Vào GameManager

```python
# Trong game_manager.py

from src.effects import FadeTransition

class GameManager:
    def __init__(self):
        # ... code cũ
        self.active_transition = None
    
    def switch_screen(self, screen_key):
        """Chuyển màn hình với fade transition"""
        
        if screen_key not in self.screens:
            return
        
        # BƯỚC 1: Fade out màn hình cũ
        fade_out = FadeTransition(
            fade_in=False, 
            duration=0.3,
            screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        fade_out.start()
        self.active_transition = fade_out
        
        # Lưu màn hình đích để chuyển sau khi fade out xong
        self.pending_screen = screen_key
    
    def update(self):
        # Update transition nếu đang chạy
        if self.active_transition and self.active_transition.is_active:
            dt = 1.0 / FPS
            self.active_transition.update(dt)
            
            # Khi fade out xong, chuyển màn + fade in
            if self.active_transition.is_finished:
                if hasattr(self, 'pending_screen'):
                    # Chuyển màn hình
                    self.active_screen_key = self.pending_screen
                    self.active_screen = self.screens[self.active_screen_key]
                    
                    # Bắt đầu fade in
                    fade_in = FadeTransition(
                        fade_in=True,
                        duration=0.3,
                        screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
                    )
                    fade_in.start()
                    self.active_transition = fade_in
                    
                    del self.pending_screen
                else:
                    # Fade in xong, xóa transition
                    self.active_transition = None
        
        # Update màn hình hiện tại
        self.active_screen.update()
    
    def draw(self, surface):
        # Vẽ màn hình
        self.active_screen.draw(surface)
        
        # Vẽ transition lên trên
        if self.active_transition and self.active_transition.is_active:
            self.active_transition.draw(surface)
```

---

## 🎯 2. SlideTransition - Trượt Màn Hình

### Cách Hoạt Động
Màn hình mới trượt vào từ **4 hướng**: left, right, up, down

### Ví Dụ Cơ Bản

```python
from src.effects import SlideTransition

# Tạo slide từ trái sang phải
slide = SlideTransition(
    direction="left",    # "left", "right", "up", "down"
    duration=0.6,
    screen_size=(1200, 600)
)

slide.start()

# Trong game loop:
# 1. Update
slide.update(dt)

# 2. Lấy offset để vẽ màn hình
offset_x, offset_y = slide.get_offset()

# 3. Vẽ màn hình mới với offset
surface.blit(new_screen_surface, (offset_x, offset_y))
```

### Tích Hợp Đầy Đủ

```python
class GameManager:
    def switch_screen_with_slide(self, screen_key, direction="left"):
        """Chuyển màn hình với slide transition"""
        
        # Tạo slide transition
        slide = SlideTransition(
            direction=direction,
            duration=0.6,
            screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        slide.start()
        
        # Lưu transition và màn hình đích
        self.active_transition = slide
        self.next_screen = screen_key
    
    def draw(self, surface):
        # Vẽ màn hình hiện tại bình thường
        self.active_screen.draw(surface)
        
        # Nếu có slide transition
        if self.active_transition and isinstance(self.active_transition, SlideTransition):
            if self.active_transition.is_active:
                # Tạo surface cho màn hình mới
                new_screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                
                # Vẽ màn hình mới lên surface tạm
                if hasattr(self, 'next_screen'):
                    self.screens[self.next_screen].draw(new_screen_surface)
                
                # Lấy offset và vẽ với offset
                offset_x, offset_y = self.active_transition.get_offset()
                surface.blit(new_screen_surface, (offset_x, offset_y))
            
            # Khi slide xong, chuyển màn hình
            if self.active_transition.is_finished:
                self.active_screen_key = self.next_screen
                self.active_screen = self.screens[self.active_screen_key]
                self.active_transition = None
                del self.next_screen
```

---

## 🎯 3. ZoomTransition - Phóng To/Thu Nhỏ

### Cách Hoạt Động
- **Zoom In**: Màn hình mới từ nhỏ → bình thường
- **Zoom Out**: Màn hình cũ từ bình thường → nhỏ

### Ví Dụ Cơ Bản

```python
from src.effects import ZoomTransition

# Tạo zoom in
zoom = ZoomTransition(
    zoom_in=True,       # True = zoom in, False = zoom out
    duration=0.7,
    min_scale=0.0,      # Scale nhỏ nhất
    max_scale=1.0,      # Scale lớn nhất
    screen_size=(1200, 600)
)

zoom.start()

# Trong game loop:
# 1. Update
zoom.update(dt)

# 2. Lấy thông tin scale
scale = zoom.get_scale()
scaled_width, scaled_height = zoom.get_scaled_size()
offset_x, offset_y = zoom.get_center_offset()

# 3. Scale và vẽ màn hình
scaled_screen = pygame.transform.smoothscale(
    screen_surface, 
    (scaled_width, scaled_height)
)
surface.blit(scaled_screen, (offset_x, offset_y))

# 4. Vẽ overlay tối (nếu có)
zoom.draw(surface)
```

---

## 🚀 4. Ví Dụ Thực Tế - Tích Hợp Vào Home Screen

### Thêm Fade Transition Khi Nhấn "Bắt Đầu"

```python
# Trong home_screen.py

from src.effects import FadeTransition

class HomeScreen(BaseScreen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        # ... code cũ
        
        # Thêm transition
        self.fade_transition = None
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.start_button_rect.collidepoint(mouse_pos):
                self.game_manager.sounds['click'].play()
                
                # Tạo và bắt đầu fade out
                self.fade_transition = FadeTransition(
                    fade_in=False,
                    duration=0.4,
                    screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
                )
                self.fade_transition.start()
    
    def update(self):
        # Update transition
        if self.fade_transition and self.fade_transition.is_active:
            dt = 1.0 / FPS
            self.fade_transition.update(dt)
            
            # Khi fade out xong, chuyển màn
            if self.fade_transition.is_finished:
                self.game_manager.switch_screen("LEVEL")
                self.fade_transition = None
    
    def draw(self, surface):
        if surface is None:
            return
        
        # Vẽ màn hình bình thường
        surface.blit(self.assets['nen_home'], (0, 0))
        surface.blit(self.assets['nutbatdau'], self.start_button_rect.topleft)
        
        # Vẽ transition lên trên
        if self.fade_transition and self.fade_transition.is_active:
            self.fade_transition.draw(surface)
```

---

## 🎨 5. Factory Functions - Tạo Nhanh

Module cung cấp các hàm tiện ích để tạo transitions nhanh với config mặc định:

```python
from src.effects.transitions import (
    create_fade_transition,
    create_slide_transition,
    create_zoom_transition
)

# Tạo fade out nhanh
fade_out = create_fade_transition(fade_in=False, duration=0.3)

# Tạo slide nhanh
slide = create_slide_transition(direction="left", duration=0.6)

# Tạo zoom nhanh
zoom = create_zoom_transition(zoom_in=True, duration=0.7)
```

---

## ⚙️ 6. Tùy Chỉnh

### Thay Đổi Màu Fade

```python
# Fade sang màu trắng thay vì đen
fade = FadeTransition(
    fade_in=False,
    duration=0.5,
    color=(255, 255, 255),  # Trắng
    screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
)
```

### Zoom Với Scale Tùy Chỉnh

```python
# Zoom từ 50% đến 150%
zoom = ZoomTransition(
    zoom_in=True,
    duration=1.0,
    min_scale=0.5,   # Bắt đầu ở 50%
    max_scale=1.5,   # Kết thúc ở 150%
    screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
)
```

---

## 🎯 7. Best Practices

### ✅ DO (Nên)
```python
# 1. Luôn check is_active trước khi update/draw
if transition.is_active:
    transition.update(dt)
    transition.draw(surface)

# 2. Vẽ transition CUỐI CÙNG (overlay lên trên tất cả)
screen.draw(surface)      # Vẽ màn hình
ui.draw(surface)          # Vẽ UI
transition.draw(surface)  # Vẽ transition

# 3. Xóa transition khi xong
if transition.is_finished:
    transition = None
```

### ❌ DON'T (Không nên)
```python
# 1. KHÔNG vẽ transition trước màn hình
transition.draw(surface)  # ❌ Sai
screen.draw(surface)      # Sẽ che mất transition

# 2. KHÔNG quên gọi start()
transition = FadeTransition(...)
transition.update(dt)  # ❌ Sẽ không hoạt động vì chưa start()

# 3. KHÔNG dùng delay() block game
pygame.time.delay(1000)  # ❌ Block toàn bộ game
# Dùng transition.is_finished để check
```

---

## 🐛 8. Troubleshooting

**Q: Transition không hiện?**
```python
# Check 3 điều:
1. Đã gọi .start() chưa?
2. Đang gọi .update(dt) mỗi frame chưa?
3. Đang gọi .draw(surface) CUỐI CÙNG chưa?
```

**Q: Fade không mượt?**
```python
# Đảm bảo dt đúng (giây, không phải milliseconds)
dt = clock.tick(FPS) / 1000.0  # ✅ Chia 1000 để có giây
dt = clock.tick(FPS)           # ❌ Sai, là milliseconds
```

**Q: Slide bị giật?**
```python
# Tăng FPS hoặc giảm duration
FPS = 120              # Tăng FPS
duration=0.4          # Giảm duration xuống
```

---

## 🎮 9. Demo Test

Chạy demo để xem tất cả transitions:

```bash
cd src\effects
python demo_effects.py
```

Nhấn **1** để vào demo transitions, nhấn **Space** để xem các hiệu ứng.

---

## 📝 10. Tóm Tắt API

| Method | Mô tả | Return |
|--------|-------|--------|
| `__init__(...)` | Khởi tạo transition | - |
| `.start()` | Bắt đầu hiệu ứng | - |
| `.update(dt)` | Cập nhật mỗi frame | - |
| `.draw(surface)` | Vẽ transition | - |
| `.get_progress()` | Lấy tiến độ (0.0-1.0) | float |
| `.is_active` | Đang chạy? | bool |
| `.is_finished` | Đã xong? | bool |
| `.reset()` | Reset về ban đầu | - |

### Riêng cho SlideTransition
| Method | Return |
|--------|--------|
| `.get_offset()` | (offset_x, offset_y) |

### Riêng cho ZoomTransition
| Method | Return |
|--------|--------|
| `.get_scale()` | float (0.0-1.0) |
| `.get_scaled_size()` | (width, height) |
| `.get_center_offset()` | (x, y) |

---

**Chúc bạn implement thành công! 🎉**
