"""
Demo các hiệu ứng của Smart Math Effects Module
================================================
Chạy file này để xem demo tất cả hiệu ứng.

Điều khiển:
- Phím số 1-6: Chuyển giữa các demo
- ESC: Thoát
- Space: Trigger hiệu ứng (một số demo)
"""

import pygame
import sys
import os

# Import hiệu ứng từ cùng thư mục
from transitions import (
    FadeTransition,
    SlideTransition,
    ZoomTransition
)
from button_effects import (
    HoverEffect,
    ClickRippleEffect,
    GlowEffect,
    PressEffect
)
from progress_effects import (
    StarPopEffect,
    ProgressPulseEffect,
    ScoreCountUpEffect
)


# Cấu hình
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 120
BG_COLOR = (28, 28, 28)

# Màu
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (255, 215, 0)
COLOR_GREEN = (0, 200, 0)
COLOR_BLUE = (0, 150, 255)


class EffectsDemo:
    """Manager cho các demo hiệu ứng."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Smart Math - Effects Demo")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.font_small = pygame.font.SysFont("Arial", 20)
        
        # Current demo
        self.current_demo = 0
        self.demos = [
            self.demo_transitions,
            self.demo_button_hover,
            self.demo_button_click,
            self.demo_button_glow,
            self.demo_progress_bar,
            self.demo_star_pop,
        ]
        self.demo_names = [
            "1. Transitions (Fade/Slide/Zoom)",
            "2. Button Hover Effect",
            "3. Button Click Effects",
            "4. Button Glow Effect",
            "5. Progress Bar Animation",
            "6. Star Pop Effect",
        ]
        
        # Setup demos
        self.setup_demos()
    
    def setup_demos(self):
        """Khởi tạo các hiệu ứng cho demo."""
        # Demo 1: Transitions
        self.fade_in = FadeTransition(fade_in=True, duration=1.0, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_out = FadeTransition(fade_in=False, duration=1.0, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.slide = SlideTransition("left", duration=1.0, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.zoom = ZoomTransition(zoom_in=True, duration=1.0, screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.current_transition = None
        self.transition_index = 0
        
        # Demo 2: Button Hover
        self.hover_fx = HoverEffect(scale_factor=1.15, duration=0.2)
        self.button_rect = pygame.Rect(500, 250, 200, 80)
        
        # Demo 3: Button Click
        self.press_fx = PressEffect()
        self.ripples = []
        
        # Demo 4: Glow
        self.glow_fx = GlowEffect(color=COLOR_GOLD, pulsing=True)
        
        # Demo 5: Progress Bar
        self.progress_fx = ProgressBarFillEffect(duration=0.5)
        self.progress_pulse = ProgressPulseEffect(speed=50)
        self.current_progress_target = 0.0
        
        # Demo 6: Star Pop
        self.star_pops = []
        self.star_positions = [
            (300, 300), (600, 300), (900, 300)
        ]
    
    def run(self):
        """Main loop."""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_1:
                        self.current_demo = 0
                    elif event.key == pygame.K_2:
                        self.current_demo = 1
                    elif event.key == pygame.K_3:
                        self.current_demo = 2
                    elif event.key == pygame.K_4:
                        self.current_demo = 3
                    elif event.key == pygame.K_5:
                        self.current_demo = 4
                    elif event.key == pygame.K_6:
                        self.current_demo = 5
                    elif event.key == pygame.K_SPACE:
                        self.trigger_effect()
                
                # Mouse events cho click demo
                if event.type == pygame.MOUSEBUTTONDOWN and self.current_demo == 2:
                    ripple = ClickRippleEffect(event.pos, max_radius=80, duration=0.6, color=COLOR_BLUE)
                    ripple.start()
                    self.ripples.append(ripple)
                    self.press_fx.trigger()
            
            # Update
            self.update(dt)
            
            # Draw
            self.draw()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def trigger_effect(self):
        """Trigger effect khi nhấn Space."""
        if self.current_demo == 0:
            # Cycle transitions
            transitions = [self.fade_out, self.fade_in, self.slide, self.zoom]
            self.current_transition = transitions[self.transition_index % len(transitions)]
            self.current_transition.reset()
            self.current_transition.start()
            self.transition_index += 1
        
        elif self.current_demo == 4:
            # Random progress
            import random
            new_target = random.random()
            self.progress_fx.set_target(new_target)
            self.current_progress_target = new_target
        
        elif self.current_demo == 5:
            # Trigger star pop for all stars
            self.star_pops = []
            for pos in self.star_positions:
                star_pop = StarPopEffect(pos, duration=1.0)
                star_pop.start()
                self.star_pops.append(star_pop)
    
    def update(self, dt):
        """Update hiệu ứng."""
        # Update current demo
        if self.current_demo == 0:
            if self.current_transition and self.current_transition.is_active:
                self.current_transition.update(dt)
        
        elif self.current_demo == 1:
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.button_rect.collidepoint(mouse_pos)
            self.hover_fx.update(is_hovering, dt)
        
        elif self.current_demo == 2:
            self.press_fx.update(dt)
            # Update ripples
            for ripple in self.ripples[:]:
                ripple.update(dt)
                if not ripple.is_active:
                    self.ripples.remove(ripple)
        
        elif self.current_demo == 3:
            self.glow_fx.update(dt)
        
        elif self.current_demo == 4:
            self.progress_fx.update(dt)
            self.progress_pulse.update(dt)
        
        elif self.current_demo == 5:
            for star_pop in self.star_pops:
                star_pop.update(dt)
    
    def draw(self):
        """Vẽ demo hiện tại."""
        self.screen.fill(BG_COLOR)
        
        # Draw current demo
        self.demos[self.current_demo]()
        
        # Draw UI overlay
        self.draw_ui()
    
    def draw_ui(self):
        """Vẽ UI chung."""
        # Title
        title = self.font.render(self.demo_names[self.current_demo], True, COLOR_WHITE)
        self.screen.blit(title, (20, 20))
        
        # Instructions
        instructions = [
            "Phím 1-6: Chuyển demo",
            "Space: Trigger hiệu ứng",
            "ESC: Thoát"
        ]
        
        y = SCREEN_HEIGHT - 80
        for instr in instructions:
            text = self.font_small.render(instr, True, (150, 150, 150))
            self.screen.blit(text, (20, y))
            y += 25
    
    # ========== DEMO IMPLEMENTATIONS ==========
    
    def demo_transitions(self):
        """Demo transition effects."""
        # Vẽ một màn hình giả
        demo_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        demo_surface.fill((50, 100, 150))
        
        # Vẽ text
        text = self.font.render("Nhấn SPACE để xem transitions", True, COLOR_WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        demo_surface.blit(text, text_rect)
        
        # Blit lên screen
        self.screen.blit(demo_surface, (0, 0))
        
        # Apply transition
        if self.current_transition and self.current_transition.is_active:
            self.current_transition.draw(self.screen)
    
    def demo_button_hover(self):
        """Demo hover effect."""
        # Draw button
        scaled_rect = self.hover_fx.get_scaled_rect(self.button_rect)
        
        # Draw shadow
        shadow_rect = scaled_rect.inflate(10, 10)
        shadow_rect.y += 5
        pygame.draw.rect(self.screen, (0, 0, 0), shadow_rect, border_radius=10)
        
        # Draw button
        pygame.draw.rect(self.screen, COLOR_BLUE, scaled_rect, border_radius=10)
        
        # Draw text
        text = self.font.render("Hover Me!", True, COLOR_WHITE)
        text_rect = text.get_rect(center=scaled_rect.center)
        self.screen.blit(text, text_rect)
        
        # Instructions
        info = self.font_small.render("Di chuột qua button", True, (200, 200, 200))
        self.screen.blit(info, (450, 400))
    
    def demo_button_click(self):
        """Demo click ripple và press effects."""
        # Draw button với press effect
        display_rect = self.press_fx.apply_to_rect(self.button_rect)
        
        pygame.draw.rect(self.screen, COLOR_GREEN, display_rect, border_radius=10)
        
        text = self.font.render("Click Me!", True, COLOR_WHITE)
        text_rect = text.get_rect(center=display_rect.center)
        self.screen.blit(text, text_rect)
        
        # Draw ripples
        for ripple in self.ripples:
            ripple.draw(self.screen)
        
        # Instructions
        info = self.font_small.render("Click vào bất kỳ đâu", True, (200, 200, 200))
        self.screen.blit(info, (480, 400))
    
    def demo_button_glow(self):
        """Demo glow effect."""
        # Draw glow
        self.glow_fx.draw(self.screen, self.button_rect, expand=10)
        
        # Draw button
        pygame.draw.rect(self.screen, COLOR_GOLD, self.button_rect, border_radius=10)
        
        text = self.font.render("Glowing!", True, (50, 50, 50))
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)
    
    def demo_progress_bar(self):
        """Demo progress bar animation."""
        # Progress bar rect
        bar_x = 200
        bar_y = 250
        bar_width = 800
        bar_height = 60
        
        # Background
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), bg_rect, border_radius=30)
        
        # Fill
        current_progress = self.progress_fx.get_current_progress()
        fill_width = int(bar_width * current_progress)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)
            
            # Create pattern surface
            fill_surface = self.progress_pulse.create_pattern_surface(
                fill_width, bar_height,
                (100, 200, 100),
                pattern_type="diagonal"
            )
            
            # Clip to rounded rect (approximate)
            self.screen.blit(fill_surface, (bar_x, bar_y))
            pygame.draw.rect(self.screen, (100, 200, 100), fill_rect, border_radius=30, width=0)
        
        # Border
        pygame.draw.rect(self.screen, (100, 100, 100), bg_rect, width=3, border_radius=30)
        
        # Percentage text
        percent_text = self.font.render(f"{int(current_progress * 100)}%", True, COLOR_WHITE)
        percent_rect = percent_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y + bar_height // 2))
        self.screen.blit(percent_text, percent_rect)
        
        # Target info
        info = self.font_small.render(f"Target: {int(self.current_progress_target * 100)}% | Nhấn SPACE cho random", True, (200, 200, 200))
        self.screen.blit(info, (350, 400))
    
    def demo_star_pop(self):
        """Demo star pop effect."""
        # Load or draw star
        star_size = 60
        
        for i, pos in enumerate(self.star_positions):
            # Draw star base
            star_surface = self.create_star_surface(star_size, COLOR_GOLD)
            
            # Apply pop effect if active
            if i < len(self.star_pops) and self.star_pops[i].is_active:
                star_surface = self.star_pops[i].apply_to_surface(star_surface)
                
                # Draw particles
                self.star_pops[i].draw(self.screen)
            
            # Blit star
            star_rect = star_surface.get_rect(center=pos)
            self.screen.blit(star_surface, star_rect)
        
        # Instructions
        info = self.font_small.render("Nhấn SPACE để trigger hiệu ứng sao", True, (200, 200, 200))
        self.screen.blit(info, (400, 450))
    
    def create_star_surface(self, size, color):
        """Tạo surface hình ngôi sao."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw simple star (5 points)
        import math
        center = size // 2
        outer_radius = size // 2 - 2
        inner_radius = size // 4
        
        points = []
        for i in range(10):
            angle = (i * 36 - 90) * math.pi / 180
            if i % 2 == 0:
                r = outer_radius
            else:
                r = inner_radius
            
            x = center + r * math.cos(angle)
            y = center + r * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(surface, color, points)
        
        return surface


if __name__ == "__main__":
    demo = EffectsDemo()
    demo.run()
