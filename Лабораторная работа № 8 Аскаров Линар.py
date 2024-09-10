import tkinter as tk
import csv
from tkinter import *
from tkinter import colorchooser


class LineDrawerApp:
    def __init__(self, master): # master ?
        self.master = master
        self.master.geometry('%dx%d+%d+%d' % (1465, 900, 150, 50))
        self.master.title("ООП 8 лабораторная работа")

        self.canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack()

        # ?
        self.start_x = None
        self.start_y = None
        self.current_line = None
        self.dragging_line = None
        self.offset_x = 0
        self.offset_y = 0
        self.current_color = "#000000"  # начальный цвет линии

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Button-3>", self.on_right_button_press)
        self.canvas.bind("<B3-Motion>", self.on_right_mouse_drag)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.current_line = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, width=10,
                                                    fill=self.current_color)  # !!!!
        print("Нажата ЛКМ")

    def on_mouse_drag(self, event):
        if self.current_line:
            self.canvas.coords(self.current_line, self.start_x, self.start_y, event.x, event.y)

        print("Курсор двигается при помощи ЛКМ")

    def on_button_release(self, event):
        self.current_line = None

        print("Кнопка мыши отпускается (ЛКМ)")

    def on_right_button_press(self, event):
        # Проверяем, если линия находится под курсором
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)  # ?
        obj = list(self.canvas.find_all()) # Все объекты в Canvas
        print(f"OBJ {obj}")
        print(items, "!!!!")
        for item in items:
            if self.canvas.type(item) == 'line':
                self.dragging_line = item
                coords = self.canvas.coords(item)
                self.offset_x = event.x - coords[0]
                self.offset_y = event.y - coords[1]
                break
        print("Нажата ПКМ")

    def on_right_mouse_drag(self, event):
        if self.dragging_line:
            coords = self.canvas.coords(self.dragging_line)
            new_coords = (
                event.x - self.offset_x,
                event.y - self.offset_y,
                event.x - self.offset_x + (coords[2] - coords[0]),
                event.y - self.offset_y + (coords[3] - coords[1])
            )
            self.canvas.coords(self.dragging_line, *new_coords)  # зачем здесь *
        print("Курсор двигается при помощи ПКМ")

    def on_right_button_release(self, event):
        self.dragging_line = None
        print("Кнопка мыши отпускается (ПКМ)")

    def set_color(self, color):
        self.current_color = color




class Interface(Frame):

    def __init__(self, app):
        super().__init__()
        self.frame = None
        self.btn = None
        self.btn_segmentation = None
        self.app = app
        self.initUI()

    def initUI(self):  # инициализация UI элементов
        self.pack(fill=BOTH, expand=1)

        self.btn = Button(self, text="Выберите цвет", command=self.onChoose)
        self.btn.place(x=20, y=30)

        self.btn_segmentation = Button(self, text="Сегментация выбранного отрезка")
        self.btn_segmentation.place(x=300, y=30)


        self.frame = Frame(self, border=1, relief=SUNKEN, width=100, height=100)
        self.frame.place(x=160, y=30)

    def onChoose(self):  # что за функция
        print("Выбор цвета")
        (rgb, hx) = colorchooser.askcolor()
        if hx:
            self.app.set_color(hx)
            self.frame.config(bg=hx)






if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawerApp(root)
    ex = Interface(app)
    ex.pack()
    root.mainloop()
