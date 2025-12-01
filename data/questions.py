# data/questions.py
import random
import math

def _create_options(correct_answer, min_val=0, max_val=100):
    """ĐẢM BẢO đáp án đúng luôn nằm trong 4 lựa chọn"""
    correct_answer = int(correct_answer)
    options = set([correct_answer])

    # Tạo đáp án sai gần đúng
    while len(options) < 4:
        offset = random.randint(-15, 15)
        if offset == 0:
            continue
        wrong = correct_answer + offset
        if min_val <= wrong <= max_val and wrong != correct_answer:
            options.add(wrong)

    # Nếu vẫn thiếu thì thêm bù
    while len(options) < 4:
        # Chọn số giả ngẫu nhiên trong khoảng chấp nhận được
        fake = random.randint(max(min_val, correct_answer - 30),
                              min(max_val, correct_answer + 30))
        if fake != correct_answer:
            options.add(fake)

    result = list(options)
    random.shuffle(result)
    return result


# --- Level 1: Phép Cộng - Trừ (1-20) ---
def get_level_1_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        
        op = random.choice(['+', '-'])
        
        if op == '+':
            question_text = f"{a} + {b} = ?"
            answer = a + b
        else: # Phép trừ đảm bảo kết quả không âm
            if a < b: a, b = b, a # Hoán đổi
            question_text = f"{a} - {b} = ?"
            answer = a - b
            
        options = _create_options(answer, min_val=0, max_val=40)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions


# --- Level 2: Phép Nhân - Chia (2-9) ---
def get_level_2_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        
        op = random.choice(['*', '/'])
        
        if op == '*':
            question_text = f"{a} x {b} = ?"
            answer = a * b
        else: # Phép chia
            answer = a
            a = a * b # Tạo số chia hết
            question_text = f"{a} : {b} = ?"
            
        options = _create_options(answer, min_val=1, max_val=81)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions

# --- Level 3: Hỗn hợp có ngoặc (Nâng cao) ---
def get_level_3_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        pattern = random.randint(1, 3)
        
        if pattern == 1: # (a + b) x c
            a = random.randint(2, 8)
            b = random.randint(2, 8)
            c = random.randint(2, 5)
            question_text = f"({a} + {b}) x {c} = ?"
            answer = (a + b) * c
        elif pattern == 2: # a x (b - c)
            a = random.randint(2, 5)
            b = random.randint(10, 20)
            c = random.randint(2, 8)
            question_text = f"{a} x ({b} - {c}) = ?"
            answer = a * (b - c)
        else: # (a - b) : c (đảm bảo chia hết)
            c = random.randint(2, 5)
            res = random.randint(5, 15)
            diff = res * c
            b = random.randint(2, 10)
            a = diff + b
            question_text = f"({a} - {b}) : {c} = ?"
            answer = res
            
        options = _create_options(answer, min_val=1, max_val=100)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions

# --- Level 4: Tìm X cơ bản (Cộng/Trừ) ---
def get_level_4_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        pattern = random.randint(1, 3)
        
        if pattern == 1: # x + a = b
            x = random.randint(10, 50)
            a = random.randint(5, 20)
            b = x + a
            question_text = f"Tìm x: x + {a} = {b}"
            answer = x
        elif pattern == 2: # a - x = b
            a = random.randint(30, 80)
            x = random.randint(5, 30)
            b = a - x
            question_text = f"Tìm x: {a} - x = {b}"
            answer = x
        else: # x - a = b
            a = random.randint(5, 20)
            b = random.randint(30, 50)
            x = a + b
            question_text = f"Tìm x: x - {a} = {b}"
            answer = x
            
        options = _create_options(answer, min_val=1, max_val=80)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions

# --- Level 5: Phân số cơ bản (Đổi sang số nguyên) ---
def get_level_5_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        # Ví dụ đơn giản: Đổi phân số thành số nguyên (tử chia hết cho mẫu)
        
        # 3/5 của 100
        mau = random.choice([2, 4, 5, 10])
        tu = random.randint(1, mau - 1)
        
        # Số bị chia (đảm bảo chia hết)
        whole = random.randint(1, 10) * mau 
        
        question_text = f"{tu}/{mau} của {whole} là bao nhiêu?"
        answer = int((whole / mau) * tu)
            
        options = _create_options(answer, min_val=1, max_val=100)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions

# --- Level 6: Tìm X nâng cao (Nhân/Chia) ---
def get_level_6_questions(num_questions=20):
    questions = []
    for _ in range(num_questions):
        pattern = random.randint(1, 2)
        
        if pattern == 1: # a * x = b
            a = random.randint(2, 9)
            x = random.randint(5, 15)
            b = a * x
            question_text = f"Tìm x: {a} x x = {b}"
            answer = x
        else: # x : a = b
            a = random.randint(2, 8)
            b = random.randint(5, 15)
            x = a * b
            question_text = f"Tìm x: x : {a} = {b}"
            answer = x
            
        options = _create_options(answer, min_val=1, max_val=80)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions

# ============================== TEST KHI CHẠY TRỰC TIẾP (Optional) ==============================
# if __name__ == "__main__": ...