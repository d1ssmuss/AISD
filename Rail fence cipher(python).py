import tkinter as tk
from tkinter import messagebox


def encrypt_message():
    message = message_entry.get().replace(" ", "")  # Убираем пробелы внутри сообщения
    m = key_entry.get()

    # Проверка на корректность ввода
    if not message:
        messagebox.showwarning("Предупреждение", "Введите сообщение для шифрования.")
        return
    if not m.isdigit():
        messagebox.showwarning("Предупреждение", "Ключ должен быть целым числом.")
        return

    m = int(m)
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
    display_matrix(matrix, encrypted_message)


def decrypt_message():
    message = message_entry.get().replace(" ", "")  # Убираем пробелы внутри сообщения
    m = key_entry.get()

    # Проверка на корректность ввода
    if not message:
        messagebox.showwarning("Предупреждение", "Введите сообщение для дешифрования.")
        return
    if not m.isdigit():
        messagebox.showwarning("Предупреждение", "Ключ должен быть целым числом.")
        return

    m = int(m)
    n = len(message)
    matrix = [["" for _ in range(n)] for _ in range(m)]

    # Заполнение матрицы символами
    j = 0
    flag = True
    while flag:
        for i in range(m):
            if j < n:
                matrix[i][j] = '*'
                j += 1
            else:
                flag = False
                break
        for i in range(m - 2, 0, -1):
            if j < n:
                matrix[i][j] = '*'
                j += 1
            else:
                flag = False
                break

    # Заполнение матрицы символами
    index = 0
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '*':
                matrix[i][j] = message[index]
                index += 1

    # Дешифрование
    decrypted_message = ""
    j = 0
    flag = True
    while flag:
        for i in range(m):
            if j < n:
                decrypted_message += matrix[i][j]
                j += 1
            else:
                flag = False
                break
        for i in range(m - 2, 0, -1):
            if j < n:
                decrypted_message += matrix[i][j]
                j += 1
            else:
                flag = False
                break

    result_label.config(text=f"Расшифрованное сообщение: {decrypted_message}")
    display_matrix(matrix, decrypted_message)


def display_matrix(matrix, message):
    for widget in matrix_frame.winfo_children():
        widget.destroy()  # Очистка предыдущих элементов

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if message and matrix[i][j] != "":
                label = tk.Label(matrix_frame, text=matrix[i][j], borderwidth=1, relief="solid", width=4, height=2,
                                 bg="lightblue", font=("Arial", 12, "bold"))
            else:
                label = tk.Label(matrix_frame, text="", borderwidth=1, relief="solid", width=4, height=2,
                                 font=("Arial", 12, "bold"))
            label.grid(row=i, column=j, padx=2, pady=2)

    # Добавление стрелочек
    for i in range(len(matrix)):
        if i < len(matrix):
            arrow_label = tk.Label(matrix_frame, text="↓", font=("Arial", 12, "bold"))
            arrow_label.grid(row=i, column=len(matrix[0]), padx=2, pady=2)

        for j in range(len(matrix[0])):
            if j < len(matrix[0]):
                arrow_label = tk.Label(matrix_frame, text="→", font=("Arial", 12, "bold"))
                arrow_label.grid(row=len(matrix), column=j, padx=2, pady=2)


# Создание основного окна
root = tk.Tk()
root.title("Зигзаговый шифр")
root.geometry('1250x700+300+200')

# Ввод сообщения
tk.Label(root, text="Введите сообщение:", font=("Arial", 14, "bold")).pack()
message_entry = tk.Entry(root, width=50, font=("Arial", 14))
message_entry.pack()

tk.Label(root, text="Введите ключ:", font=("Arial", 14, "bold")).pack()
key_entry = tk.Entry(root, width=10, font=("Arial", 14))
key_entry.pack()

encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_message, font=("Arial", 14, "bold"))
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Дешифровать", command=decrypt_message, font=("Arial", 14, "bold"))
decrypt_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack()

matrix_frame = tk.Frame(root)
matrix_frame.pack()

# Запуск приложения
root.mainloop()
