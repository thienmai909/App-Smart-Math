"""
Progress Effects - Hiệu ứng cho thanh tiến độ và sao
===================================================
Cung cấp hiệu ứng mượt mà cho progress bar và star milestone.
"""

import pygame
import math
import random

# Try relative import first (when used as module), fallback to direct import
try:
    from .base_effect import BaseEffect
    from .animation_utils import lerp, ease_out_bounce, ease_out_elastic, ease_in_out, ease_out_quad
except ImportError:
    from base_effect import BaseEffect
    from animation_utils import lerp, ease_out_bounce, ease_out_elastic, ease_in_out, ease_out_quad


class ProgressBarFillEffect:
    """
    Animated fill cho progress bar.
    
    Thay vì nhảy cóc, progress bar sẽ điền từ từ với animation mượt.
    
    Usage:
        progress_fx = ProgressBarFillEffect(duration=0.4)
        
        # Khi điểm thay đổi:
        new_progress = score / max_score
        progress_fx.set_target(new_progress)
        
        # Mỗi frame:
        progress_fx.update(dt)
        current_progress = progress_fx.get_current_progress()
        # Vẽ progress bar với current_progress
    """
    
    def __init__(self, duration=0.4, easing_func=None):
        """
        Args:
            duration (float): Thời gian animation (giây)
            easing_func (callable): Hàm easing (mặc định: ease_in_out)
        """
        self.duration = duration
        self.easing_func = easing_func or ease_in_out
        
        self.current_progress = 0.0
        self.target_progress = 0.0
        self.start_progress = 0.0
        
        self.elapsed_time = 0.0
        self.is_animating = False
    
    def set_target(self, new_progress):
        """
        Set progress mục tiêu và bắt đầu animation.
        
        Args:
            new_progress (float): Progress mục tiêu (0.0 - 1.0)
        """
        new_progress = max(0.0, min(1.0, new_progress))
        
        if abs(new_progress - self.target_progress) < 0.001:
            return
        
        self.start_progress = self.current_progress
        self.target_progress = new_progress
        self.elapsed_time = 0.0
        self.is_animating = True
    
    def update(self, dt):
        """
        Cập nhật animation.
        
        Args:
            dt (float): Delta time
        """
        if not self.is_animating:
            return
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.duration:
            self.current_progress = self.target_progress
            self.is_animating = False
            return
        
        # Tính progress
        t = min(1.0, self.elapsed_time / self.duration)
        eased_t = self.easing_func(t)
        
        # Lerp từ start -> target
        self.current_progress = lerp(self.start_progress, self.target_progress, eased_t)
    
    def get_current_progress(self):
        """
        Trả về progress hiện tại.
        
        Returns:
            float: Progress từ 0.0 đến 1.0
        """
        return self.current_progress
    
    def is_at_target(self):
        """
        Kiểm tra đã đến target chưa.
        
        Returns:
            bool: True nếu đã đến target
        """
        return not self.is_animating and abs(self.current_progress - self.target_progress) < 0.001
    
    def reset(self):
        """Reset về 0."""
        self.current_progress = 0.0
        self.target_progress = 0.0
        self.start_progress = 0.0
        self.is_animating = False


class StarPopEffect(BaseEffect):
    """
    Hiệu ứng sao bật ra khi đạt milestone.
    
    - Scale từ 0 -> 1.2 -> 1.0 (bounce)
    - Rotate nhẹ
    - Particle vàng bay ra xung quanh
    
    Usage:
        star_pop = StarPopEffect(star_pos=(600, 100))
        star_pop.start()
        
        # Mỗi frame:
        star_pop.update(dt)
        scale, rotation = star_pop.get_transform()
        # Vẽ sao với scale và rotation
        star_pop.draw(surface)  # Vẽ particles
    """
    
    def __init__(self, star_pos, duration=0.8):
        """
        Args:
            star_pos (tuple): Vị trí sao (x, y)
            duration (float): Thời gian hiệu ứng (giây)
        """
        super().__init__(duration)
        self.star_pos = star_pos
        
        self.scale = 0.0
        self.rotation = 0.0
        
        # Particles
        self.particles = []
        self.particle_count = 12
    
    def on_start(self):
        """Tạo particles khi bắt đầu."""
        self.particles = []
        
        # Tạo particles bay ra theo hình tròn
        for i in range(self.particle_count):
            angle = (i / self.particle_count) * 2 * math.pi
            speed = random.uniform(80, 150)
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.particles.append({
                'x': self.star_pos[0],
                'y': self.star_pos[1],
                'vx': vx,
                'vy': vy,
                'life': 1.0,  # 0.0 - 1.0
                'size': random.randint(3, 6),
                'color': random.choice([
                    (255, 215, 0),   # Vàng
                    (255, 255, 100), # Vàng nhạt
                    (255, 200, 50),  # Vàng đậm
                ])
            })
    
    def on_update(self, dt):
        """Cập nhật scale, rotation và particles."""
        progress = self.get_progress()
        
        # Scale với bounce
        if progress < 0.5:
            # 0 -> 1.2 (phóng to)
            t = progress * 2.0
            self.scale = lerp(0.0, 1.2, ease_out_elastic(t))
        else:
            # 1.2 -> 1.0 (thu nhỏ về bình thường)
            t = (progress - 0.5) * 2.0
            self.scale = lerp(1.2, 1.0, ease_in_out(t))
        
        # Rotation (xoay nhẹ)
        self.rotation = math.sin(progress * math.pi * 2) * 15  # +/- 15 độ
        
        # Update particles
        for p in self.particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            
            # Gravity
            p['vy'] += 200 * dt
            
            # Giảm life
            p['life'] -= dt / self.duration
            if p['life'] < 0:
                p['life'] = 0
    
    def on_draw(self, surface):
        """Vẽ particles."""
        for p in self.particles:
            if p['life'] <= 0:
                continue
            
            # Alpha giảm dần khi life giảm
            alpha = int(255 * p['life'])
            size = int(p['size'] * p['life'])
            
            if size <= 0:
                continue
            
            # Vẽ particle (circle)
            color_with_alpha = (*p['color'], alpha)
            
            # Tạo surface tạm với alpha
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                particle_surface,
                color_with_alpha,
                (size, size),
                size
            )
            
            surface.blit(particle_surface, (int(p['x']) - size, int(p['y']) - size))
    
    def get_transform(self):
        """
        Trả về scale và rotation của sao.
        
        Returns:
            tuple: (scale, rotation_degrees)
        """
        return (self.scale, self.rotation)
    
    def apply_to_surface(self, surface):
        """
        Apply transform lên surface sao.
        
        Args:
            surface (pygame.Surface): Surface sao gốc
        
        Returns:
            pygame.Surface: Surface đã transform
        """
        if abs(self.scale) < 0.001:
            # Scale = 0, không vẽ
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # Scale
        new_width = int(surface.get_width() * self.scale)
        new_height = int(surface.get_height() * self.scale)
        
        if new_width <= 0 or new_height <= 0:
            return pygame.Surface((1, 1), pygame.SRCALPHA)
        
        scaled_surface = pygame.transform.smoothscale(surface, (new_width, new_height))
        
        # Rotate
        if abs(self.rotation) > 0.1:
            scaled_surface = pygame.transform.rotate(scaled_surface, self.rotation)
        
        return scaled_surface


class ProgressPulseEffect:
    """
    Pulse effect cho phần fill của progress bar.
    
    Tạo hiệu ứng "chảy" (flowing) bằng cách vẽ gradient di chuyển.
    
    Usage:
        pulse = ProgressPulseEffect()
        
        # Mỗi frame:
        pulse.update(dt)
        offset = pulse.get_offset()
        # Vẽ progress bar với pattern offset
    """
    
    def __init__(self, speed=100, enabled=True):
        """
        Args:
            speed (float): Tốc độ pulse (pixels/giây)
            enabled (bool): Bật hiệu ứng?
        """
        self.speed = speed
        self.enabled = enabled
        self.offset = 0.0
    
    def update(self, dt):
        """
        Cập nhật offset.
        
        Args:
            dt (float): Delta time
        """
        if not self.enabled:
            return
        
        self.offset += self.speed * dt
        
        # Wrap around để không tràn số
        if self.offset > 1000:
            self.offset = 0.0
    
    def get_offset(self):
        """
        Trả về offset hiện tại.
        
        Returns:
            float: Offset (pixels)
        """
        return self.offset
    
    def create_pattern_surface(self, width, height, base_color, pattern_type="diagonal"):
        """
        Tạo surface pattern cho progress bar.
        
        Args:
            width (int): Chiều rộng
            height (int): Chiều cao
            base_color (tuple): Màu nền (R, G, B)
            pattern_type (str): Loại pattern - "diagonal", "dots"
        
        Returns:
            pygame.Surface: Surface pattern
        """
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(base_color)
        
        if pattern_type == "diagonal":
            # Vẽ các sọc chéo
            stripe_width = 20
            stripe_spacing = 40
            
            offset_int = int(self.offset) % stripe_spacing
            
            overlay_color = (
                min(255, base_color[0] + 30),
                min(255, base_color[1] + 30),
                min(255, base_color[2] + 30),
                100
            )
            
            for x in range(-stripe_spacing + offset_int, width + stripe_spacing, stripe_spacing):
                points = [
                    (x, 0),
                    (x + stripe_width, 0),
                    (x + stripe_width - height, height),
                    (x - height, height)
                ]
                pygame.draw.polygon(surface, overlay_color, points)
        
        elif pattern_type == "dots":
            # Vẽ các chấm
            dot_spacing = 15
            offset_int = int(self.offset) % dot_spacing
            
            overlay_color = (
                min(255, base_color[0] + 40),
                min(255, base_color[1] + 40),
                min(255, base_color[2] + 40),
                150
            )
            
            for x in range(offset_int, width, dot_spacing):
                for y in range(0, height, dot_spacing):
                    if (x // dot_spacing + y // dot_spacing) % 2 == 0:
                        pygame.draw.circle(surface, overlay_color, (x, y), 3)
        
        return surface
    
    def toggle(self):
        """Bật/tắt hiệu ứng."""
        self.enabled = not self.enabled


class ScoreCountUpEffect:
    """
    Count-up effect cho điểm số.
    
    Thay vì hiện số ngay, số sẽ đếm từ từ từ giá trị cũ lên giá trị mới.
    
    Usage:
        count_up = ScoreCountUpEffect()
        
        # Khi điểm thay đổi:
        count_up.set_target(new_score)
        
        # Mỗi frame:
        count_up.update(dt)
        displayed_score = count_up.get_current_value()
        # Vẽ displayed_score
    """
    
    def __init__(self, duration=0.5):
        """
        Args:
            duration (float): Thời gian đếm (giây)
        """
        self.duration = duration
        
        self.current_value = 0
        self.target_value = 0
        self.start_value = 0
        
        self.elapsed_time = 0.0
        self.is_counting = False
    
    def set_target(self, new_value):
        """
        Set giá trị mục tiêu và bắt đầu đếm.
        
        Args:
            new_value (int): Giá trị mục tiêu
        """
        if new_value == self.target_value:
            return
        
        self.start_value = self.current_value
        self.target_value = new_value
        self.elapsed_time = 0.0
        self.is_counting = True
    
    def update(self, dt):
        """
        Cập nhật đếm.
        
        Args:
            dt (float): Delta time
        """
        if not self.is_counting:
            return
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.duration:
            self.current_value = self.target_value
            self.is_counting = False
            return
        
        # Tính progress
        t = min(1.0, self.elapsed_time / self.duration)
        eased_t = ease_out_quad(t)
        
        # Lerp
        self.current_value = int(lerp(self.start_value, self.target_value, eased_t))
    
    def get_current_value(self):
        """
        Trả về giá trị hiện tại (đang đếm).
        
        Returns:
            int: Giá trị hiện tại
        """
        return self.current_value
    
    def skip_to_target(self):
        """Nhảy ngay đến target (bỏ qua animation)."""
        self.current_value = self.target_value
        self.is_counting = False
    
    def reset(self):
        """Reset về 0."""
        self.current_value = 0
        self.target_value = 0
        self.is_counting = False
