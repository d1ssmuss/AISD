"Program n_0"
# Импортирую библиотеки
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title('Крестики нолики v1.0')
        self.master.geometry('%dx%d+%d+%d' % (1585, 900, 150, 50))

        # добавляю ** background **
        self.master.config(bg="#6c6bb2")

        # Заголовок игры
        self.game_title = Label(master, text="Крестики нолики X.O", font=("Tahoma", 59), background="#6c6bb2",
                                foreground="#ffffff")
        self.game_title.pack(pady=50)  # Центрируем заголовок

        # Кнопки
        self.play_two_person = Button(master, text="На двоих", font=("Tahoma", 45),
                   activebackground="#3b3fc5",
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   disabledforeground="gray",
                   #fg="black",
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=15)
        self.play_ai = Button(master, text="Против Компьютера", font=("Tahoma", 45), activebackground="#3b3fc5",
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   disabledforeground="gray",
                   #fg="black",
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=20)
        self.exit = Button(master, text="Выйти из игры", font=("Tahoma", 45), command=master.destroy, activebackground="#3b3fc5",
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   disabledforeground="gray",
                   #fg="black",
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=15)

        # Размещаем кнопки
        self.play_two_person.pack(pady=20)  # Вертикальное расположение
        self.play_ai.pack(pady=20)
        self.exit.pack(pady=20)


    def main_menu(self):
        pass


if __name__ == "__main__":
    root = Tk()
    app = TicTacToe(root)
    root.mainloop()
    print("return 0")  # потом убрать
