import tkinter as tk
import csv
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo


class LineDrawerApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry('%dx%d+%d+%d' % (1585, 900, 150, 50))
        self.master.configure(background="#A8E4A0")
        self.master.title("ООП 8 лабораторная работа")

        self.canvas = Canvas(master, bg="white", width=1080, height=600)
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.current_line = None
        self.selected_line = None
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

    def on_mouse_drag(self, event):
        if self.current_line:
            self.last_line = self.current_line
            self.canvas.coords(self.current_line, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        if self.current_line:
            coords = self.canvas.coords(self.current_line)
            self.lines.append([self.current_line, coords, self.current_color, "No"])
        self.current_line = None

    def on_right_button_press(self, event):
        items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for item in items:
            if self.canvas.type(item) == 'line':
                self.dragging_line = item
                self.selected_line = item
                coords = self.canvas.coords(item)
                self.offset_x = event.x - coords[0]
                self.offset_y = event.y - coords[1]
                break

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
            # Обновляем координаты в списке lines
            for line in self.lines:
                if line[0] == self.dragging_line:
                    line[1] = list(new_coords)

    def on_right_button_release(self, event):
        self.dragging_line = None

    def set_color(self, color):
        self.current_color = color

    def segment(self):
        if self.selected_line:
            self.canvas.itemconfig(self.selected_line, dash=(100, 50))
            for line in self.lines:
                if line[0] == self.selected_line:
                    line[3] = "Yes"
        self.selected_line = None

    def save_lines(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Line ID", "X1", "Y1", "X2", "Y2", "Color", "Segmented"])
                    for i, line in enumerate(self.lines):
                        writer.writerow([i, line[1][0], line[1][1], line[1][2], line[1][3], line[2], line[3]])
                showinfo("Сохранение", "Линии успешно сохранены в файл!")
        except Exception as e:
            showerror("Ошибка", f"Ошибка при сохранении: {e}")

    def load_lines(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                self.lines = []
                with open(file_path, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # пропускаем заголовок
                    for row in reader:
                        line_id = int(row[0])
                        coords = [float(row[1]), float(row[2]), float(row[3]), float(row[4])]
                        color = row[5]
                        segmented = row[6]
                        new_line = self.canvas.create_line(*coords, width=10, fill=color)
                        self.lines.append([new_line, coords, color, segmented])
                showinfo("Загрузка", "Линии успешно загружены из файла!")
        except Exception as e:
            showerror("Ошибка", f"Ошибка при загрузке: {e}")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.lines = []


class Interface(Frame):
    def __init__(self, app):
        super().__init__()
        self.frame = None
        self.btn = None
        self.btn_segmentation = None
        self.btn_open = None
        self.save = None
        self.clear = None
        self.info = None
        self.app = app
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)
        self.config(background="#A8E4B9")
        self.btn = Button(self, text="Выберите цвет", command=self.choose_color)
        self.btn.place(x=20, y=30)
        self.btn_segmentation = Button(self, text="Сегментация выбранного отрезка", command=self.onClick,
                                       activebackground="#599fc0",
                                       activeforeground="white", anchor="center", bd=3, bg="lightgray",
                                       disabledforeground="gray", fg="black", font=("Arial", 12), height=2,
                                       highlightbackground="black", highlightcolor="green", highlightthickness=2,
                                       justify="center", overrelief="raised", padx=10, pady=5, width=30,
                                       wraplength=100)
        self.btn_segmentation.place(x=630, y=30)

        self.btn_open = Button(self, text="Ввод данных", command=self.app.load_lines, activebackground="#599fc0",
                               activeforeground="white", anchor="center", bd=3, bg="lightgray",
                               disabledforeground="gray",
                               fg="black", font=("Arial", 12), height=2, highlightbackground="black",
                               highlightcolor="green", highlightthickness=2, justify="center", overrelief="raised",
                               padx=10, pady=5, width=30, wraplength=100)
        self.btn_open.place(x=330, y=30)

        self.save = Button(self, text="Сохранение данных", command=self.app.save_lines, activebackground="#599fc0",
                           activeforeground="white", anchor="center", bd=3, bg="lightgray", disabledforeground="gray",
                           fg="black", font=("Arial", 12), height=2, highlightbackground="black",
                           highlightcolor="green",
                           highlightthickness=2, justify="center", overrelief="raised", padx=10, pady=5, width=30,
                           wraplength=100)
        self.save.place(x=932, y=30)

        self.info = Button(self, text="Информация", command=self.about, activebackground="#599fc0",
                           activeforeground="white", anchor="center", bd=3, bg="lightgray", disabledforeground="gray",
                           fg="black", font=("Arial", 12), height=2, highlightbackground="black",
                           highlightcolor="green",
                           highlightthickness=2, justify="center", overrelief="raised", padx=10, pady=5, width=30,
                           wraplength=100)
        self.info.place(x=470, y=92)

        self.clear = Button(self, text="Очистить доску", command=self.app.clear_canvas, activebackground="#599fc0",
                            activeforeground="white",anchor="center", bd=3, bg="lightgray", disabledforeground="gray",
                            fg="black", font=("Arial", 12), height=2, highlightbackground="black",
                            highlightcolor="green", highlightthickness=2,
                            justify="center", overrelief="raised", padx=10, pady=5, width=30,
                            wraplength=100)

        self.clear.place(x=772, y=92)

        self.frame = Frame(self, border=1, relief=SUNKEN, width=100, height=100, background="black")
        self.frame.place(x=160, y=30)



    def about(self):
        window = Tk()
        window.title("Окно информации")
        window.geometry('%dx%d+%d+%d' % (1400, 400, 250, 250))
        label = tk.Label(window, text="--Руководство к приложению--\n"
                                      "В данной программе, пользователь рисует с помощью отрезков. Примечание:\n"
                                      "1. Файл должен иметь расширение .csv (имя файла любое) и находиться в рабочем директории проекта.\n"
                                      "2. CSV-файл содержит информацию об отрезках, где каждая строка описывает один отрезок.\n"
                                      "3. Каждая строка состоит из 7 объектов, разделенных запятыми:\n"
                                      "   - Первый объект - ID Отрезка\n"
                                      "   - Далее идут 4 числа - координаты отрезка: x0, y0, x1, y1\n"
                                      "   - Цвет и статус сегментирования.\n"
                                      "4. Пользователь может сохранить свою работу при нажатии на кнопку 'Сохранение данных'.\n"
                                      "5. Для того чтобы сегментировать отрезок, пользователю нужно выбрать данный отрезок при помощи ПКМ. \nА затем нажать на кнопку 'Сегментация выбранного отрезка'.\n"
                                      "6. Есть функция, которая очищает доску. \n"
                                      "7. Помните, что при загрузке нескольких файлов, рисунки накладываются друг на друга!",
                         font=("Tahoma ", 17, "bold"))
        label.pack()



    def choose_color(self):
        print("Выбор цвета")
        (rgb, hx) = colorchooser.askcolor()
        if hx:
            print(hx)
            self.app.set_color(hx)
            self.frame.config(bg=hx)


    def onClick(self):
        print("Кнопка сегментация нажата")
        self.app.segment()

if __name__ == "__main__":
    root = tk.Tk()
    app = LineDrawerApp(root)
    ex = Interface(app)
    ex.pack()
    root.mainloop()