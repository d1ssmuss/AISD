"""Задание на л.р. №8 ООП 24
Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.
ИСТбд-13
Вариант 4
Объекты – отрезки
Функции:	сегментация
визуализация
раскраска
перемещение на плоскости
"""
from tkinter import *
import math

# Добавить кнопки


tk = Tk()
canvas = Canvas(bg="white", width=1360, height=720)  # canvas
canvas.pack(anchor=CENTER)

# Создаю линию
canvas.create_line(85, 85, 365, 365, fill="blue", width=5, dash=100)  # width - изменяет толщину фигуры
canvas.create_line(42, 85, 860, 365, fill="orange", width=5, dash=150)
canvas.create_line(46, 128, 749, 389, fill="green", width=9)  # dash - сегментация ?

tk.title("Лабораторная Работа №8 (Алгоритмы и Структуры Данных)")
tk.geometry("1070x720")

btn_left = Button(text="<-", width=3, height=3)
btn_right = Button(text="->", width=3, height=3)
btn_up = Button(text="^", width=3, height=3)
btn_down = Button(text="V", width=3, height=3)
btn_left.place(x=0, y=0) # place или pack
btn_right.place(x=100, y=1)
btn_up.place(x=300, y=150)
btn_down.place(x=420, y=130)


class Line:
    def __init__(self, x1, y1, x2, y2):  # (x1;y1) - нач.координаты, (x2;y2) - конеч.координаты
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def paint(self):
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'black']  # атрибут



# Segment - отрезок(рус.)

Segment = Line(5, 5, 25, 25)



tk.mainloop()
