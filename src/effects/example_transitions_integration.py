"""
Ví Dụ Tích Hợp Transitions Vào Game Manager
============================================
File này demo cách tích hợp đầy đủ transitions vào GameManager của Smart Math.
"""

import pygame
from src.config import *
from src.effects import FadeTransition, SlideTransition, ZoomTransition


class GameManagerWithTransitions:
    """
    GameManager mở rộng với hỗ trợ transitions.
    
    Cách dùng:
    1. Thay thế GameManager hiện tại bằng class này
    2. Gọi switch_screen_with_transition() thay vì switch_screen()
    3. Transitions sẽ tự động chạy
    """
    
    def __init__(self):
        # ... (code khởi tạo của GameManager cũ)
        
        # Thêm biến cho transitions
        self.active_transition = None
        self.pending_screen = None
        self.transition_stage = None  # "fade_out", "fade_in", "slide", "zoom"
    
    # ============================================================================
    # METHOD 1: FADE TRANSITION (Đơn giản nhất)
    # ============================================================================
    
    def switch_screen_with_fade(self, screen_key, duration=0.3):
        """
        Chuyển màn hình với fade transition.
        
        Quy trình:
        1. Fade out màn hình cũ (đen)
        2. Chuyển sang màn hình mới
        3. Fade in màn hình mới (sáng)
        
        Args:
            screen_key (str): Tên màn hình đích ("HOME", "LEVEL", "GAMEPLAY")
            duration (float): Thời gian mỗi fade (giây)
        """
        if screen_key not in self.screens:
            return
        
        # Tạo fade out transition
        fade_out = FadeTransition(
            fade_in=False,
            duration=duration,
            color=(0, 0, 0),  # Đen
            screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        fade_out.start()
        
        # Lưu state
        self.active_transition = fade_out
        self.pending_screen = screen_key
        self.transition_stage = "fade_out"
    
    # ============================================================================
    # METHOD 2: SLIDE TRANSITION
    # ============================================================================
    
    def switch_screen_with_slide(self, screen_key, direction="left", duration=0.6):
        """
        Chuyển màn hình với slide transition.
        
        Args:
            screen_key (str): Tên màn hình đích
            direction (str): Hướng trượt ("left", "right", "up", "down")
            duration (float): Thời gian slide (giây)
        """
        if screen_key not in self.screens:
            return
        
        # Tạo slide transition
        slide = SlideTransition(
            direction=direction,
            duration=duration,
            screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        slide.start()
        
        # Lưu state
        self.active_transition = slide
        self.pending_screen = screen_key
        self.transition_stage = "slide"
    
    # ============================================================================
    # METHOD 3: ZOOM TRANSITION
    # ============================================================================
    
    def switch_screen_with_zoom(self, screen_key, zoom_in=True, duration=0.7):
        """
        Chuyển màn hình với zoom transition.
        
        Args:
            screen_key (str): Tên màn hình đích
            zoom_in (bool): True = zoom in, False = zoom out
            duration (float): Thời gian zoom (giây)
        """
        if screen_key not in self.screens:
            return
        
        zoom = ZoomTransition(
            zoom_in=zoom_in,
            duration=duration,
            screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        zoom.start()
        
        self.active_transition = zoom
        self.pending_screen = screen_key
        self.transition_stage = "zoom"
    
    # ============================================================================
    # UPDATE - XỬ LÝ TRANSITIONS
    # ============================================================================
    
    def update(self):
        """
        Update game - bao gồm cả transitions.
        
        QUAN TRỌNG: Gọi method này mỗi frame trong game loop.
        """
        dt = 1.0 / FPS
        
        # Update transition nếu đang chạy
        if self.active_transition and self.active_transition.is_active:
            self.active_transition.update(dt)
            
            # Kiểm tra transition đã xong chưa
            if self.active_transition.is_finished:
                self._on_transition_finished()
        
        # Update màn hình hiện tại (nếu không đang transition)
        if not self.active_transition or self.transition_stage in ["slide", "zoom"]:
            # Slide và Zoom vẫn update màn hình cũ
            self.active_screen.update()
    
    def _on_transition_finished(self):
        """
        Xử lý khi một giai đoạn transition kết thúc.
        """
        if self.transition_stage == "fade_out":
            # Fade out xong → Chuyển màn hình → Bắt đầu fade in
            self._switch_screen_immediately(self.pending_screen)
            
            # Tạo fade in
            fade_in = FadeTransition(
                fade_in=True,
                duration=0.3,
                color=(0, 0, 0),
                screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            fade_in.start()
            
            self.active_transition = fade_in
            self.transition_stage = "fade_in"
        
        elif self.transition_stage == "fade_in":
            # Fade in xong → Cleanup
            self.active_transition = None
            self.transition_stage = None
            self.pending_screen = None
        
        elif self.transition_stage == "slide":
            # Slide xong → Chuyển màn hình
            self._switch_screen_immediately(self.pending_screen)
            self.active_transition = None
            self.transition_stage = None
            self.pending_screen = None
        
        elif self.transition_stage == "zoom":
            # Zoom xong → Chuyển màn hình
            self._switch_screen_immediately(self.pending_screen)
            self.active_transition = None
            self.transition_stage = None
            self.pending_screen = None
    
    def _switch_screen_immediately(self, screen_key):
        """Chuyển màn hình ngay lập tức (không transition)."""
        if screen_key in self.screens:
            # Generate câu hỏi nếu chuyển sang GAMEPLAY
            if screen_key == "GAMEPLAY" and self.current_level_key:
                generator = QUESTION_GENERATORS.get(self.current_level_key)
                if generator:
                    self.questions_pool = generator(MAX_QUESTIONS)
                    self.question_index = 0
                self.screens[screen_key].on_enter()
            
            self.active_screen_key = screen_key
            self.active_screen = self.screens[self.active_screen_key]
    
    # ============================================================================
    # DRAW - VẼ VỚI TRANSITIONS
    # ============================================================================
    
    def draw(self, surface):
        """
        Vẽ game - bao gồm cả transitions.
        
        Thứ tự vẽ:
        1. Màn hình hiện tại
        2. Màn hình mới (nếu slide/zoom)
        3. Transition overlay (fade)
        """
        # Vẽ màn hình hiện tại bình thường
        self.active_screen.draw(surface)
        
        # Xử lý transitions đặc biệt
        if self.active_transition and self.active_transition.is_active:
            
            # SLIDE: Vẽ màn hình mới trượt vào
            if self.transition_stage == "slide" and self.pending_screen:
                # Tạo surface cho màn hình mới
                new_screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screens[self.pending_screen].draw(new_screen_surface)
                
                # Lấy offset và vẽ
                offset_x, offset_y = self.active_transition.get_offset()
                surface.blit(new_screen_surface, (offset_x, offset_y))
            
            # ZOOM: Vẽ màn hình zoom
            elif self.transition_stage == "zoom" and self.pending_screen:
                # Lấy scale info
                scale = self.active_transition.get_scale()
                scaled_size = self.active_transition.get_scaled_size()
                offset = self.active_transition.get_center_offset()
                
                # Tạo và scale màn hình mới
                new_screen_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screens[self.pending_screen].draw(new_screen_surface)
                
                if scaled_size[0] > 0 and scaled_size[1] > 0:
                    scaled_surface = pygame.transform.smoothscale(
                        new_screen_surface,
                        scaled_size
                    )
                    surface.blit(scaled_surface, offset)
                
                # Vẽ overlay tối
                self.active_transition.draw(surface)
            
            # FADE: Chỉ vẽ overlay
            elif self.transition_stage in ["fade_out", "fade_in"]:
                self.active_transition.draw(surface)


# ============================================================================
# VÍ DỤ SỬ DỤNG TRONG SCREENS
# ============================================================================

class HomeScreenWithTransition:
    """Ví dụ sử dụng transition trong HomeScreen."""
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.start_button_rect.collidepoint(mouse_pos):
                # Phát âm thanh
                self.game_manager.sounds['click'].play()
                
                # Chuyển màn với fade transition
                self.game_manager.switch_screen_with_fade("LEVEL", duration=0.3)
                
                # HOẶC slide transition
                # self.game_manager.switch_screen_with_slide("LEVEL", direction="left")
                
                # HOẶC zoom transition
                # self.game_manager.switch_screen_with_zoom("LEVEL", zoom_in=True)


class LevelSelectWithTransition:
    """Ví dụ transition khi chọn level."""
    
    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ... code check level không khóa
            
            if not is_locked:
                self.game_manager.current_level_key = selected_level['key']
                
                # Chuyển sang gameplay với zoom in effect
                self.game_manager.switch_screen_with_zoom(
                    "GAMEPLAY", 
                    zoom_in=True, 
                    duration=0.5
                )


class GameplayAfterFinish:
    """Ví dụ transition khi kết thúc gameplay."""
    
    def on_next_button_clicked(self):
        """Khi nhấn nút Next sau khi hoàn thành level."""
        # Về màn chọn level với slide transition
        self.game_manager.switch_screen_with_slide(
            "LEVEL",
            direction="right",  # Trượt ngược lại
            duration=0.6
        )
    
    def on_replay_button_clicked(self):
        """Khi nhấn nút Replay."""
        # Replay với fade nhanh
        self.game_manager.switch_screen_with_fade("GAMEPLAY", duration=0.2)


# ============================================================================
# TIPS & TRICKS
# ============================================================================

"""
1. Chọn transition phù hợp:
   - Fade: Dùng cho mọi chuyển màn (universal)
   - Slide: Dùng khi có hướng rõ ràng (back/forward)
   - Zoom: Dùng khi muốn focus/blur (enter game)

2. Duration hợp lý:
   - Fade: 0.2-0.4s (nhanh)
   - Slide: 0.5-0.8s (vừa)
   - Zoom: 0.6-1.0s (chậm, dramatic)

3. Kết hợp với âm thanh:
   - Play sound TRƯỚC khi start transition
   - Tạo cảm giác responsive

4. Performance:
   - Slide/Zoom tốn CPU hơn Fade (vì phải scale/blit)
   - Nếu lag, dùng Fade thay vì Slide/Zoom
   
5. Debugging:
   - In ra transition_stage để biết đang ở giai đoạn nào
   - Check is_active và is_finished
"""
