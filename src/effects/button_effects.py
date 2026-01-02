"""
Button Effects - Hiệu ứng cho nút bấm
=====================================
Cung cấp các hiệu ứng tương tác cho buttons: hover, click, glow.
"""

import pygame
import math

# Try relative import first (when used as module), fallback to direct import
try:
    from .animation_utils import lerp, ease_out_bounce, ease_out_quad
except ImportError:
    from animation_utils import lerp, ease_out_bounce, ease_out_quad


class HoverEffect:
    """
    Hover effect - Phóng to/thu nhỏ button khi di chuột qua.
    
    Animation mượt mà khi hover/unhover với easing.
    
    Usage:
        hover_fx = HoverEffect(scale_factor=1.1, duration=0.15)
        
        # Mỗi frame:
        is_hovering = button_rect.collidepoint(mouse_pos)
        hover_fx.update(is_hovering, dt)
        
        # Khi vẽ:
        scaled_rect = hover_fx.get_scaled_rect(button_rect)
        scaled_image = hover_fx.scale_surface(button_image)
    """
    
    def __init__(self, scale_factor=1.1, duration=0.15):
        """
        Args:
            scale_factor (float): Tỷ lệ phóng to khi hover (VD: 1.1 = 110%)
            duration (float): Thời gian animation scale (giây)
        """
        self.scale_factor = scale_factor
        self.duration = duration
        
        self.current_scale = 1.0
        self.target_scale = 1.0
        self.is_hovering = False
        
        # Velocity cho smooth damping
        self.scale_velocity = 0.0
    
    def update(self, is_hovering, dt):
        """
        Cập nhật trạng thái hover.
        
        Args:
            is_hovering (bool): Có đang hover không?
            dt (float): Delta time
        """
        self.is_hovering = is_hovering
        
        # Set target scale
        self.target_scale = self.scale_factor if is_hovering else 1.0
        
        # Smooth interpolation
        if abs(self.current_scale - self.target_scale) > 0.001:
            # Tính speed dựa trên duration
            speed = abs(self.scale_factor - 1.0) / self.duration
            
            if self.current_scale < self.target_scale:
                self.current_scale += speed * dt
                if self.current_scale > self.target_scale:
                    self.current_scale = self.target_scale
            else:
                self.current_scale -= speed * dt
                if self.current_scale < self.target_scale:
                    self.current_scale = self.target_scale
        else:
            self.current_scale = self.target_scale
    
    def get_current_scale(self):
        """
        Trả về scale hiện tại.
        
        Returns:
            float: Scale từ 1.0 đến scale_factor
        """
        return self.current_scale
    
    def get_scaled_rect(self, original_rect):
        """
        Tính rect đã scale, căn giữa.
        
        Args:
            original_rect (pygame.Rect): Rect gốc
        
        Returns:
            pygame.Rect: Rect đã scale, căn giữa
        """
        center = original_rect.center
        
        new_width = int(original_rect.width * self.current_scale)
        new_height = int(original_rect.height * self.current_scale)
        
        new_rect = pygame.Rect(0, 0, new_width, new_height)
        new_rect.center = center
        
        return new_rect
    
    def scale_surface(self, surface):
        """
        Scale surface theo current_scale.
        
        Args:
            surface (pygame.Surface): Surface gốc
        
        Returns:
            pygame.Surface: Surface đã scale
        """
        if abs(self.current_scale - 1.0) < 0.001:
            return surface
        
        new_width = int(surface.get_width() * self.current_scale)
        new_height = int(surface.get_height() * self.current_scale)
        
        return pygame.transform.smoothscale(surface, (new_width, new_height))


class ClickRippleEffect:
    """
    Click ripple effect - Hiệu ứng sóng lan tỏa khi click.
    
    Một vòng tròn mở rộng từ điểm click, với alpha giảm dần.
    
    Usage:
        ripple = None
        
        # Khi click:
        if event.type == pygame.MOUSEBUTTONDOWN:
            ripple = ClickRippleEffect(event.pos, max_radius=50)
            ripple.start()
        
        # Mỗi frame:
        if ripple and ripple.is_active:
            ripple.update(dt)
            ripple.draw(surface)
    """
    
    def __init__(self, center, max_radius=50, duration=0.5, color=(255, 255, 255)):
        """
        Args:
            center (tuple): Vị trí trung tâm (x, y)
            max_radius (int): Bán kính tối đa
            duration (float): Thời gian hiệu ứng (giây)
            color (tuple): Màu sóng (R, G, B)
        """
        self.center = center
        self.max_radius = max_radius
        self.duration = duration
        self.color = color
        
        self.current_radius = 0
        self.alpha = 255
        
        self.elapsed_time = 0.0
        self.is_active = False
    
    def start(self):
        """Bắt đầu hiệu ứng."""
        self.is_active = True
        self.elapsed_time = 0.0
        self.current_radius = 0
        self.alpha = 255
    
    def update(self, dt):
        """
        Cập nhật hiệu ứng.
        
        Args:
            dt (float): Delta time
        """
        if not self.is_active:
            return
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.duration:
            self.is_active = False
            return
        
        # Tính progress
        progress = min(1.0, self.elapsed_time / self.duration)
        eased_progress = ease_out_quad(progress)
        
        # Mở rộng radius
        self.current_radius = int(lerp(0, self.max_radius, eased_progress))
        
        # Giảm alpha
        self.alpha = int(lerp(255, 0, progress))
    
    def draw(self, surface):
        """
        Vẽ ripple lên surface.
        
        Args:
            surface (pygame.Surface): Surface để vẽ
        """
        if not self.is_active or self.current_radius <= 0:
            return
        
        # Tạo surface tạm với alpha
        ripple_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        
        # Vẽ vòng tròn
        color_with_alpha = (*self.color, self.alpha)
        pygame.draw.circle(
            ripple_surface,
            color_with_alpha,
            (self.max_radius, self.max_radius),
            self.current_radius,
            width=3  # Độ dày viền
        )
        
        # Blit lên surface chính
        ripple_rect = ripple_surface.get_rect(center=self.center)
        surface.blit(ripple_surface, ripple_rect.topleft)


class GlowEffect:
    """
    Glow effect - Viền sáng xung quanh button.
    
    Có 2 mode:
    - Static: Viền sáng cố định
    - Pulsing: Viền sáng nhấp nháy (breathing effect)
    
    Usage:
        glow = GlowEffect(color=(255, 215, 0), intensity=1.0, pulsing=True)
        
        # Mỗi frame:
        glow.update(dt)
        glow.draw(surface, button_rect)
    """
    
    def __init__(self, color=(255, 215, 0), intensity=1.0, pulsing=True, pulse_speed=2.0, glow_width=5):
        """
        Args:
            color (tuple): Màu glow (R, G, B)
            intensity (float): Độ sáng (0.0 - 1.0)
            pulsing (bool): Có nhấp nháy không?
            pulse_speed (float): Tốc độ nhấp nháy (Hz)
            glow_width (int): Độ dày viền sáng
        """
        self.color = color
        self.base_intensity = intensity
        self.pulsing = pulsing
        self.pulse_speed = pulse_speed
        self.glow_width = glow_width
        
        self.current_intensity = intensity
        self.pulse_time = 0.0
    
    def update(self, dt):
        """
        Cập nhật hiệu ứng (nếu pulsing).
        
        Args:
            dt (float): Delta time
        """
        if not self.pulsing:
            self.current_intensity = self.base_intensity
            return
        
        # Tăng pulse time
        self.pulse_time += dt
        
        # Tính intensity bằng sine wave
        # Dao động từ 0.3 đến 1.0
        wave = math.sin(self.pulse_time * self.pulse_speed * 2 * math.pi)
        self.current_intensity = lerp(0.3, 1.0, (wave + 1.0) / 2.0) * self.base_intensity
    
    def draw(self, surface, rect, expand=5):
        """
        Vẽ glow xung quanh rect.
        
        Args:
            surface (pygame.Surface): Surface để vẽ
            rect (pygame.Rect): Rect của button
            expand (int): Mở rộng glow ra ngoài rect (pixels)
        """
        # Tính alpha dựa trên intensity
        alpha = int(255 * self.current_intensity)
        
        # Tạo rect mở rộng
        glow_rect = rect.inflate(expand * 2, expand * 2)
        
        # Vẽ nhiều lớp với alpha giảm dần (để tạo hiệu ứng blur)
        for i in range(self.glow_width):
            current_alpha = int(alpha * (1.0 - i / self.glow_width))
            if current_alpha <= 0:
                break
            
            color_with_alpha = (*self.color, current_alpha)
            
            # Vẽ rect với border radius
            try:
                pygame.draw.rect(
                    surface,
                    color_with_alpha,
                    glow_rect.inflate(i * 2, i * 2),
                    width=2,
                    border_radius=10
                )
            except:
                # Fallback nếu pygame không hỗ trợ border_radius
                pygame.draw.rect(
                    surface,
                    color_with_alpha,
                    glow_rect.inflate(i * 2, i * 2),
                    width=2
                )


class PressEffect:
    """
    Press effect - Hiệu ứng nhấn xuống button.
    
    Button scale nhỏ lại khi nhấn, sau đó bounce trở lại.
    
    Usage:
        press_fx = PressEffect()
        
        # Khi click:
        if event.type == pygame.MOUSEBUTTONDOWN:
            press_fx.trigger()
        
        # Mỗi frame:
        press_fx.update(dt)
        scaled_rect = press_fx.apply_to_rect(button_rect)
    """
    
    def __init__(self, press_scale=0.95, duration=0.3):
        """
        Args:
            press_scale (float): Scale khi nhấn (VD: 0.95 = 95%)
            duration (float): Thời gian animation (giây)
        """
        self.press_scale = press_scale
        self.duration = duration
        
        self.current_scale = 1.0
        self.is_animating = False
        self.elapsed_time = 0.0
    
    def trigger(self):
        """Kích hoạt hiệu ứng nhấn."""
        self.is_animating = True
        self.elapsed_time = 0.0
    
    def update(self, dt):
        """
        Cập nhật animation.
        
        Args:
            dt (float): Delta time
        """
        if not self.is_animating:
            self.current_scale = 1.0
            return
        
        self.elapsed_time += dt
        
        if self.elapsed_time >= self.duration:
            self.is_animating = False
            self.current_scale = 1.0
            return
        
        # Tính progress
        progress = min(1.0, self.elapsed_time / self.duration)
        
        # Bounce từ press_scale về 1.0
        eased_progress = ease_out_bounce(progress)
        self.current_scale = lerp(self.press_scale, 1.0, eased_progress)
    
    def apply_to_rect(self, rect):
        """
        Apply scale lên rect.
        
        Args:
            rect (pygame.Rect): Rect gốc
        
        Returns:
            pygame.Rect: Rect đã scale
        """
        if abs(self.current_scale - 1.0) < 0.001:
            return rect
        
        center = rect.center
        new_width = int(rect.width * self.current_scale)
        new_height = int(rect.height * self.current_scale)
        
        new_rect = pygame.Rect(0, 0, new_width, new_height)
        new_rect.center = center
        
        return new_rect
    
    def apply_to_surface(self, surface):
        """
        Apply scale lên surface.
        
        Args:
            surface (pygame.Surface): Surface gốc
        
        Returns:
            pygame.Surface: Surface đã scale
        """
        if abs(self.current_scale - 1.0) < 0.001:
            return surface
        
        new_width = int(surface.get_width() * self.current_scale)
        new_height = int(surface.get_height() * self.current_scale)
        
        return pygame.transform.smoothscale(surface, (new_width, new_height))
