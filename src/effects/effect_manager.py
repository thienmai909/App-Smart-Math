"""
Effect Manager - Quản lý hiệu ứng tập trung
===========================================
Singleton manager để áp dụng transitions và effects một cách dễ dàng.

Usage:
    # Import manager
    from src.effects.effect_manager import EffectManager
    
    # Lấy instance (singleton)
    fx = EffectManager.get_instance()
    
    # Áp dụng transition đơn giản
    fx.fade_to_black(callback=lambda: game_manager.switch_screen("LEVEL"))
    
    # Trong game loop
    fx.update(dt)
    fx.draw(surface)
"""

import pygame
from typing import Callable, Optional, Tuple, Dict, Any

# Try relative import first, fallback to direct import
try:
    from .transitions import FadeTransition, SlideTransition, ZoomTransition
    from .base_effect import BaseEffect
except ImportError:
    from transitions import FadeTransition, SlideTransition, ZoomTransition
    from base_effect import BaseEffect


class EffectManager:
    """
    Singleton Effect Manager - Quản lý tất cả transitions và effects.
    
    Đơn giản hóa việc áp dụng hiệu ứng chuyển màn hình:
    - Tự động xử lý fade out/in
    - Tự động gọi callback khi transition xong
    - Dễ dàng áp dụng với 1 dòng code
    """
    
    _instance = None
    
    def __init__(self, screen_size=(1200, 600)):
        """
        Khởi tạo Effect Manager.
        
        Args:
            screen_size (tuple): Kích thước màn hình (width, height)
        """
        self.screen_size = screen_size
        self.active_transition = None
        self.pending_callback = None
        self.transition_queue = []  # Queue cho nhiều transitions liên tiếp
        
        # Cấu hình mặc định
        self.default_fade_duration = 0.3
        self.default_slide_duration = 0.6
        self.default_zoom_duration = 0.7
        
    @classmethod
    def get_instance(cls, screen_size=(1200, 600)):
        """
        Lấy singleton instance của EffectManager.
        
        Args:
            screen_size (tuple): Kích thước màn hình (chỉ dùng lần đầu)
            
        Returns:
            EffectManager: Instance duy nhất
        """
        if cls._instance is None:
            cls._instance = cls(screen_size)
        return cls._instance
    
    @classmethod
    def initialize(cls, screen_size):
        """
        Khởi tạo hoặc reset EffectManager với screen size mới.
        
        Args:
            screen_size (tuple): Kích thước màn hình
        """
        cls._instance = cls(screen_size)
        return cls._instance
    
    # ========================================================================
    # CORE METHODS
    # ========================================================================
    
    def update(self, dt: float):
        """
        Update transition hiện tại.
        
        Args:
            dt (float): Delta time (giây)
        """
        if self.active_transition and self.active_transition.is_active:
            self.active_transition.update(dt)
            
            # Nếu transition xong, gọi callback
            if self.active_transition.is_finished:
                if self.pending_callback:
                    callback = self.pending_callback
                    self.pending_callback = None
                    callback()  # Gọi callback (vd: chuyển màn hình)
                
                # Kiểm tra queue có transition tiếp theo không
                if self.transition_queue:
                    next_transition = self.transition_queue.pop(0)
                    self.active_transition = next_transition['transition']
                    self.pending_callback = next_transition['callback']
                    self.active_transition.start()
                else:
                    self.active_transition = None
    
    def draw(self, surface: pygame.Surface):
        """
        Vẽ transition lên màn hình.
        
        Args:
            surface (pygame.Surface): Surface để vẽ
        """
        if self.active_transition and self.active_transition.is_active:
            self.active_transition.draw(surface)
    
    def is_transitioning(self) -> bool:
        """
        Kiểm tra có transition đang chạy không.
        
        Returns:
            bool: True nếu đang có transition
        """
        return self.active_transition is not None and self.active_transition.is_active
    
    def clear(self):
        """Xóa tất cả transitions và callbacks."""
        self.active_transition = None
        self.pending_callback = None
        self.transition_queue.clear()
    
    # ========================================================================
    # FADE TRANSITIONS - Dễ dùng nhất
    # ========================================================================
    
    def fade_to_black(self, callback: Optional[Callable] = None, duration: Optional[float] = None):
        """
        Fade màn hình sang đen, sau đó gọi callback (vd: chuyển màn).
        
        Args:
            callback (Callable): Hàm gọi khi fade out xong (vd: lambda: game.switch_screen("LEVEL"))
            duration (float): Thời gian fade (mặc định 0.3)
            
        Example:
            fx.fade_to_black(callback=lambda: game_manager.switch_screen("LEVEL"))
        """
        duration = duration or self.default_fade_duration
        
        fade_out = FadeTransition(
            fade_in=False,
            duration=duration,
            color=(0, 0, 0),
            screen_size=self.screen_size
        )
        fade_out.start()
        
        self.active_transition = fade_out
        self.pending_callback = callback
    
    def fade_from_black(self, callback: Optional[Callable] = None, duration: Optional[float] = None):
        """
        Fade màn hình từ đen về bình thường.
        
        Args:
            callback (Callable): Hàm gọi khi fade in xong
            duration (float): Thời gian fade
            
        Example:
            fx.fade_from_black()  # Chỉ fade in, không callback
        """
        duration = duration or self.default_fade_duration
        
        fade_in = FadeTransition(
            fade_in=True,
            duration=duration,
            color=(0, 0, 0),
            screen_size=self.screen_size
        )
        fade_in.start()
        
        self.active_transition = fade_in
        self.pending_callback = callback
    
    def fade_transition(self, callback: Optional[Callable] = None, 
                       fade_out_duration: Optional[float] = None,
                       fade_in_duration: Optional[float] = None,
                       color: Tuple[int, int, int] = (0, 0, 0)):
        """
        Full fade transition: fade out -> callback -> fade in.
        
        Tự động xử lý fade out, gọi callback (chuyển màn), rồi fade in.
        
        Args:
            callback (Callable): Hàm gọi giữa fade out và fade in
            fade_out_duration (float): Thời gian fade out
            fade_in_duration (float): Thời gian fade in
            color (tuple): Màu fade (R, G, B)
            
        Example:
            fx.fade_transition(callback=lambda: game_manager.switch_screen("LEVEL"))
        """
        fade_out_duration = fade_out_duration or self.default_fade_duration
        fade_in_duration = fade_in_duration or self.default_fade_duration
        
        # Fade out
        fade_out = FadeTransition(
            fade_in=False,
            duration=fade_out_duration,
            color=color,
            screen_size=self.screen_size
        )
        fade_out.start()
        
        self.active_transition = fade_out
        self.pending_callback = callback
        
        # Queue fade in
        fade_in = FadeTransition(
            fade_in=True,
            duration=fade_in_duration,
            color=color,
            screen_size=self.screen_size
        )
        
        self.transition_queue.append({
            'transition': fade_in,
            'callback': None
        })
    
    # ========================================================================
    # SLIDE TRANSITIONS
    # ========================================================================
    
    def slide_screen(self, direction: str = "left", 
                    callback: Optional[Callable] = None,
                    duration: Optional[float] = None):
        """
        Slide transition - màn hình mới trượt vào.
        
        Args:
            direction (str): "left", "right", "up", "down"
            callback (Callable): Hàm gọi ngay khi bắt đầu slide (để switch screen)
            duration (float): Thời gian slide
            
        Example:
            fx.slide_screen("left", callback=lambda: game.switch_screen("LEVEL"))
            
        Note:
            - Callback được gọi NGAY khi bắt đầu (để chuẩn bị màn mới)
            - Screen Manager cần xử lý việc vẽ màn mới với offset từ slide.get_offset()
        """
        duration = duration or self.default_slide_duration
        
        # Gọi callback NGAY để switch screen (để có màn mới để slide vào)
        if callback:
            callback()
        
        slide = SlideTransition(
            direction=direction,
            duration=duration,
            screen_size=self.screen_size
        )
        slide.start()
        
        self.active_transition = slide
        self.pending_callback = None  # Callback đã gọi rồi
    
    def get_slide_offset(self) -> Tuple[int, int]:
        """
        Lấy offset của slide transition (nếu đang có).
        
        Returns:
            tuple: (offset_x, offset_y) hoặc (0, 0) nếu không có slide
        """
        if (self.active_transition and 
            isinstance(self.active_transition, SlideTransition) and
            self.active_transition.is_active):
            return self.active_transition.get_offset()
        return (0, 0)
    
    # ========================================================================
    # ZOOM TRANSITIONS
    # ========================================================================
    
    def zoom_in(self, callback: Optional[Callable] = None,
               duration: Optional[float] = None,
               min_scale: float = 0.0):
        """
        Zoom in transition - màn hình từ nhỏ -> bình thường.
        
        Args:
            callback (Callable): Hàm gọi ngay khi bắt đầu zoom
            duration (float): Thời gian zoom
            min_scale (float): Scale nhỏ nhất (0.0 = từ điểm)
            
        Example:
            fx.zoom_in(callback=lambda: game.switch_screen("LEVEL"))
        """
        duration = duration or self.default_zoom_duration
        
        # Gọi callback NGAY để switch screen
        if callback:
            callback()
        
        zoom = ZoomTransition(
            zoom_in=True,
            duration=duration,
            min_scale=min_scale,
            max_scale=1.0,
            screen_size=self.screen_size
        )
        zoom.start()
        
        self.active_transition = zoom
        self.pending_callback = None
    
    def zoom_out(self, callback: Optional[Callable] = None,
                duration: Optional[float] = None,
                min_scale: float = 0.0):
        """
        Zoom out transition - màn hình từ bình thường -> nhỏ.
        
        Args:
            callback (Callable): Hàm gọi khi zoom out xong
            duration (float): Thời gian zoom
            min_scale (float): Scale nhỏ nhất
            
        Example:
            fx.zoom_out(callback=lambda: game.switch_screen("LEVEL"))
        """
        duration = duration or self.default_zoom_duration
        
        zoom = ZoomTransition(
            zoom_in=False,
            duration=duration,
            min_scale=min_scale,
            max_scale=1.0,
            screen_size=self.screen_size
        )
        zoom.start()
        
        self.active_transition = zoom
        self.pending_callback = callback
    
    def get_zoom_info(self) -> Dict[str, Any]:
        """
        Lấy thông tin zoom hiện tại (nếu đang có zoom transition).
        
        Returns:
            dict: {'scale': float, 'scaled_size': tuple, 'offset': tuple}
                  Hoặc None nếu không có zoom
        """
        if (self.active_transition and 
            isinstance(self.active_transition, ZoomTransition) and
            self.active_transition.is_active):
            return {
                'scale': self.active_transition.get_scale(),
                'scaled_size': self.active_transition.get_scaled_size(),
                'offset': self.active_transition.get_center_offset()
            }
        return None
    
    # ========================================================================
    # CUSTOM TRANSITION
    # ========================================================================
    
    def play_transition(self, transition: BaseEffect, callback: Optional[Callable] = None):
        """
        Chạy một transition tùy chỉnh.
        
        Args:
            transition (BaseEffect): Transition đã tạo sẵn
            callback (Callable): Hàm gọi khi transition xong
            
        Example:
            custom_fade = FadeTransition(fade_in=False, duration=1.0, color=(255, 0, 0))
            fx.play_transition(custom_fade, callback=lambda: print("Done!"))
        """
        transition.start()
        self.active_transition = transition
        self.pending_callback = callback
    
    # ========================================================================
    # CONFIGURATION
    # ========================================================================
    
    def set_default_durations(self, fade: float = 0.3, slide: float = 0.6, zoom: float = 0.7):
        """
        Đặt thời gian mặc định cho các transitions.
        
        Args:
            fade (float): Thời gian fade mặc định
            slide (float): Thời gian slide mặc định
            zoom (float): Thời gian zoom mặc định
        """
        self.default_fade_duration = fade
        self.default_slide_duration = slide
        self.default_zoom_duration = zoom


# ============================================================================
# GLOBAL FUNCTIONS - Shortcut để sử dụng nhanh
# ============================================================================

def init_effect_manager(screen_size):
    """
    Khởi tạo EffectManager với screen size.
    
    Gọi hàm này trong game initialization.
    
    Args:
        screen_size (tuple): (width, height)
        
    Returns:
        EffectManager: Instance đã khởi tạo
    """
    return EffectManager.initialize(screen_size)


def get_effect_manager():
    """
    Lấy EffectManager instance (shortcut).
    
    Returns:
        EffectManager: Instance singleton
    """
    return EffectManager.get_instance()
