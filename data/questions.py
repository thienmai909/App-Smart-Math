import random

def _create_options(correct_answer, min_val, max_val):
    """
    Hàm nội bộ: Tạo 3 đáp án sai ngẫu nhiên xung quanh đáp án đúng.
    Đảm bảo các đáp án sai không trùng nhau và không trùng đáp án đúng.
    """
    options = [correct_answer]
    while len(options) < 4:
        wrong_answer = random.randint(max(min_val, correct_answer - 12),
                                      min(max_val, correct_answer + 12))
        if wrong_answer not in options:
            options.append(wrong_answer)
    random.shuffle(options)
    return options


# --- Level 1: Phép Cộng - Trừ (1-20) ---
def get_level_1_questions(num_questions=20):
    """Tạo câu hỏi Level 1: Phép cộng - trừ (phạm vi 1-20)"""
    questions = []
    for _ in range(num_questions):
        a = random.randint(1, 20)
        b = random.randint(1, 20)

        if random.choice([True, False]):
            # Phép cộng
            question_text = f"{a} + {b} = ?"
            correct_answer = a + b
            options = _create_options(correct_answer, min_val=0, max_val=50)
        else:
            # Phép trừ (đảm bảo kết quả không âm)
            if a < b:
                a, b = b, a
            question_text = f"{a} - {b} = ?"
            correct_answer = a - b
            options = _create_options(correct_answer, min_val=0, max_val=20)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer
        })
    return questions


# --- Level 2: Phép Nhân - Chia (bảng cửu chương 2-9) ---
def get_level_2_questions(num_questions=20):
    """Tạo câu hỏi Level 2: Phép nhân - chia (bảng cửu chương 2-9)"""
    questions = []
    for _ in range(num_questions):
        a = random.randint(2, 9)
        b = random.randint(2, 9)

        if random.choice([True, False]):
            # Phép nhân
            question_text = f"{a} × {b} = ?"
            correct_answer = a * b
            options = _create_options(correct_answer, min_val=4, max_val=81)
        else:
            # Phép chia (chia hết)
            product = a * b
            question_text = f"{product} : {a} = ?"
            correct_answer = b
            options = _create_options(correct_answer, min_val=2, max_val=9)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer
        })
    return questions


# --- Level 3: Phép tính hỗn hợp (cộng trừ nhân chia có ngoặc) ---
def get_level_3_questions(num_questions=20):
    """Level 3: Phép tính hỗn hợp, có ngoặc đơn, ưu tiên nhân chia trước"""
    questions = []
    for _ in range(num_questions):
        # Tạo 3 số và 2 phép tính
        nums = [random.randint(2, 12) for _ in range(3)]
        ops = random.choices(["+", "-", "×", ":"], k=2)

        # Tạo biểu thức có ngoặc để thay đổi thứ tự thực hiện
        pattern = random.choice([
            f"({nums[0]} {ops[0]} {nums[1]}) {ops[1]} {nums[2]}",
            f"{nums[0]} {ops[0]} ({nums[1]} {ops[1]} {nums[2]})",
            f"{nums[0]} {ops[0]} {nums[1]} {ops[1]} {nums[2]}"
        ])

        # Tính toán đáp án đúng (ưu tiên × và : trước + -)
        def calc(expr):
            try:
                return eval(expr.replace("×", "*").replace(":", "/"))
            except:
                return 0

        correct_answer = int(calc(pattern)) if calc(pattern).is_integer() else round(calc(pattern), 1)

        # Đảm bảo đáp án là số nguyên hợp lý
        if not isinstance(correct_answer, int) or correct_answer < 0 or correct_answer > 100:
            # Tạo lại nếu quá phức tạp
            i = random.randint(5, 30)
            question_text = f"{i} + {random.randint(1, 20)} = ?"
            correct_answer = i + random.randint(1, 20)
        else:
            question_text = pattern.replace("×", "×").replace(":", ":") + " = ?"

        options = _create_options(int(correct_answer), min_val=0, max_val=150)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": int(correct_answer)
        })
    return questions


# --- Level 4: Tìm X cơ bản (x ± a = b, x × a = b, x : a = b) ---
def get_level_4_questions(num_questions=20):
    """Tạo câu hỏi Level 4: Tìm X cơ bản"""
    questions = []
    for _ in range(num_questions):
        op = random.choice(["+", "-", "×", ":"])
        a = random.randint(2, 15)
        x = random.randint(5, 30)  # Giá trị thực của x

        if op == "+":
            b = x + a
            question_text = f"Tìm x: x + {a} = {b}"
        elif op == "-":
            b = x - a if x > a else a - x
            if x <= a:
                x, a = a + random.randint(5, 15), x
                b = x - a
            question_text = f"Tìm x: x - {a} = {b}"
        elif op == "×":
            b = x * a
            question_text = f"Tìm x: x × {a} = {b}"
        else:  # chia
            b = x * a
            question_text = f"Tìm x: x : {a} = {b // a}"
            x = b // a

        options = _create_options(x, min_val=1, max_val=50)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": x
        })
    return questions


# --- Level 5: Phân số cơ bản (rút gọn, quy đồng, cộng trừ) ---
def get_level_5_questions(num_questions=20):
    """Level 5: Phân số - rút gọn, cộng, trừ, nhân, chia"""
    questions = []
    for _ in range(num_questions):
        type_q = random.choice(["rutgon", "cong", "tru", "nhan", "chia"])

        if type_q == "rutgon":
            # Phân số cần rút gọn
            d = random.randint(2, 10)
            n = random.randint(2, 20) * d
            question_text = f"Rút gọn phân số: {n}/{n + d * random.randint(1, 5)}"
            correct_answer = f"{d}/{d + random.randint(1, 5)}"  # giả sử
            # Tính thật
            from math import gcd
            num, den = n, n + d * random.randint(1, 5)
            g = gcd(num, den)
            correct_answer = f"{num//g}/{den//g}"

        elif type_q in ["cong", "tru"]:
            n1, d1 = random.randint(1, 10), random.randint(2, 10)
            n2, d2 = random.randint(1, 10), random.randint(2, 10)
            if type_q == "cong":
                question_text = f"Tính: {n1}/{d1} + {n2}/{d2} = ?"
                # Quy đồng mẫu
                common = d1 * d2
                num = n1 * d2 + n2 * d1
            else:
                question_text = f"Tính: {n1}/{d1} - {n2}/{d2} = ?"
                common = d1 * d2
                num = n1 * d2 - n2 * d1
                if num < 0:
                    num, n1, n2 = -num, n2, n1
                    question_text = f"Tính: {n1}/{d1} - {n2}/{d2} = ?"
            from math import gcd
            g = gcd(num, common)
            correct_answer = f"{num//g}/{common//g}" if g > 1 else f"{num}/{common}"

        elif type_q == "nhan":
            n1, d1 = random.randint(1, 10), random.randint(2, 10)
            n2, d2 = random.randint(1, 10), random.randint(2, 10)
            question_text = f"Tính: {n1}/{d1} × {n2}/{d2} = ?"
            from math import gcd
            g1 = gcd(n1, d2)
            g2 = gcd(n2, d1)
            correct_answer = f"{(n1//g1)*(n2//g2)}/{(d1//g2)*(d2//g1)}"

        else:  # chia
            n1, d1 = random.randint(1, 10), random.randint(2, 10)
            n2, d2 = random.randint(1, 10), random.randint(2, 10)
            question_text = f"Tính: {n1}/{d1} : {n2}/{d2} = ?"
            correct_answer = f"{n1*d2}/{d1*n2}"
            from math import gcd
            g = gcd(n1*d2, d1*n2)
            correct_answer = f"{(n1*d2)//g}/{(d1*n2)//g}"

        # Vì đáp án là chuỗi phân số, ta sẽ chuyển thành số để tạo options
        num_val = eval(correct_answer.replace("/", "*1.0/"))
        options = _create_options(int(num_val * 10), min_val=1, max_val=200)
        # Nhưng vẫn giữ đáp án dạng phân số đẹp
        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer,
            "note": "Phân số (đáp án dạng chuỗi)"
        })
    return questions


# --- Level 6: Tìm X nâng cao (phương trình, phân số, hỗn hợp) ---
def get_level_6_questions(num_questions=20):
    """Level 6: Tìm X nâng cao - phương trình bậc nhất, phân số, nhiều bước"""
    questions = []
    for _ in range(num_questions):
        pattern = random.choice([
            "phuongtrinh", "phuongtrinh2", "phanso_x", "honhop"
        ])

        if pattern == "phuongtrinh":
            a = random.randint(2, 10)
            b = random.randint(1, 20)
            c = random.randint(5, 30)
            x = random.randint(5, 20)
            left = a * x + b
            question_text = f"Giải phương trình: {a}x + {b} = {left + c}"
            correct_answer = x

        elif pattern == "phuongtrinh2":
            a = random.randint(2, 8)
            b = random.randint(10, 30)
            x = random.randint(3, 15)
            question_text = f"Tìm x: {a}(x + {x//2}) = {a*(x + x//2) + b}"
            correct_answer = x

        elif pattern == "phanso_x":
            d = random.randint(3, 8)
            x = random.randint(5, 20)
            question_text = f"Tìm x (nguyên): x/{d} + {x//3} = {x//d + x//3 + random.randint(5, 15)}"
            correct_answer = x

        else:  # hỗn hợp
            x = random.randint(10, 25)
            question_text = f"Tìm x: 3x - 7 = {3*x - 7} và 5 + x = {5 + x + random.randint(3, 10)}"
            correct_answer = x

        options = _create_options(correct_answer, min_val=1, max_val=60)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_answer
        })
    return questions


# ============================== TEST KHI CHẠY TRỰC TIẾP ==============================
if __name__ == "__main__":
    print("="*60)
    print("TEST TẠO CÂU HỎI - TOÁN HỌC 6 LEVEL")
    print("="*60)

    levels = [
        ("Level 1 - Cộng Trừ", get_level_1_questions),
        ("Level 2 - Nhân Chia", get_level_2_questions),
        ("Level 3 - Hỗn hợp có ngoặc", get_level_3_questions),
        ("Level 4 - Tìm X cơ bản", get_level_4_questions),
        ("Level 5 - Phân số", get_level_5_questions),
        ("Level 6 - Tìm X nâng cao", get_level_6_questions),
    ]

    for name, func in levels:
        print(f"\n{name} (3 câu mẫu):")
        print("-" * 50)
        sample = func(3)
        for i, q in enumerate(sample, 1):
            print(f"{i}. {q['question']}")
            print(f"   Đáp án đúng: {q['answer']}")
            print(f"   Lựa chọn: {q['options']}")
            print()
        print("..." + "═"*50)