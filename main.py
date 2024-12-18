import time
import matplotlib.pyplot as plt
import numpy as np

def direct_search(text, pattern):
    n = len(text)
    m = len(pattern)

    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            return i
    return -1

def direct_search_time(text, pattern, length):
    truncated_text = text[:length]
    start = time.time()
    direct_search(truncated_text,pattern)
    end = time.time()
    return end - start

def rabin_karp(text, pattern, d, q):
    n = len(text)
    m = len(pattern)
    if m > n:
        return -1

    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % q
        text_hash = (d * text_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if text_hash < 0:
                text_hash += q

    return -1

def rabin_karp_time(text, pattern,length, d=256, q=101):
    truncated_text = text[:length]
    start = time.time()
    rabin_karp(truncated_text, pattern, d=d, q=q)
    end = time.time()
    return end - start

def boyer_moore(text, pattern):
    def build_bad_char_table(pattern):
        table = {}
        m = len(pattern)
        for i in range(m):
            table[pattern[i]] = m - i - 1
        return table

    def build_good_suffix_table(pattern):
        m = len(pattern)
        good_suffix = [m] * (m + 1)
        border_position = [0] * (m + 1)

        i = m
        j = m + 1
        border_position[i] = j
        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if good_suffix[j] == m:
                    good_suffix[j] = j - i
                j = border_position[j]
            i -= 1
            j -= 1
            border_position[i] = j

        j = border_position[0]
        for i in range(m + 1):
            if good_suffix[i] == m:
                good_suffix[i] = j
            if i == j:
                j = border_position[j]
        return good_suffix

    m = len(pattern)
    n = len(text)
    bad_char_table = build_bad_char_table(pattern)
    good_suffix_table = build_good_suffix_table(pattern)

    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j == -1:
            return i
        else:
            bad_char_shift = bad_char_table.get(text[i + j], m)
            good_suffix_shift = good_suffix_table[j + 1]
            shift = max(bad_char_shift, good_suffix_shift)
            i += shift
    return -1

def boyer_moore_time(text, pattern, length):
    truncated_text = text[:length]
    start = time.time()
    boyer_moore(truncated_text, pattern)
    end = time.time()
    return end - start

def kmp_search(text, pattern):
    def compute_lps(pattern):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    i = 0
    j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


def kmp_search_time(text, pattern, length):
    truncated_text = text[:length]
    start = time.time()
    kmp_search(truncated_text, pattern)
    end = time.time()
    return end - start

file_path = "Alice.txt"
with open(file_path, "r") as file:
    text = file.read()

pattern = "Ultimately this exercise challenges us to strike a balance between brevity and detail pushing us to create a thoughtful and polished text that is not only the required length but also impactful cohesive and carefully crafted from start to finish"

search = {
    "Прямой поиск": direct_search_time,
    "Рабин-Карп": rabin_karp_time,
    "Бойер-Мур": boyer_moore_time,
    "Кнут-Моррис-Пратт": kmp_search_time
}
all_results = {}

for alg_name, alg_code in search.items():
    print(f"Запуск алгоритма: {alg_name}")
    lengths = []
    times = []
    for length in range(300, 1001, 2):
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

