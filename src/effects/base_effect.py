"""
Base Effect - Lớp cơ sở cho tất cả hiệu ứng
============================================
Cung cấp interface chung và lifecycle management cho mọi hiệu ứng.
"""

import time


class BaseEffect:
    """
    Lớp cơ sở cho tất cả hiệu ứng trong game.
    
    Lifecycle:
    1. Khởi tạo: __init__()
    2. Bắt đầu: start()
    3. Cập nhật: update(dt) - gọi mỗi frame
    4. Vẽ: draw(surface) - gọi mỗi frame
    5. Kết thúc: is_finished = True
    
    Attributes:
        duration (float): Thời gian hiệu ứng (giây)
        start_time (float): Thời điểm bắt đầu (time.time())
        is_active (bool): Hiệu ứng đang chạy?
        is_finished (bool): Hiệu ứng đã hoàn thành?
    """
    
    def __init__(self, duration=1.0):
        """
        Khởi tạo hiệu ứng.
        
        Args:
            duration (float): Thời gian chạy hiệu ứng (giây)
        """
        self.duration = duration
        self.start_time = None
        self.is_active = False
        self.is_finished = False
        self.elapsed_time = 0.0
    
    def start(self):
        """
        Bắt đầu hiệu ứng.
        Ghi lại thời điểm bắt đầu và set is_active = True.
        """
        self.start_time = time.time()
        self.is_active = True
        self.is_finished = False
        self.elapsed_time = 0.0
        self.on_start()
    
    def on_start(self):
        """
        Hook method - được gọi khi hiệu ứng bắt đầu.
        Override trong subclass nếu cần.
        """
        pass
    
    def update(self, dt):
        """
        Cập nhật hiệu ứng mỗi frame.
        
        Args:
            dt (float): Delta time (thời gian từ frame trước, giây)
        """
        if not self.is_active or self.is_finished:
            return
        
        self.elapsed_time += dt
        
        # Kiểm tra nếu đã hết thời gian
        if self.elapsed_time >= self.duration:
            self.elapsed_time = self.duration
            self.is_finished = True
            self.on_finish()
        
        self.on_update(dt)
    
    def on_update(self, dt):
        """
        Hook method - logic cập nhật cụ thể của hiệu ứng.
        Override trong subclass.
        
        Args:
            dt (float): Delta time
        """
        pass
    
    def on_finish(self):
        """
        Hook method - được gọi khi hiệu ứng kết thúc.
        Override trong subclass nếu cần cleanup.
        """
        pass
    
    def draw(self, surface):
        """
        Vẽ hiệu ứng lên surface.
        
        Args:
            surface (pygame.Surface): Surface để vẽ
        """
        if not self.is_active or self.is_finished:
            return
        
        self.on_draw(surface)
    
    def on_draw(self, surface):
        """
        Hook method - logic vẽ cụ thể của hiệu ứng.
        Override trong subclass.
        
        Args:
            surface (pygame.Surface): Surface để vẽ
        """
        pass
    
    def get_progress(self):
        """
        Tính progress của hiệu ứng (0.0 -> 1.0).
        
        Returns:
            float: Progress từ 0.0 (bắt đầu) đến 1.0 (kết thúc)
        """
        if not self.is_active or self.duration <= 0:
            return 0.0
        
        return min(1.0, self.elapsed_time / self.duration)
    
    def reset(self):
        """
        Reset hiệu ứng về trạng thái ban đầu.
        """
        self.start_time = None
        self.is_active = False
        self.is_finished = False
        self.elapsed_time = 0.0
    
    def stop(self):
        """
        Dừng hiệu ứng ngay lập tức.
        """
        self.is_active = False
        self.is_finished = True
