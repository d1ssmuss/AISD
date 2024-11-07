from tkinter import *
from tkinter.messagebox import showinfo


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
        self.game_title.pack(pady=50)

        # Кнопки
        self.play_two_person = Button(master, text="На двоих", font=("Tahoma", 45),
                                      command=self.start_game_two, activebackground="#3b3fc5",
                                      activeforeground="white",
                                      anchor="center",
                                      bd=3,
                                      bg="lightgray",
                                      disabledforeground="gray",
                                      highlightbackground="black",
                                      highlightcolor="green",
                                      highlightthickness=2,
                                      justify="center",
                                      overrelief="raised",
                                      padx=10,
                                      pady=5,
                                      width=15)

        self.play_ai = Button(master, text="Против Компьютера", font=("Tahoma", 45),
                              command=self.start_game_ai, activebackground="#3b3fc5",
                              activeforeground="white",
                              anchor="center",
                              bd=3,
                              bg="lightgray",
                              disabledforeground="gray",
                              highlightbackground="black",
                              highlightcolor="green",
                              highlightthickness=2,
                              justify="center",
                              overrelief="raised",
                              padx=10,
                              pady=5,
                              width=20)

        self.exit = Button(master, text="Выйти из игры", font=("Tahoma", 45), command=master.destroy,
                           activebackground="#3b3fc5",
                           activeforeground="white",
                           anchor="center",
                           bd=3,
                           bg="lightgray",
                           disabledforeground="gray",
                           highlightbackground="black",
                           highlightcolor="green",
                           highlightthickness=2,
                           justify="center",
                           overrelief="raised",
                           padx=10,
                           pady=5,
                           width=15)

        # Размещаем кнопки
        self.play_two_person.pack(pady=20)
        self.play_ai.pack(pady=20)
        self.exit.pack(pady=20)

        self.current_player = "X"  # Игрок, который сейчас ходит
        self.maps = [""] * 9  # Инициализируем игровую карту
        self.is_ai_game = False  # Флаг, указывающий, играем ли мы против AI

    def start_game_two(self):
        self.is_ai_game = False  # Устанавливаем флаг, что играем против друга
        self.hide_menu()
        self.create_game_board()

    def start_game_ai(self):
        self.is_ai_game = True  # Устанавливаем флаг, что играем против AI
        self.hide_menu()
        self.create_game_board()

    def hide_menu(self):
        self.game_title.pack_forget()
        self.play_two_person.pack_forget()
        self.play_ai.pack_forget()
        self.exit.pack_forget()

    def create_game_board(self):
        self.board_frame = Frame(self.master)
        self.board_frame.pack(pady=20)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = Button(self.board_frame, text="", font=("Tahoma", 40), width=5, height=2,
                                            command=lambda x=i, y=j: self.make_move(x, y))
                self.buttons[i][j].grid(row=i, column=j)

        # Кнопка "Назад"
        self.back_button = Button(self.master, text="Назад", font=("Tahoma", 30), command=self.back_to_menu)
        self.back_button.pack(pady=20)

    def back_to_menu(self):
        self.board_frame.pack_forget()
        self.back_button.pack_forget()
        self.show_menu()

    def show_menu(self):
        self.game_title.pack(pady=50)
        self.play_two_person.pack(pady=20)
        self.play_ai.pack(pady=20)
        self.exit.pack(pady=20)

    def make_move(self, x, y):
        if self.buttons[x][y]['text'] == "":
            self.buttons[x][y]['text'] = self.current_player  # Устанавливаем текущего игрока
            self.buttons[x][y]['fg'] = "Blue" if self.current_player == "X" else "Red"
            self.maps[x * 3 + y] = self.current_player  # Обновляем карту

            if self.check_winner(self.current_player):
                showinfo("Победа!", f"Игрок {self.current_player} победил!")
                self.reset_game()
            elif self.is_draw():
                showinfo("Ничья!", "Игра закончилась вничью!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"  # Меняем игрока
                if self.is_ai_game and self.current_player == "O":  # Если следующий ход AI
                    self.AI()

    def check_winner(self, player):
        # Проверка строк
        for row in range(3):
            if all(self.buttons[row][col]['text'] == player for col in range(3)):
                return True
        # Проверка столбцов
        for col in range(3):
            if all(self.buttons[row][col]['text'] == player for row in range(3)):
                return True
        # Проверка диагоналей
        if all(self.buttons[i][i]['text'] == player for i in range(3)):
            return True
        if all(self.buttons[i][2 - i]['text'] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.buttons[i][j]['text'] != "" for i in range(3) for j in range(3))

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ""
                self.maps[i * 3 + j] = ""  # Сбрасываем карту
        self.current_player = "X"  # Сбросить текущего игрока на "X"

    def check_line(self, sum_O, sum_X):
        step = ""
        victories = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # строки
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # столбцы
            [0, 4, 8], [2, 4, 6]  # диагонали
        ]
        for line in victories:
            o = sum(1 for j in line if self.maps[j] == "O")
            x = sum(1 for j in line if self.maps[j] == "X")

            if o == sum_O and x == sum_X:
                for j in line:
                    if self.maps[j] != "O" and self.maps[j] != "X":
                        step = j  # Возвращаем индекс пустой ячейки
        return step

    def AI(self):
        step = ""

        # 1) Если на какой-либо из победных линий 2 свои фигуры и 0 чужих - ставим
        step = self.check_line(2, 0)

        # 2) Если на какой-либо из победных линий 2 чужие фигуры и 0 своих - ставим
        if step == "":
            step = self.check_line(0, 2)

        # 3) Если 1 фигура своя и 0 чужих - ставим
        if step == "":
            step = self.check_line(1, 0)

        # 4) Центр пуст, то занимаем центр
        if step == "":
            if self.maps[4] == "":
                step = 4  # Центр

        # 5) Если центр занят, то занимаем первую пустую ячейку
        if step == "":
            for i in range(9):
                if self.maps[i] == "":
                    step = i
                    break

        if step != "":
            x, y = divmod(step, 3)  # Преобразуем индекс в координаты
            self.make_move(x, y)  # Делаем ход AI


if __name__ == "__main__":
    root = Tk()
    app = TicTacToe(root)
    root.mainloop()