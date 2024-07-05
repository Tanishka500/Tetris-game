import tkinter as tk
import random

class Tetris(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tetris")
        self.geometry("300x700")
        self.resizable(False, False)
        
        self.canvas = tk.Canvas(self, width=300, height=600, bg='black')
        self.canvas.pack()

        self.score_label = tk.Label(self, text="Score: 0", font=("Helvetica", 16), bg='black', fg='white')
        self.score_label.pack(pady=10)

        self.restart_button = tk.Button(self, text="Restart", command=self.restart_game, font=("Helvetica", 14, "bold"), bg='white', fg='black', width=10, height=2)
        self.restart_button.pack(pady=10)

        self.tetrominoes = [
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1, 1]],          # I
            [[1, 1], [1, 1]],        # O
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]],  # Z
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]]   # J
        ]
        self.colors = ['cyan', 'yellow', 'purple', 'green', 'red', 'blue', 'orange']

        self.score = 0
        self.board = [[0] * 10 for _ in range(20)]
        self.current_tetromino = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        self.game_over = False

        self.bind("<Key>", self.handle_keys)
        self.new_tetromino()
        self.update_game()

    def restart_game(self):
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.board = [[0] * 10 for _ in range(20)]
        self.current_tetromino = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        self.game_over = False
        self.new_tetromino()
        self.update_game()

    def new_tetromino(self):
        self.current_tetromino = random.choice(self.tetrominoes)
        self.current_color = random.choice(self.colors)
        self.current_x = 3
        self.current_y = 0

    def handle_keys(self, event):
        if self.game_over:
            return
        if event.keysym == "Left":
            self.move(-1)
        elif event.keysym == "Right":
            self.move(1)
        elif event.keysym == "Down":
            self.drop()
        elif event.keysym == "Up":
            self.rotate()

    def move(self, dx):
        if not self.collides(self.current_tetromino, self.current_x + dx, self.current_y):
            self.current_x += dx
        self.redraw()

    def drop(self):
        if not self.collides(self.current_tetromino, self.current_x, self.current_y + 1):
            self.current_y += 1
        else:
            self.place_tetromino()
            self.clear_lines()
            if not self.game_over:
                self.new_tetromino()
        self.redraw()

    def rotate(self):
        rotated = list(zip(*self.current_tetromino[::-1]))
        if not self.collides(rotated, self.current_x, self.current_y):
            self.current_tetromino = rotated
        self.redraw()

    def collides(self, tetromino, x, y):
        for i, row in enumerate(tetromino):
            for j, cell in enumerate(row):
                if cell and (x + j < 0 or x + j >= 10 or y + i >= 20 or self.board[y + i][x + j]):
                    if y + i < 0:
                        self.game_over = True
                    return True
        return False

    def place_tetromino(self):
        for i, row in enumerate(self.current_tetromino):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.current_y + i][self.current_x + j] = self.current_color
        if self.current_y == 0:
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = 20 - len(new_board)
        self.score += lines_cleared * 100
        self.score_label.config(text=f"Score: {self.score}")
        self.board = [[0] * 10 for _ in range(lines_cleared)] + new_board

    def redraw(self):
        self.canvas.delete("all")
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(x * 30, y * 30, x * 30 + 30, y * 30 + 30, fill=cell)
        for i, row in enumerate(self.current_tetromino):
            for j, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle((self.current_x + j) * 30, (self.current_y + i) * 30, (self.current_x + j) * 30 + 30, (self.current_y + i) * 30 + 30, fill=self.current_color)
        if self.game_over:
            self.canvas.create_text(150, 300, text="GAME OVER", fill="red", font=("Helvetica", 24))

    def update_game(self):
        if not self.game_over:
            self.drop()
            self.after(500, self.update_game)

if __name__ == "__main__":
    game = Tetris()
    game.mainloop()
