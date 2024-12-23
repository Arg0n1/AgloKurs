import time
import matplotlib.pyplot as plt
import numpy as np

def direct_search(string, substring):
    n = len(string)
    m = len(substring)
    result = []
    for i in range(n - m + 1):
        if string[i:i + m] == substring:
            result.append(i)
    return result if result else -1

def direct_search_time(string, substring, length):
    truncated_text = string[:length]
    start = time.time()
    direct_search(truncated_text, substring)
    end = time.time()
    return end - start

def pi_func_create(substring):
    m = len(substring)
    pi_func = [0] * m
    for i in range(1, m):
        j = pi_func[i - 1]
        while j > 0 and substring[i] != substring[j]:
            j = pi_func[j - 1]
        if substring[i] == substring[j]:
            j += 1
        pi_func[i] = j
    return pi_func

def kmp_search(string, substring):
    pi_func = pi_func_create(substring)
    j = 0
    result = []
    for i in range(0, len(string)):
        while j > 0 and string[i] != substring[j]:
            j = pi_func[j - 1]
        if string[i] == substring[j]:
            j += 1
        if j == len(substring):
            result.append(i - j + 1)
            j = pi_func[j - 1]
    return result if result else -1

def kmp_time(string, substring, length):
    truncated_text = string[:length]
    start = time.time()
    kmp_search(truncated_text, substring)
    end = time.time()
    return end - start

def offset_table(substring, start_index, end_index):
    alphabet_size = end_index - start_index + 1
    alphabet_table = [len(substring)] * alphabet_size
    for i in range(len(substring) - 1):
        char_index = ord(substring[i]) - start_index
        if 0 <= char_index < alphabet_size:
            alphabet_table[char_index] = len(substring) - i - 1
    return alphabet_table

def bmh_search(string, substring):
    if len(substring) > len(string):
        return -1
    start_index = ord(" ")
    end_index = ord("~")
    alphabet_table = offset_table(substring, start_index, end_index)
    i = len(substring) - 1
    result = []
    while i < len(string):
        if string[i - len(substring) + 1:i + 1] == substring:
            result.append(i - len(substring) + 1)
            i += 1
            continue
        char_index = ord(string[i]) - start_index
        shift = alphabet_table[char_index] if 0 <= char_index < len(alphabet_table) else len(substring)
        i += shift
    return result if result else -1

def bmh_time(string, substring, length):
    truncated_text = string[:length]
    start = time.time()
    bmh_search(truncated_text, substring)
    end = time.time()
    return end - start

def gorner_scheme(text):
    result = 0
    base = 52
    for i in text:
        result = result * base + ord(i)
    return result

def calculate_hash(string):
        q = 65713
        return gorner_scheme(string) % q

def rk_search(string, substring):
    base = 52
    q = 65713
    m = len(substring)
    n = len(string)
    if m > n:
        return -1
    pattern_hash = calculate_hash(substring)
    text_hash = calculate_hash(string[:m])
    result = []
    for i in range(n - m + 1):
        if text_hash == pattern_hash:
            if string[i:i + m] == substring:
                result.append(i)
        if i + m < n:
            text_hash = ((text_hash - ord(string[i]) * base ** (m - 1)) * base + ord(string[i + m])) % q
            text_hash = (text_hash + q) % q
    return result if result else -1

def rk_time(string, substring, length):
    truncated_text = string[:length]
    start = time.time()
    rk_search(truncated_text, substring)
    end = time.time()
    return end - start

file_path = "DNA.txt"
with open(file_path, "r") as file:
    text = file.read()

pattern = "ACTG"

search = {
    "Прямой поиск": direct_search_time,
    "Кнут-Моррис-Пратт": kmp_time,
    "Бойер-Мур-Хорспул": bmh_time,
    "Рабин-Карп": rk_time
}
all_results = {}

for alg_name, alg_code in search.items():
    print(f"Запуск алгоритма: {alg_name}")
    lengths = []
    times = []
    for length in range(300, 150000, 1000):
        execution_time = alg_code(text, pattern, length)
        lengths.append(length)
        times.append(execution_time)
        print(f"Время выполнения {alg_name} для текста длиной {length} символов: {execution_time} секунд")
    all_results[alg_name] = (lengths, times)

plt.figure(figsize=(12, 8))
for alg_name, (lengths, times) in all_results.items():
    coeffs = np.polyfit(lengths, times, 2)
    fitted_times = np.polyval(coeffs, lengths)
    plt.plot(lengths, times, marker='o', ms=2, linestyle=' ', label=f"{alg_name}")
    plt.plot(lengths, fitted_times, linestyle='-', linewidth=4, label=f"{alg_name}")
    poly_eq = f"{alg_name}: {coeffs[0]:.2e} * x² + {coeffs[1]:.2e} * x + {coeffs[2]:.2e}"
    if alg_name == list(all_results.keys())[0]:
        plt.figtext(0.1, 0.17,
                    poly_eq,
                    ha='left', fontsize=10, color='black')
    elif alg_name == list(all_results.keys())[1]:
        plt.figtext(0.1, 0.12,
                    poly_eq,
                    ha='left', fontsize=10, color='black')
    elif alg_name == list(all_results.keys())[2]:
        plt.figtext(0.1, 0.07,
                    poly_eq,
                    ha='left', fontsize=10, color='black')
    elif alg_name == list(all_results.keys())[3]:
        plt.figtext(0.1, 0.02,
                    poly_eq,
                    ha='left', fontsize=10, color='black')
plt.title(f"Подстрока - {len(pattern)} символа")
plt.xlabel("Количество символов")
plt.ylabel("Секунды")
plt.legend()
plt.subplots_adjust(bottom=0.3)
plt.grid(True)
plt.show()

print(direct_search(text, pattern))
print(kmp_search(text, pattern))
print(bmh_search(text, pattern))
print(rk_search(text, pattern))
print(offset_table(pattern, start_index=ord(" "), end_index=ord("~")))