"""
Transitions - Hiệu ứng chuyển màn hình
======================================
Cung cấp các hiệu ứng chuyển cảnh mượt mà giữa các màn hình.
"""

import pygame

# Try relative import first (when used as module), fallback to direct import
try:
    from .base_effect import BaseEffect
    from .animation_utils import ease_in_out, ease_out_cubic, lerp
except ImportError:
    from base_effect import BaseEffect
    from animation_utils import ease_in_out, ease_out_cubic, lerp


class FadeTransition(BaseEffect):
    """
    Fade transition - Làm mờ/hiện màn hình.
    
    Có 2 mode:
    - Fade Out: Từ trong suốt -> đen (che khuất màn hình cũ)
    - Fade In: Từ đen -> trong suốt (hiện màn hình mới)
    
    Usage:
        # Fade out trước khi chuyển màn
        fade_out = FadeTransition(fade_in=False, duration=0.3)
        fade_out.start()
        
        # Sau khi chuyển màn, fade in
        fade_in = FadeTransition(fade_in=True, duration=0.3)
        fade_in.start()
    """
    
    def __init__(self, fade_in=True, duration=0.5, color=(0, 0, 0), screen_size=(1200, 600)):
        """
        Args:
            fade_in (bool): True = fade in (đen -> trong suốt), False = fade out (trong suốt -> đen)
            duration (float): Thời gian chuyển cảnh (giây)
            color (tuple): Màu overlay (R, G, B)
            screen_size (tuple): Kích thước màn hình (width, height)
        """
        super().__init__(duration)
        self.fade_in = fade_in
        self.color = color
        self.screen_size = screen_size
        self.alpha = 0 if fade_in else 255
        
        # Tạo surface overlay với alpha channel
        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
    
    def on_update(self, dt):
        """Cập nhật alpha dựa trên progress."""
        progress = self.get_progress()
        eased_progress = ease_in_out(progress)
        
        if self.fade_in:
            # Fade in: 255 -> 0
            self.alpha = int(lerp(255, 0, eased_progress))
        else:
            # Fade out: 0 -> 255
            self.alpha = int(lerp(0, 255, eased_progress))
    
    def on_draw(self, surface):
        """Vẽ overlay lên màn hình."""
        self.overlay.fill((*self.color, self.alpha))
        surface.blit(self.overlay, (0, 0))


class SlideTransition(BaseEffect):
    """
    Slide transition - Trượt màn hình từ một hướng.
    
    Directions: "left", "right", "up", "down"
    
    Usage:
        slide = SlideTransition(direction="left", duration=0.6)
        slide.start()
        # Trong draw(), dùng get_offset() để vẽ màn hình với offset
    """
    
    def __init__(self, direction="left", duration=0.6, screen_size=(1200, 600)):
        """
        Args:
            direction (str): Hướng trượt - "left", "right", "up", "down"
            duration (float): Thời gian chuyển cảnh (giây)
            screen_size (tuple): Kích thước màn hình (width, height)
        """
        super().__init__(duration)
        self.direction = direction.lower()
        self.screen_size = screen_size
        self.offset_x = 0
        self.offset_y = 0
        
        if self.direction not in ["left", "right", "up", "down"]:
            raise ValueError(f"Invalid direction: {direction}. Must be 'left', 'right', 'up', or 'down'.")
    
    def on_update(self, dt):
        """Tính offset dựa trên progress và direction."""
        progress = self.get_progress()
        eased_progress = ease_out_cubic(progress)
        
        width, height = self.screen_size
        
        if self.direction == "left":
            # Trượt từ phải sang trái
            self.offset_x = int(lerp(width, 0, eased_progress))
            self.offset_y = 0
        elif self.direction == "right":
            # Trượt từ trái sang phải
            self.offset_x = int(lerp(-width, 0, eased_progress))
            self.offset_y = 0
        elif self.direction == "up":
            # Trượt từ dưới lên
            self.offset_x = 0
            self.offset_y = int(lerp(height, 0, eased_progress))
        else:  # down
            # Trượt từ trên xuống
            self.offset_x = 0
            self.offset_y = int(lerp(-height, 0, eased_progress))
    
    def get_offset(self):
        """
        Trả về offset để vẽ màn hình.
        
        Returns:
            tuple: (offset_x, offset_y)
        """
        return (self.offset_x, self.offset_y)
    
    def on_draw(self, surface):
        """
        Slide không tự vẽ - screen phải dùng get_offset() để vẽ với offset.
        Method này để giữ tương thích với BaseEffect.
        """
        pass


class ZoomTransition(BaseEffect):
    """
    Zoom transition - Phóng to/thu nhỏ màn hình.
    
    Có 2 mode:
    - Zoom In: Scale từ 0 -> 1 (màn hình mới từ nhỏ -> bình thường)
    - Zoom Out: Scale từ 1 -> 0 (màn hình cũ từ bình thường -> nhỏ)
    
    Usage:
        zoom = ZoomTransition(zoom_in=True, duration=0.5)
        zoom.start()
        # Trong draw(), dùng get_scale() để scale màn hình
    """
    
    def __init__(self, zoom_in=True, duration=0.7, min_scale=0.0, max_scale=1.0, screen_size=(1200, 600)):
        """
        Args:
            zoom_in (bool): True = zoom in (0 -> 1), False = zoom out (1 -> 0)
            duration (float): Thời gian chuyển cảnh (giây)
            min_scale (float): Scale nhỏ nhất
            max_scale (float): Scale lớn nhất
            screen_size (tuple): Kích thước màn hình (width, height)
        """
        super().__init__(duration)
        self.zoom_in = zoom_in
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.screen_size = screen_size
        self.current_scale = min_scale if zoom_in else max_scale
        
        # Tạo overlay tối cho hiệu ứng mờ nền
        self.overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        self.overlay_alpha = 0
    
    def on_update(self, dt):
        """Cập nhật scale và alpha dựa trên progress."""
        progress = self.get_progress()
        eased_progress = ease_in_out(progress)
        
        if self.zoom_in:
            # Zoom in: min_scale -> max_scale
            self.current_scale = lerp(self.min_scale, self.max_scale, eased_progress)
            # Overlay dark: 200 -> 0
            self.overlay_alpha = int(lerp(200, 0, eased_progress))
        else:
            # Zoom out: max_scale -> min_scale
            self.current_scale = lerp(self.max_scale, self.min_scale, eased_progress)
            # Overlay dark: 0 -> 200
            self.overlay_alpha = int(lerp(0, 200, eased_progress))
    
    def get_scale(self):
        """
        Trả về scale hiện tại.
        
        Returns:
            float: Scale từ min_scale đến max_scale
        """
        return self.current_scale
    
    def get_scaled_size(self):
        """
        Trả về kích thước màn hình đã scale.
        
        Returns:
            tuple: (scaled_width, scaled_height)
        """
        width, height = self.screen_size
        return (int(width * self.current_scale), int(height * self.current_scale))
    
    def get_center_offset(self):
        """
        Trả về offset để căn giữa màn hình đã scale.
        
        Returns:
            tuple: (offset_x, offset_y)
        """
        width, height = self.screen_size
        scaled_width, scaled_height = self.get_scaled_size()
        
        offset_x = (width - scaled_width) // 2
        offset_y = (height - scaled_height) // 2
        
        return (offset_x, offset_y)
    
    def on_draw(self, surface):
        """Vẽ overlay tối (nếu cần)."""
        if self.overlay_alpha > 0:
            self.overlay.fill((0, 0, 0, self.overlay_alpha))
            surface.blit(self.overlay, (0, 0))


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_fade_transition(fade_in=True, duration=0.5, color=(0, 0, 0)):
    """
    Factory function để tạo FadeTransition dễ dàng.
    
    Args:
        fade_in (bool): True = fade in, False = fade out
        duration (float): Thời gian chuyển cảnh
        color (tuple): Màu overlay
    
    Returns:
        FadeTransition: Instance đã tạo
    """
    from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
    return FadeTransition(fade_in, duration, color, (SCREEN_WIDTH, SCREEN_HEIGHT))


def create_slide_transition(direction="left", duration=0.6):
    """
    Factory function để tạo SlideTransition dễ dàng.
    
    Args:
        direction (str): Hướng trượt
        duration (float): Thời gian chuyển cảnh
    
    Returns:
        SlideTransition: Instance đã tạo
    """
    from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
    return SlideTransition(direction, duration, (SCREEN_WIDTH, SCREEN_HEIGHT))


def create_zoom_transition(zoom_in=True, duration=0.7):
    """
    Factory function để tạo ZoomTransition dễ dàng.
    
    Args:
        zoom_in (bool): True = zoom in, False = zoom out
        duration (float): Thời gian chuyển cảnh
    
    Returns:
        ZoomTransition: Instance đã tạo
    """
    from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
    return ZoomTransition(zoom_in, duration, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
