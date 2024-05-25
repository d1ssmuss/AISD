from tkinter import *
import itertools
import time
import random
from tkinter.scrolledtext import ScrolledText

tk = Tk()
tk.title("Лабораторная работа №7")

screen_width = tk.winfo_screenwidth()
screen_height = tk.winfo_screenheight()

x_cordinate = int((screen_width/2) - (1280/2))
y_cordinate = int((screen_height/2) - (720/2))

tk.geometry("{}x{}+{}+{}".format(1280, 750, x_cordinate, y_cordinate))

n = 0
k = 0


def show_context_n():
    value = len_arr.get()
    global n
    n = value
    if value:
        return value
    else:
        print("Параметр N не задан")


def show_context_k():
    val = argument_K.get()
    global k
    k = val
    if val:
        return val
    else:
        print("Параметр K не задан")


label_n = Label(text="Введите длину массива (N): ", font=("Arial", 14))
label_n.pack(anchor="nw")

len_arr = Entry(tk, width=25, font=("Arial", 15))
len_arr.pack(anchor="nw")

label_k = Label(text="Введите кол-во отрицательных чисел меньше или равно в массивах (K): ", font=("Arial", 14))
label_k.pack(anchor="nw")

argument_K = Entry(tk, width=25, font=("Arial", 15))
argument_K.pack(anchor="nw")

label_v = Label(text="Все возможные варианты: ", font=("Arial", 14, 'italic'))
label_v.pack()

text_info = ""
st = ScrolledText(tk, width=100,  height=20, font=("Times New Roman", 15))
st.pack()


def lab(n,k):
    global text_info
    arr = [random.randint(-5, 5) for i in range(n)]
    middle_length = n // 2
    text_info += str(arr)
    f = bool()
    start_func = time.time()

    def replace_negatives(arr, mask):
        return [abs(arr[i]) if mask[i] and (i % 2 == 0) and (arr[i] < 0) else arr[i] for i in range(len(arr))]

    all_variants = [replace_negatives(arr, mask) for mask in itertools.product([0, 1], repeat=n)]
    combinations = []
    for i in all_variants:
        if i not in combinations and i != arr:
            combinations.append(i)

    if len(combinations) == 0:
        text_info += "\n"
        text_info += "Ваш массив не удовлетворяет условию задачи. Перезапустите программу"
        f = False
    else:
        text_info += "\n"
        f = True
        text_info += "Все возможные варианты: (Функции питона)"
        text_info += "\n"
        for i in combinations:
            text_info += str(i) + " "
            text_info += "\n"

        end_func = time.time()

        text_info += "\n"
        text_info += "С помощью функций питона: {:>.5f}".format(end_func - start_func) + " секунд."
    if f:
        text_info += "\n"
        start_alg = time.time()
        masks = []
        for i in range(2 ** n):
            mask = bin(i)[2:].zfill(n)
            masks.append(list(mask))
        for mask in masks:
            for j in range(len(mask)):
                mask[j] = int(mask[j])
        alg_var = [replace_negatives(arr, mask) for mask in masks]
        var = []
        for i in alg_var:
            if i not in var and i != arr:
                var.append(i)
    try:
        if len(var) == 0:
            text_info += "Ваш массив не удовлетворяет условию задачи. Перезапустите программу"
            fl = False
        else:
            fl = True
            text_info += "Все возможные варианты: (Алгоритмический метод) \n"
            for i in var:
                text_info += str(i) + " "
                text_info += "\n"
            end_alg = time.time()
            text_info += "Алгоритмический метод: {:>.5f}".format(end_alg - start_alg) + " секунд. \n"
            text_info += "Разница по времени {:>.5f}".format(abs((end_alg - start_alg) - (end_func - start_func))) + " секунд.\n"
            text_info += "\nУсложнённый вариант:\n"

    except NameError:
        pass
    try:
        if fl:
            flag = bool
            values = []
            for i in range(len(var)):
                neg_count = sum(1 for x in var[i] if x < 0)
                if neg_count <= k:
                    values.append(var[i])
            text_info += "\n"
            if len(values) == 0:
                text_info += "Число K не удовлетворяет условию. Перезапустите программу"
                flag = False
            else:
                text_info += str(values) + "\n"
                flag = True
            if flag:
                min_sum = float('inf')
                optimal_variant = None
                for variant in values:
                    current_sum = sum(variant)
                    if current_sum < min_sum:
                        min_sum = current_sum
                        optimal_variant = variant
                text_info += "\n"
                text_info += f"Массив: {optimal_variant} \n"
                text_info += f"Минимальная сумма: {min_sum}"
    except NameError:
        pass
    info = text_info
    text_info = ""
    return info


btn2 = Button(
    text="Вывести результаты",
    width=25,
    height=2,
    font=("Sans", 16, "bold"),
    command=lambda: [show_context_n(), show_context_k(), st.insert(END, lab(int(n),int(k)))]
)
btn2.pack(anchor="nw")


btn_clean = Button(
    text="Очистить виджет Text",
    width=25,
    height=2,
    font=("Sans", 16, "bold"),
    command=lambda: st.delete(1.0, END)
)
btn_clean.pack(anchor="nw")
tk.mainloop()
