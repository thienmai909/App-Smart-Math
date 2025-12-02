import json
import os

# Tên file lưu trữ nằm cùng thư mục data/
SAVE_FILE = os.path.join(os.path.dirname(__file__), "save.json")

def load_game_data():
    """Tải dữ liệu điểm cao và sao đã lưu. Nếu không có file, trả về mặc định."""
    # Mặc định cho 6 level (highscores và stars)
    default_data = {"highscores": [0] * 6, "stars": [0] * 6}
    
    if not os.path.exists(SAVE_FILE):
        return default_data
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            
            # Đảm bảo cấu trúc dữ liệu luôn có 6 phần tử cho 6 level
            if len(data.get('highscores', [])) < 6:
                data['highscores'] = data.get('highscores', []) + [0] * (6 - len(data.get('highscores', [])))
            if len(data.get('stars', [])) < 6:
                data['stars'] = data.get('stars', []) + [0] * (6 - len(data.get('stars', [])))
                
            return data
    except Exception as e:
        print(f"Lỗi khi đọc file save.json: {e}. Trả về dữ liệu mặc định.")
        return default_data

def save_game_data(data):
    """Lưu dữ liệu điểm cao và sao."""
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Lỗi khi ghi file save.json: {e}")