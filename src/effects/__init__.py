"""
Smart Math - Effects Module
============================
Hệ thống hiệu ứng modular cho game học toán.

Module này cung cấp các hiệu ứng animation cho:
- Transitions (chuyển màn hình)
- Button effects (hiệu ứng nút bấm)
- Progress effects (thanh tiến độ và sao)
- Answer effects (hiệu ứng trả lời)
- Particle systems (pháo hoa, confetti)
"""

from .base_effect import BaseEffect
from .animation_utils import ease_in_out, ease_out_bounce, ease_out_elastic, lerp, color_lerp
from .transitions import FadeTransition, SlideTransition, ZoomTransition
from .button_effects import HoverEffect, ClickRippleEffect, GlowEffect
from .progress_effects import ProgressBarFillEffect, StarPopEffect
from .effect_manager import EffectManager, init_effect_manager, get_effect_manager
from .gif_animation import GifAnimation

__all__ = [
    # Base
    'BaseEffect',
    
    # Utils
    'ease_in_out', 
    'ease_out_bounce', 
    'ease_out_elastic',
    'lerp', 
    'color_lerp',
    
    # Transitions
    'FadeTransition', 
    'SlideTransition', 
    'ZoomTransition',
    
    # Button Effects
    'HoverEffect', 
    'ClickRippleEffect', 
    'GlowEffect',
    
    # Progress Effects
    'ProgressBarFillEffect', 
    'StarPopEffect',
    
    # Effect Manager
    'EffectManager',
    'init_effect_manager',
    'get_effect_manager',
    
    # GIF Animation
    'GifAnimation',
]

__version__ = '1.0.0'
__author__ = 'Smart Math Team'
