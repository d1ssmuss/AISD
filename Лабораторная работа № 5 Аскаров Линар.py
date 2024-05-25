'''
Лабораторная работа №5
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно.
Определить границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной
и графической форме в виде отчета по лабораторной работе.
F(1) = G(1) = 1;
F(n) = (-1)**n * ( n! //F(n–1) – G(n–1) ),
G(n) = (n–1)! + G(n–1), при n >=2

'''

import timeit
import matplotlib.pyplot as plt


last_factorial = 1
def dynamic_factorial(n):
    global last_factorial
    last_factorial = n * last_factorial
    return last_factorial

def recursive_factorial(n):
    if n == 1:
        return 1
    else:
        return n * recursive_factorial(n-1)


def iterative_factorial(n):
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

last_G_value = 1
last_F_value = 1

# G
def dynamic_G(n):
    global last_G_value, last_F_value
    if n == 1:
        return 1
    else:
        last_G_value = dynamic_factorial(n-1) + dynamic_G(n-1)
        return last_G_value

# F
def dynamic_F(n):
    global last_G_value, last_F_value
    if n == 1:
        return 1
    else:
        global step
        step *= -1
        last_F_value = step * (dynamic_factorial(n) // dynamic_F(n-1) - dynamic_G(n-1))
        return last_F_value

# Время time.time
def score_time(func, n):
    return timeit.timeit(lambda: func(n), number=1000)

# Значения n для которых мы хотим измерить время выполнения
n_values = range(2, 100)
recursive_times = []
iterative_times = []
step = 1


for n in n_values:
    recursive_times.append(score_time(recursive_factorial, n))
    iterative_times.append(score_time(iterative_factorial, n))


# Табличка
print(f"{'n':<10}{'Рекурсивное время (мс)':<25}{'Итерационное время (мс)':<25}")
for i, n in enumerate(n_values):
    print(f"{n:<10}{recursive_times[i]:<25}{iterative_times[i]:<25}")

# График
plt.plot(n_values, recursive_times, label='Рекурсивно')
plt.plot(n_values, iterative_times, label='Итерационно')
plt.xlabel('n')
plt.ylabel('Время (в миллисекундах)')
plt.legend()
plt.title('Сравнение времени вычисления функции F(n)')
plt.show()
