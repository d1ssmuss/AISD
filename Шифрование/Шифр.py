import numpy as np

# Заметки
"""
j != len(message)
Читать строку, затем убрать пробелы
"".join(s.split())
"""
# Сообщение
message = input("Введите сообщение, которое нужно зашифровать: ")

encrypted_message = ""

m = int(input("Введите ключ M: "))  # ключ
n = len(message)
matrix = np.empty((m, n), dtype=str)  # Создание массива, заполненного пустыми строками
matrix = [['' for some in range(n)] for something in range(m)]

matrix = [[""] * m for i in range(n)]  # в чём отличие
print(matrix)
j = 0

flag = True
while flag:
    for i in range(0, m):
        if j == len(message):
            flag = False
        else:
            matrix[i][j] = message[j]
            j += 1
    for i in range(m-2, 0, -1):
        if j == len(message):
            flag = False
        else:
            matrix[i][j] = message[j]
            j += 1

for i in range(m):
    for j in range(n):
        if matrix[i][j] != " ":
            encrypted_message += matrix[i][j]

print(encrypted_message)
