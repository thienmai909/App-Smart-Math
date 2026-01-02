# Smart Math - Effects Module

Hệ thống hiệu ứng modular cho game học toán Smart Math.

## 📁 Cấu Trúc Module

```
src/effects/
├── __init__.py              # Export tất cả effects
├── base_effect.py          # Base class cho effects
├── animation_utils.py      # Easing functions & interpolation
├── transitions.py          # Fade, Slide, Zoom transitions
├── button_effects.py       # Hover, Click, Glow, Press effects
├── progress_effects.py     # Progress bar, Star pop, Count up
└── demo_effects.py         # Demo tất cả hiệu ứng
```

## 🚀 Cách Sử Dụng

### 1. Import Effects

```python
from src.effects import (
    FadeTransition,
    HoverEffect,
    ProgressBarFillEffect,
    StarPopEffect
)
```

### 2. Transitions - Chuyển màn hình

```python
# Fade Out khi chuyển màn
fade_out = FadeTransition(fade_in=False, duration=0.3)
fade_out.start()

# Trong update loop:
fade_out.update(dt)

# Trong draw loop:
fade_out.draw(surface)
```

### 3. Button Hover Effect

```python
# Khởi tạo
hover_fx = HoverEffect(scale_factor=1.1, duration=0.15)

# Mỗi frame:
is_hovering = button_rect.collidepoint(mouse_pos)
hover_fx.update(is_hovering, dt)

# Khi vẽ:
scaled_rect = hover_fx.get_scaled_rect(button_rect)
scaled_image = hover_fx.scale_surface(button_image)
surface.blit(scaled_image, scaled_rect)
```

### 4. Progress Bar Animation

```python
# Khởi tạo
progress_fx = ProgressBarFillEffect(duration=0.4)

# Khi điểm thay đổi:
new_progress = score / max_score
progress_fx.set_target(new_progress)

# Mỗi frame:
progress_fx.update(dt)
current_progress = progress_fx.get_current_progress()

# Vẽ progress bar với current_progress
fill_width = int(bar_width * current_progress)
```

### 5. Star Pop Effect

```python
# Khởi tạo
star_pop = StarPopEffect(star_pos=(600, 100), duration=0.8)
star_pop.start()

# Mỗi frame:
star_pop.update(dt)
scale, rotation = star_pop.get_transform()

# Vẽ sao:
star_surface = star_pop.apply_to_surface(star_image)
surface.blit(star_surface, star_pos)

# Vẽ particles:
star_pop.draw(surface)
```

## 🎨 Các Hiệu Ứng Đã Implement

### Transitions (transitions.py)
- ✅ **FadeTransition** - Fade in/out màn hình
- ✅ **SlideTransition** - Trượt màn hình (left/right/up/down)
- ✅ **ZoomTransition** - Zoom in/out màn hình

### Button Effects (button_effects.py)
- ✅ **HoverEffect** - Scale lên khi hover
- ✅ **ClickRippleEffect** - Sóng lan tỏa khi click
- ✅ **GlowEffect** - Viền sáng xung quanh button (có pulsing)
- ✅ **PressEffect** - Nhấn xuống với bounce

### Progress Effects (progress_effects.py)
- ✅ **ProgressBarFillEffect** - Animated fill cho progress bar
- ✅ **StarPopEffect** - Sao bật ra với bounce + particles
- ✅ **ProgressPulseEffect** - Pattern chảy trong progress bar
- ✅ **ScoreCountUpEffect** - Đếm số từ 0 lên target

### Animation Utils (animation_utils.py)
- ✅ **Easing Functions**: linear, ease_in_out, ease_out_bounce, ease_out_elastic, etc.
- ✅ **Interpolation**: lerp, color_lerp, smooth_damp
- ✅ **Utilities**: clamp

## 🎮 Chạy Demo

```bash
cd src/effects
python demo_effects.py
```

**Điều khiển Demo:**
- Phím **1-6**: Chuyển giữa các demo
- **Space**: Trigger hiệu ứng
- **ESC**: Thoát

## 📝 Tích Hợp Vào Game

### Ví dụ: Thêm Hover Effect vào Level Select

```python
# Trong level_select_screen.py

from src.effects import HoverEffect

class LevelSelectScreen:
    def __init__(self, game_manager):
        # ... code cũ
        
        # Thêm hover effects
        self.level_hover_effects = [
            HoverEffect(scale_factor=1.08, duration=0.15) 
            for _ in range(6)
        ]
    
    def update(self):
        dt = 1.0 / 120  # Hoặc tính từ clock
        mouse_pos = pygame.mouse.get_pos()
        
        # Update hover effects
        for i, hover_fx in enumerate(self.level_hover_effects):
            is_hovering = self.level_rects[i]['rect'].collidepoint(mouse_pos)
            hover_fx.update(is_hovering, dt)
    
    def draw(self, surface):
        # ... vẽ background
        
        for i, level in enumerate(LEVELS):
            # Lấy scaled rect
            hover_fx = self.level_hover_effects[i]
            scaled_rect = hover_fx.get_scaled_rect(self.level_rects[i]['rect'])
            
            # Scale image
            level_image = self.assets[level['image_key']]
            scaled_image = hover_fx.scale_surface(level_image)
            
            # Vẽ
            surface.blit(scaled_image, scaled_rect)
```

### Ví dụ: Thêm Progress Animation vào Gameplay

```python
# Trong gameplay_screen.py

from src.effects import ProgressBarFillEffect, StarPopEffect

class GameplayScreen:
    def __init__(self, game_manager):
        # ... code cũ
        
        # Thêm hiệu ứng
        self.progress_fill_fx = ProgressBarFillEffect(duration=0.3)
        self.star_pop_fx = None
    
    def process_answer(self, selected_index):
        # ... tính điểm
        
        # Update progress bar với animation
        max_score = len(self.game_manager.questions_pool) * POINTS_CORRECT
        new_progress = self.score / max_score
        self.progress_fill_fx.set_target(new_progress)
        
        # Check star milestone
        if self.check_new_star_achieved():
            self.star_pop_fx = StarPopEffect(star_position, duration=0.8)
            self.star_pop_fx.start()
    
    def update(self):
        dt = 1.0 / FPS
        
        # Update progress animation
        self.progress_fill_fx.update(dt)
        
        # Update star pop
        if self.star_pop_fx and self.star_pop_fx.is_active:
            self.star_pop_fx.update(dt)
    
    def draw(self, surface):
        # Vẽ progress bar
        current_progress = self.progress_fill_fx.get_current_progress()
        fill_width = int(bar_width * current_progress)
        # ... vẽ với fill_width
        
        # Vẽ star pop particles
        if self.star_pop_fx:
            self.star_pop_fx.draw(surface)
```

## 🎯 Best Practices

1. **Delta Time**: Luôn dùng `dt` (delta time) thay vì frame-based animation
2. **Reset**: Gọi `.reset()` khi cần khởi động lại hiệu ứng
3. **Check is_active**: Kiểm tra trước khi update/draw để tiết kiệm performance
4. **Factory Functions**: Dùng `create_fade_transition()` để tạo nhanh với config mặc định

## 📚 API Reference

### BaseEffect

Lớp cơ sở cho tất cả hiệu ứng.

**Methods:**
- `start()` - Bắt đầu hiệu ứng
- `update(dt)` - Cập nhật mỗi frame
- `draw(surface)` - Vẽ hiệu ứng
- `get_progress()` - Trả về 0.0-1.0
- `reset()` - Reset về trạng thái ban đầu
- `stop()` - Dừng ngay lập tức

**Properties:**
- `is_active` - Đang chạy?
- `is_finished` - Đã hoàn thành?
- `duration` - Thời gian (giây)

## 🔧 Configuration

Các hiệu ứng có thể điều chỉnh nhiều thông số:

```python
# Hover với scale nhỏ hơn
hover = HoverEffect(scale_factor=1.05, duration=0.1)

# Glow không pulsing
glow = GlowEffect(color=(0, 150, 255), pulsing=False, intensity=0.8)

# Progress bar chậm hơn
progress = ProgressBarFillEffect(duration=1.0)
```

## 🐛 Troubleshooting

**Q: Hiệu ứng không chạy?**
- Kiểm tra đã gọi `.start()` chưa
- Kiểm tra đang gọi `.update(dt)` mỗi frame chưa

**Q: Animation giật lag?**
- Đảm bảo `dt` được tính đúng (giây, không phải milliseconds)
- Check FPS có đủ cao không (>= 60)

**Q: Import error?**
- Đảm bảo đang import từ `src.effects`, không phải `effects`

## 📄 License

Phần của Smart Math project.
