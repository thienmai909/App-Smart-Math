"""
Animation Utils - Các hàm tiện ích cho animation
================================================
Cung cấp easing functions và interpolation cho hiệu ứng mượt mà.
"""

import math


# ============================================================================
# EASING FUNCTIONS
# ============================================================================
# Reference: https://easings.net/

def linear(t):
    """
    Linear easing - không có gia tốc.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value từ 0.0 đến 1.0
    """
    return t


def ease_in_out(t):
    """
    Ease In-Out (Smoothstep) - chậm ở đầu và cuối, nhanh ở giữa.
    Rất phù hợp cho transitions mượt mà.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value
    """
    return t * t * (3.0 - 2.0 * t)


def ease_in_quad(t):
    """
    Ease In Quadratic - bắt đầu chậm, tăng tốc dần.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value
    """
    return t * t


def ease_out_quad(t):
    """
    Ease Out Quadratic - bắt đầu nhanh, giảm tốc dần.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value
    """
    return t * (2.0 - t)


def ease_in_cubic(t):
    """
    Ease In Cubic - tăng tốc mạnh hơn quadratic.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value
    """
    return t * t * t


def ease_out_cubic(t):
    """
    Ease Out Cubic - giảm tốc mạnh hơn quadratic.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value
    """
    t -= 1.0
    return t * t * t + 1.0


def ease_out_bounce(t):
    """
    Ease Out Bounce - hiệu ứng nảy (bounce) ở cuối.
    Rất phù hợp cho button click, star pop.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        float: Eased value (có thể > 1.0 khi bounce)
    """
    if t < 1.0 / 2.75:
        return 7.5625 * t * t
    elif t < 2.0 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375


def ease_out_elastic(t, amplitude=1.0, period=0.3):
    """
    Ease Out Elastic - hiệu ứng đàn hồi (spring/elastic) ở cuối.
    Rất phù hợp cho star pop, scale animations.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
        amplitude (float): Biên độ dao động
        period (float): Chu kỳ dao động
    
    Returns:
        float: Eased value (có thể > 1.0 hoặc < 0.0 khi oscillate)
    """
    if t == 0.0:
        return 0.0
    if t == 1.0:
        return 1.0
    
    s = period / 4.0
    return amplitude * math.pow(2.0, -10.0 * t) * math.sin((t - s) * (2.0 * math.pi) / period) + 1.0


def ease_in_back(t, overshoot=1.70158):
    """
    Ease In Back - "lùi lại" trước khi tiến.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
        overshoot (float): Mức độ lùi lại
    
    Returns:
        float: Eased value
    """
    return t * t * ((overshoot + 1.0) * t - overshoot)


def ease_out_back(t, overshoot=1.70158):
    """
    Ease Out Back - "vượt qua" mục tiêu rồi quay lại.
    
    Args:
        t (float): Progress từ 0.0 đến 1.0
        overshoot (float): Mức độ vượt qua
    
    Returns:
        float: Eased value
    """
    t -= 1.0
    return t * t * ((overshoot + 1.0) * t + overshoot) + 1.0


# ============================================================================
# INTERPOLATION FUNCTIONS
# ============================================================================

def lerp(a, b, t):
    """
    Linear Interpolation - nội suy tuyến tính giữa 2 giá trị.
    
    Args:
        a (float): Giá trị bắt đầu
        b (float): Giá trị kết thúc
        t (float): Progress từ 0.0 (trả về a) đến 1.0 (trả về b)
    
    Returns:
        float: Giá trị nội suy
    
    Examples:
        >>> lerp(0, 100, 0.5)
        50.0
        >>> lerp(10, 20, 0.25)
        12.5
    """
    return a + (b - a) * t


def lerp_clamped(a, b, t):
    """
    Linear Interpolation với clamp - đảm bảo t trong [0, 1].
    
    Args:
        a (float): Giá trị bắt đầu
        b (float): Giá trị kết thúc
        t (float): Progress
    
    Returns:
        float: Giá trị nội suy
    """
    t = max(0.0, min(1.0, t))
    return lerp(a, b, t)


def color_lerp(color1, color2, t):
    """
    Nội suy giữa 2 màu RGB/RGBA.
    
    Args:
        color1 (tuple): Màu bắt đầu (R, G, B) hoặc (R, G, B, A)
        color2 (tuple): Màu kết thúc (R, G, B) hoặc (R, G, B, A)
        t (float): Progress từ 0.0 đến 1.0
    
    Returns:
        tuple: Màu nội suy
    
    Examples:
        >>> color_lerp((255, 0, 0), (0, 0, 255), 0.5)
        (127, 0, 127)
    """
    # Clamp t
    t = max(0.0, min(1.0, t))
    
    # Interpolate từng channel
    r = int(lerp(color1[0], color2[0], t))
    g = int(lerp(color1[1], color2[1], t))
    b = int(lerp(color1[2], color2[2], t))
    
    # Nếu có alpha channel
    if len(color1) > 3 and len(color2) > 3:
        a = int(lerp(color1[3], color2[3], t))
        return (r, g, b, a)
    
    return (r, g, b)


def smooth_damp(current, target, current_velocity, smooth_time, dt, max_speed=float('inf')):
    """
    Smooth damp - di chuyển mượt từ current đến target với velocity.
    Tương tự Unity's Mathf.SmoothDamp.
    
    Args:
        current (float): Giá trị hiện tại
        target (float): Giá trị mục tiêu
        current_velocity (float): Vận tốc hiện tại (tham chiếu)
        smooth_time (float): Thời gian ước tính đến target
        dt (float): Delta time
        max_speed (float): Vận tốc tối đa
    
    Returns:
        tuple: (new_value, new_velocity)
    """
    smooth_time = max(0.0001, smooth_time)
    omega = 2.0 / smooth_time
    
    x = omega * dt
    exp = 1.0 / (1.0 + x + 0.48 * x * x + 0.235 * x * x * x)
    
    change = current - target
    original_to = target
    
    max_change = max_speed * smooth_time
    change = max(-max_change, min(change, max_change))
    target = current - change
    
    temp = (current_velocity + omega * change) * dt
    current_velocity = (current_velocity - omega * temp) * exp
    output = target + (change + temp) * exp
    
    # Prevent overshooting
    if (original_to - current > 0.0) == (output > original_to):
        output = original_to
        current_velocity = (output - original_to) / dt
    
    return output, current_velocity


def clamp(value, min_val, max_val):
    """
    Giới hạn giá trị trong khoảng [min_val, max_val].
    
    Args:
        value (float): Giá trị cần clamp
        min_val (float): Giá trị nhỏ nhất
        max_val (float): Giá trị lớn nhất
    
    Returns:
        float: Giá trị đã clamp
    """
    return max(min_val, min(value, max_val))
