"""
GIF Animation Handler - Xử lý hiệu ứng GIF động
================================================
Load và phát GIF animations trong Pygame với hỗ trợ async loading.
"""

import pygame
import os
import threading
from PIL import Image

class GifAnimation:
    """
    Class để load và phát GIF animations trong Pygame.
    Hỗ trợ async loading để tránh block main thread.
    
    Usage:
        gif = GifAnimation('path/to/file.gif', duration=2.0)
        gif.load_async()  # Load không block
        
        # Trong game loop:
        if gif.is_loaded:
            gif.play()
            gif.update(dt)
            if gif.is_playing:
                gif.draw(surface, (x, y))
    """
    
    def __init__(self, gif_path, duration=2.0, scale_size=None, auto_load=True, auto_clear=False):
        """
        Args:
            gif_path (str): Đường dẫn đến file GIF
            duration (float): Thời gian phát (giây), None = lặp vô hạn
            scale_size (tuple): Kích thước scale (width, height), None = giữ nguyên
            auto_load (bool): Tự động load đồng bộ (True) hoặc đợi load_async() (False)
            auto_clear (bool): Tự động giải phóng frames sau khi play xong (tiết kiệm RAM)
        """
        self.gif_path = gif_path
        self.duration = duration
        self.scale_size = scale_size
        self.auto_clear = auto_clear
        
        self.frames = []
        self.frame_durations = []
        self.current_frame_index = 0
        self.elapsed_time = 0.0
        self.frame_time = 0.0
        self.total_elapsed = 0.0
        
        self.is_playing = False
        self.is_loaded = False
        self.is_loading = False
        self._loading_thread = None
        
        if auto_load:
            self._load_gif()
    
    def _load_gif(self):
        """Load GIF và chuyển thành pygame surfaces."""
        if not os.path.exists(self.gif_path):
            print(f"GIF không tồn tại: {self.gif_path}")
            self.is_loading = False
            return
        
        try:
            self.is_loading = True
            
            # Mở GIF bằng PIL
            gif = Image.open(self.gif_path)
            
            # Lưu tạm frames và durations
            temp_frames = []
            temp_durations = []
            
            # Lấy tất cả frames
            frame_index = 0
            while True:
                try:
                    gif.seek(frame_index)
                    
                    # Chuyển frame sang RGBA
                    frame = gif.convert('RGBA')
                    
                    # Scale nếu cần
                    if self.scale_size:
                        frame = frame.resize(self.scale_size, Image.Resampling.LANCZOS)
                    
                    # Chuyển PIL Image sang Pygame Surface
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    
                    pygame_surface = pygame.image.fromstring(data, size, mode)
                    temp_frames.append(pygame_surface)
                    
                    # Lấy thời gian của frame (milliseconds)
                    try:
                        frame_duration = gif.info.get('duration', 100) / 1000.0  # Chuyển sang giây
                    except:
                        frame_duration = 0.1  # Mặc định 100ms
                    
                    temp_durations.append(frame_duration)
                    
                    frame_index += 1
                    
                except EOFError:
                    # Hết frames
                    break
            
            # Gán vào self một lần (thread-safe hơn)
            if temp_frames:
                self.frames = temp_frames
                self.frame_durations = temp_durations
                self.is_loaded = True
                print(f"Đã load GIF: {self.gif_path} - {len(self.frames)} frames")
            else:
                print(f"Không có frames trong GIF: {self.gif_path}")
                
        except Exception as e:
            print(f"Lỗi load GIF {self.gif_path}: {e}")
        finally:
            self.is_loading = False
    
    def load_async(self):
        """Load GIF trong background thread (không block main thread)."""
        if self.is_loaded or self.is_loading:
            return
        
        self._loading_thread = threading.Thread(target=self._load_gif, daemon=True)
        self._loading_thread.start()
    
    def wait_for_load(self, timeout=5.0):
        """
        Chờ loading hoàn thành (nếu đang load async).
        
        Args:
            timeout (float): Thời gian chờ tối đa (giây)
        
        Returns:
            bool: True nếu load thành công, False nếu timeout
        """
        if self._loading_thread and self._loading_thread.is_alive():
            self._loading_thread.join(timeout=timeout)
        return self.is_loaded
    
    def play(self):
        """Bắt đầu phát animation."""
        if not self.is_loaded:
            return
        
        self.is_playing = True
        self.current_frame_index = 0
        self.elapsed_time = 0.0
        self.frame_time = 0.0
        self.total_elapsed = 0.0
    
    def stop(self):
        """Dừng animation."""
        self.is_playing = False
    
    def reset(self):
        """Reset animation về frame đầu."""
        self.current_frame_index = 0
        self.elapsed_time = 0.0
        self.frame_time = 0.0
        self.total_elapsed = 0.0
    
    def update(self, dt):
        """
        Update animation.
        
        Args:
            dt (float): Delta time (giây)
        """
        if not self.is_playing or not self.frames:
            return
        
        self.total_elapsed += dt
        self.frame_time += dt
        
        # Kiểm tra duration
        if self.duration is not None and self.total_elapsed >= self.duration:
            self.is_playing = False
            # Tự động giải phóng frames nếu auto_clear=True
            if self.auto_clear:
                self.clear_frames()
            return
        
        # Chuyển frame
        current_frame_duration = self.frame_durations[self.current_frame_index]
        if self.frame_time >= current_frame_duration:
            self.frame_time = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
    
    def draw(self, surface, position, center=False):
        """
        Vẽ frame hiện tại.
        
        Args:
            surface (pygame.Surface): Surface để vẽ
            position (tuple): Vị trí (x, y)
            center (bool): Căn giữa theo position?
        """
        if not self.is_playing or not self.frames:
            return
        
        current_frame = self.frames[self.current_frame_index]
        
        if center:
            rect = current_frame.get_rect(center=position)
            surface.blit(current_frame, rect.topleft)
        else:
            surface.blit(current_frame, position)
    
    def get_current_frame_surface(self):
        """
        Lấy surface của frame hiện tại.
        
        Returns:
            pygame.Surface hoặc None
        """
        if not self.frames:
            return None
        return self.frames[self.current_frame_index]
    
    def clear_frames(self):
        """
        Giải phóng frames khỏi RAM để tiết kiệm memory.
        Hữu ích khi GIF đã phát xong và không cần nữa.
        """
        num_frames = len(self.frames)
        self.frames.clear()
        self.frame_durations.clear()
        self.is_loaded = False
        self.is_playing = False
        if num_frames > 0:
            print(f"Cleared {num_frames} GIF frames from memory")
