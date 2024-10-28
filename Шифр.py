import numpy as np


# Сообщение
message = "АЛГОРИТМЫИСТРУКТУРЫДАННЫХ"

encrypted_message = ""

m = int(input("Введите ключ M: "))  # ключ
n = len(message)
matrix = np.empty((m, n), dtype=str)  # Создание массива, заполненного пустыми строками
#print(matrix)

"""for i in range(1, 0, -1):
    print(i)"""



j = 0

flag = True
# j != len(message)
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


print(matrix)
for i in range(m):
    for j in range(n):
        if matrix[i][j] != " ":
            encrypted_message += matrix[i][j]

print(encrypted_message)
