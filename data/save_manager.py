# data/save_manager.py
import json
import os

# Tạo thư mục 'data' nếu chưa có
os.makedirs('data', exist_ok=True)

SAVE_FILE = "data/save.json"

def load_game_data():
    """Tải dữ liệu game (highscores và stars) từ tệp JSON."""
    if not os.path.exists(SAVE_FILE):
        # Mặc định: 6 level, điểm cao 0, sao 0
        return {"highscores": [0]*6, "stars": [0]*6} 
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Đảm bảo cấu trúc data luôn đúng và đủ 6 level
            if 'highscores' not in data or len(data['highscores']) < 6:
                 return {"highscores": [0]*6, "stars": [0]*6}
            return data
    except Exception as e:
        print(f"Lỗi tải dữ liệu save: {e}. Sử dụng dữ liệu mặc định.")
        return {"highscores": [0]*6, "stars": [0]*6}

def save_game_data(data):
    """Lưu dữ liệu game vào tệp JSON."""
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Lỗi lưu dữ liệu save: {e}")