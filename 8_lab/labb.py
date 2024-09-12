import tkinter as tk
import csv
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
import numpy as np
from tkinter.messagebox import showerror, showwarning, showinfo


class LineDrawerApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('%dx%d+%d+%d' % (1465, 900, 150, 50))
        self.master.title("ООП 8 лабораторная работа")

        self.canvas = tk.Canvas(master, bg="white", width=800, height=600)
        self.canvas.pack()

        self.obj = None
        self.start_x = None
        self.start_y = None
        self.current_line = None
        self.last_line = None
        self.dragging_line = None
        self.offset_x = 0
        self.offset_y = 0
        self.current_color = "#000000"  # начальный цвет линии
        self.lines = []  # для хранения данных о линиях

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
                                                    fill=self.current_color)
        # print("Нажата ЛКМ")

    def on_mouse_drag(self, event):
        if self.current_line:
            self.last_line = self.current_line
            self.canvas.coords(self.current_line, self.start_x, self.start_y, event.x, event.y)

        # print("Курсор двигается при помощи ЛКМ")

    def on_button_release(self, event):
        if self.current_line:
            coords = self.canvas.coords(self.current_line)
            self.lines.append([self.current_line, coords, self.current_color, "No"])
        self.current_line = None

        # print("Кнопка мыши отпускается (ЛКМ)")

    def on_right_button_press(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in items:
            if self.canvas.type(item) == 'line':
                self.dragging_line = item
                coords = self.canvas.coords(item)
                self.offset_x = event.x - coords[0]
                self.offset_y = event.y - coords[1]
                break
        # print("Нажата ПКМ")

    def on_right_mouse_drag(self, event):
        if self.dragging_line:
            coords = self.canvas.coords(self.dragging_line)
            new_coords = (
                event.x - self.offset_x,
                event.y - self.offset_y,
                event.x - self.offset_x + (coords[2] - coords[0]),
                event.y - self.offset_y + (coords[3] - coords[1])
            )
            self.canvas.coords(self.dragging_line, *new_coords)
        # print("Курсор двигается при помощи ПКМ")

    def on_right_button_release(self, event):
        self.dragging_line = None
        # print("Кнопка мыши отпускается (ПКМ)")

    def set_color(self, color):
        self.current_color = color

    def segment(self, obj):
        self.obj = obj
        self.canvas.itemconfig(self.last_line, dash=(100, 50))
        for line in self.lines:
            if line[0] == self.last_line:
                line[3] = "Yes"


class Interface(Frame):
    def __init__(self, app):
        super().__init__()
        self.frame = None
        self.btn = None
        self.btn_segmentation = None
        self.btn_open = None
        self.save = None
        self.app = app
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)

        self.btn = Button(self, text="Выберите цвет", command=self.onChoose)
        self.btn.place(x=20, y=30)

        self.btn_segmentation = Button(self, text="Сегментация последнего отрезка", command=self.onClick)
        self.btn_segmentation.place(x=300, y=30)

        self.btn_open = Button(self, text="Открыть файл", command=self.open_csv_file)
        self.btn_open.place(x=495, y=30)

        self.save = Button(self, text="Сохранить файл", command=self.savefile)
        self.save.place(x=585, y=30)

        self.frame = Frame(self, border=1, relief=SUNKEN, width=100, height=100)
        self.frame.place(x=160, y=30)

    def open_csv_file(self):
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.display_csv_data(file_path)

    def savefile(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.save_csv_data(file_path)

    def save_csv_data(self, file_path):
        with open(file_path, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            # Записываем заголовок
            csv_writer.writerow(['Line ID', 'Start X', 'Start Y', 'End X', 'End Y', 'Color', 'Segmented'])
            # Записываем данные о каждой линии
            for line in self.app.lines:
                line_id, coords, color, segmented = line
                csv_writer.writerow([line_id] + coords + [color, segmented])

    def display_csv_data(self, file_path):
        self.app.canvas.delete("all")  # Очищаем Canvas
        try:
            with open(file_path, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                header = next(csv_reader)  # Читаем заголовок
                for row in csv_reader:
                    line_id, start_x, start_y, end_x, end_y, color, segmented = row
                    line_id = int(line_id)
                    coords = [float(start_x), float(start_y), float(end_x), float(end_y)]
                    self.app.lines.append([line_id, coords, color, segmented])
                    self.app.canvas.create_line(*coords, fill=color, width=10,
                                                dash=(100, 50) if segmented == "Yes" else None)
        except Exception as e:
            showerror(title="Ошибка", message="Некорректный ввод данных !")

    def onChoose(self):
        print("Выбор цвета")
        (rgb, hx) = colorchooser.askcolor()
        if hx:
            self.app.set_color(hx)
            self.frame.config(bg=hx)

    def onClick(self):
        print("Кнопка сегментация нажата")
        self.app.segment(self.app.current_line)


if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawerApp(root)
    ex = Interface(app)
    ex.pack()
    root.mainloop()
