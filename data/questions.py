import random

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
        if min_val <= wrong <= max_val:
            options.add(wrong)

    # Nếu vẫn thiếu thì thêm bù
    while len(options) < 4:
        fake = random.randint(max(min_val, correct_answer - 30),
                              min(max_val, correct_answer + 30))
        if fake != correct_answer:
            options.add(fake)

    result = list(options)
    random.shuffle(result)
    return result


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
    questions = []
    templates = [
        ("({a} + {b}) × {c}", lambda a,b,c: (a+b)*c),
        ("{a} × ({b} + {c})", lambda a,b,c: a*(b+c)),
        ("({a} × {b}) + {c}", lambda a,b,c: a*b + c),
        ("{a} + ({b} × {c})", lambda a,b,c: a + b*c),
        ("({a} × {b}) − {c}", lambda a,b,c: a*b - c),
    ]
    for _ in range(num_questions):
        temp, func = random.choice(templates)
        a = random.randint(2, 12)
        b = random.randint(2, 10)
        c = random.randint(2, 9)
        if "−" in temp:
            while a*b <= c:
                a += 2
                b += 1
        ans = func(a, b, c)
        q = temp.format(a=a, b=b, c=c) + " = ?"
        questions.append({"question": q, "options": _create_options(ans, 0, 200), "answer": ans})
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
            a = random.randint(2, 15)
            x = random.randint(a + 5, a + 30)  # đảm bảo x > a
            b = x - a
            question_text = f"Tìm x: x − {a} = {b}"
        elif op == "×":
            b = x * a
            question_text = f"Tìm x: x × {a} = {b}"
        else:  # chia
            a = random.randint(2, 10)
            x = random.randint(6, 30) 
            b = x * a
            question_text = f"Tìm x: {b} : {a} = x"

        options = _create_options(x, min_val=1, max_val=50)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": x
        })
    return questions


# --- Level 5: Phân số cơ bản (rút gọn, quy đồng, cộng trừ) ---
from math import gcd
from fractions import Fraction

def _create_fraction_options(correct_frac, num_options=4):
    """
    Tạo các đáp án dạng phân số (dưới dạng chuỗi 'a/b') xung quanh đáp án đúng
    """
    num, den = correct_frac.numerator, correct_frac.denominator
    options = [correct_frac]

    while len(options) < num_options:
        # Tạo phân số sai gần đúng
        offset = random.randint(-5, 5)
        if offset == 0:
            continue
        wrong_num = num + offset
        wrong_den = den + random.randint(-3, 3)

        if wrong_den <= 1:
            wrong_den = den  # tránh mẫu âm hoặc bằng 1 sai

        wrong_g = gcd(wrong_num, wrong_den)
        wrong_frac = Fraction(wrong_num // wrong_g, wrong_den // wrong_g)

        # Tránh trùng
        if wrong_frac not in options and wrong_frac != correct_frac:
            options.append(wrong_frac)

    # Nếu chưa đủ thì thêm bừa vài cái sai
    while len(options) < num_options:
        fake = Fraction(random.randint(1, 20), random.randint(2, 20))
        if fake not in options:
            options.append(fake)

    random.shuffle(options)
    # Chuyển thành chuỗi
    return [f"{f.numerator}/{f.denominator}" for f in options]


# --- Level 5: Phân số cơ bản ---
def get_level_5_questions(num_questions=20):
    """Level 5: Phân số - rút gọn, cộng, trừ, nhân, chia"""
    questions = []
    for _ in range(num_questions):
        type_q = random.choice(["rutgon", "cong", "tru", "nhan", "chia"])

        if type_q == "rutgon":
            multiplier = random.randint(2, 10)
            num = random.randint(2, 15) * multiplier
            den = random.randint(2, 15) * multiplier
            frac = Fraction(num, den)
            question_text = f"Rút gọn phân số: {num}/{den}"
            correct_str = f"{frac.numerator}/{frac.denominator}"

        elif type_q == "cong":
            f1 = Fraction(random.randint(1, 12), random.randint(2, 12))
            f2 = Fraction(random.randint(1, 12), random.randint(2, 12))
            result = f1 + f2
            question_text = f"Tính: {f1.numerator}/{f1.denominator} + {f2.numerator}/{f2.denominator} = ?"
            correct_str = f"{result.numerator}/{result.denominator}"

        elif type_q == "tru":
            f1 = Fraction(random.randint(3, 15), random.randint(2, 10))
            f2 = Fraction(random.randint(1, 8), random.randint(2, 10))
            if f1 < f2:
                f1, f2 = f2, f1  # đảm bảo kết quả dương
            result = f1 - f2
            question_text = f"Tính: {f1.numerator}/{f1.denominator} - {f2.numerator}/{f2.denominator} = ?"
            correct_str = f"{result.numerator}/{result.denominator}"

        elif type_q == "nhan":
            f1 = Fraction(random.randint(1, 10), random.randint(2, 10))
            f2 = Fraction(random.randint(1, 10), random.randint(2, 10))
            result = f1 * f2
            question_text = f"Tính: {f1.numerator}/{f1.denominator} × {f2.numerator}/{f2.denominator} = ?"
            correct_str = f"{result.numerator}/{result.denominator}"

        else:  # chia
            f1 = Fraction(random.randint(2, 12), random.randint(2, 8))
            f2 = Fraction(random.randint(2, 10), random.randint(2, 10))
            # Tránh chia cho 0 và kết quả quá phức tạp
            result = f1 / f2
            if result.denominator > 20:  # nếu mẫu quá lớn thì bỏ
                result = Fraction(random.randint(1, 10), random.randint(2, 10))
            question_text = f"Tính: {f1.numerator}/{f1.denominator} : {f2.numerator}/{f2.denominator} = ?"
            correct_str = f"{result.numerator}/{result.denominator}"

        # Tạo đáp án sai dạng phân số (chuỗi)
        options = _create_fraction_options(Fraction(correct_str))

        questions.append({
            "question": question_text,
            "options": options,
            "answer": correct_str,   # dạng "3/4"
            "answer_index": options.index(correct_str)  # để kiểm tra sau
        })

    return questions

# --- Level 6: Tìm X nâng cao (phương trình, phân số, hỗn hợp) ---
def get_level_6_questions(num_questions=20):
    """Level 6: Tìm x nâng cao - phương trình bậc 1, có ngoặc, phân số (nguyên)"""
    questions = []
    for _ in range(num_questions):
        pattern = random.randint(1, 5)

        if pattern == 1:
            # Dạng: ax + b = c
            a = random.randint(2, 8)
            b = random.randint(1, 15)
            x = random.randint(3, 20)
            c = a * x + b
            question_text = f"Giải phương trình: {a}x + {b} = {c}"
            answer = x

        elif pattern == 2:
            # Dạng: a(x + b) = c
            a = random.randint(2, 6)
            b = random.randint(2, 10)
            x = random.randint(5, 18)
            c = a * (x + b)
            question_text = f"Giải phương trình: {a}(x + {b}) = {c}"
            answer = x

        elif pattern == 3:
            # Dạng: ax - b = c
            a = random.randint(2, 7)
            b = random.randint(5, 20)
            x = random.randint(6, 20)
            c = a * x - b
            question_text = f"Giải phương trình: {a}x − {b} = {c}"
            answer = x

        elif pattern == 4:
            # Dạng: x/a + b = c (x nguyên)
            a = random.randint(3, 8)
            b = random.randint(2, 12)
            x = random.randint(10, 50)
            # Đảm bảo x chia hết cho a
            x = ((x + a - 1) // a) * a  
            c = x // a + b
            question_text = f"Tìm x (số nguyên): x : {a} + {b} = {c}"
            answer = x

        else:  # pattern == 5: hỗn hợp 2 vế
            x = random.randint(8, 25)
            left_add = random.randint(3, 12)
            right_add = random.randint(5, 15)
            question_text = f"Tìm x: 2x + {left_add} = {2*x + left_add + right_add} và x − 5 = {x - 5}"
            answer = x

        options = _create_options(answer, min_val=1, max_val=80)
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    return questions

QUESTION_GENERATORS = {
        "LEVEL_1": get_level_1_questions,
        "LEVEL_2": get_level_2_questions,
        "LEVEL_3": get_level_3_questions,
        "LEVEL_4": get_level_4_questions,
        "LEVEL_5": get_level_5_questions,
        "LEVEL_6": get_level_6_questions,
    }

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