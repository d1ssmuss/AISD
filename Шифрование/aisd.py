import tkinter as tk
from tkinter import messagebox
import numpy as np


def encrypt_message():
    message = message_entry.get()
    m = int(key_entry.get())

    if not message:
        messagebox.showwarning("Предупреждение", "Введите сообщение для шифрования.")
        return

    encrypted_message = ""
    n = len(message)

    # Создание массива
    matrix = [["" for _ in range(n)] for _ in range(m)]

    j = 0
    flag = True

    while flag:
        for i in range(m):
            if j == len(message):
                flag = False
                break
            matrix[i][j] = message[j]
            j += 1
        for i in range(m - 2, 0, -1):
            if j == len(message):
                flag = False
                break
            matrix[i][j] = message[j]
            j += 1

    for i in range(m):
        for j in range(n):
            if matrix[i][j] != "":
                encrypted_message += matrix[i][j]

    # Отображение зашифрованного сообщения
    result_label.config(text=f"Зашифрованное сообщение: {encrypted_message}")

    # Отображение матрицы
    display_matrix(matrix)


def display_matrix(matrix):
    for widget in matrix_frame.winfo_children():
        widget.destroy()

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            label = tk.Label(matrix_frame, text=matrix[i][j], borderwidth=1, relief="solid", width=4, height=2)
            label.grid(row=i, column=j, padx=2, pady=2)

    # Добавление стрелочек
    for i in range(len(matrix)):
        if i < len(matrix):
            arrow_label = tk.Label(matrix_frame, text="↓", font=("Arial", 12))
            arrow_label.grid(row=i, column=len(matrix[0]), padx=2, pady=2)

    for j in range(len(matrix[0])):
        if j < len(matrix[0]):
            arrow_label = tk.Label(matrix_frame, text="→", font=("Arial", 12))
            arrow_label.grid(row=len(matrix), column=j, padx=2, pady=2)


# Создание основного окна
root = tk.Tk()
root.title("Шифрование сообщения")

# Ввод сообщения
tk.Label(root, text="Введите сообщение:").pack()
message_entry = tk.Entry(root, width=50)
message_entry.pack()

# Ввод ключа
tk.Label(root, text="Введите ключ M:").pack()
key_entry = tk.Entry(root, width=10)
key_entry.pack()

# Кнопка для шифрования
encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_message)
encrypt_button.pack()

# Метка для результата
result_label = tk.Label(root, text="")
result_label.pack()

# Фрейм для отображения матрицы
matrix_frame = tk.Frame(root)
matrix_frame.pack()

# Запуск приложения
root.mainloop()