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

def pi_func_create(pattern):
    m = len(pattern)
    pi_func = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi_func[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi_func[i] = j
    return pi_func

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    pi_func = pi_func_create(pattern)
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi_func[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    return -1

def kmp_time(text, pattern, length):
    truncated_text = text[:length]
    start = time.time()
    kmp_search(truncated_text, pattern)
    end = time.time()
    return end - start


def offset_table(pattern):
    m = len(pattern)
    S = set()
    dictionary = {}
    for i in range(m-2, -1, -1):
        if pattern[i] not in S:
            dictionary[pattern[i]] = m - i - 1
            S.add(pattern[i])

    if pattern[m-1] not in S:
        dictionary[pattern[m-1]] = m

    dictionary['*'] = m

    return dictionary

def bmh_search(text, pattern):
    n = len(text)
    m = len(pattern)
    dictionary = offset_table(pattern)
    if n >= m:
        i = m - 1

        while i < n:
            k = 0
            for j in range(m-1, -1, -1):
                if text[i - k] != pattern[j]:
                    if j == m - 1:
                        off = dictionary[text[i]] if dictionary.get(text[i], False) else dictionary['*']
                    else:
                        off = dictionary[pattern[j]]

                    i += off
                    break
                k += 1
            if j == 0:
                return i-k+1
        else:
            return -1
    else:
        return -1

def bmh_time(text, pattern, length):
    truncated_text = text[:length]
    start = time.time()
    bmh_search(truncated_text, pattern)
    end = time.time()
    return end - start

def gorner_scheme(text):
    result = 0
    base = 31
    for i in text:
        result = result * base + ord(i)
    return result

def calculate_hash(text):
        q = 2147483647
        return gorner_scheme(text) % q

def rk_search(text, pattern):
    base = 31
    q = 2147483647
    m = len(pattern)
    n = len(text)
    if m > n:
        return -1
    pattern_hash = calculate_hash(pattern)
    text_hash = calculate_hash(text[:m])
    high_order = pow(base, m - 1, q)
    for i in range(n - m + 1):
        if text_hash == pattern_hash:
            if text[i:i + m] == pattern:
                return i
        if i + m < n:
            text_hash = (text_hash - ord(text[i]) * high_order) * base + ord(text[i + m])
            text_hash %= q
    return -1

def rk_time(text, pattern,length):
    truncated_text = text[:length]
    start = time.time()
    rk_search(truncated_text, pattern)
    end = time.time()
    return end - start

file_path = "Alice.txt"
with open(file_path, "r") as file:
    text = file.read()

pattern = "Alice said nothing; she had sat down with her face in her"

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
    for length in range(300, 20001, 200):
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