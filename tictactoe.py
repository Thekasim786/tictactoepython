import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎮 Tic Tac Toe Pro")
        self.window.geometry("600x700")   # fits most screens
        self.window.resizable(False, False)

        # Modern color scheme
        self.colors = {
            'bg': '#1a1a2e',
            'secondary': '#16213e',
            'accent': '#0f3460',
            'x_color': '#e94560',
            'o_color': '#f39c12',
            'text': '#eee',
            'button_hover': '#533483',
            'win_highlight': '#27ae60'
        }
        self.window.configure(bg=self.colors['bg'])

        # Game state
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.current_player = 'X'
        self.game_over = False
        self.scores = {'X': 0, 'O': 0, 'Draw': 0}

        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        # Title
        title = tk.Label(self.window, text="🎮 TIC TAC TOE PRO",
                         font=('Arial Black', 22, 'bold'),
                         fg=self.colors['x_color'], bg=self.colors['bg'])
        title.pack(pady=(10, 5))

        subtitle = tk.Label(self.window, text="Modern Gaming Experience",
                            font=('Arial', 11),
                            fg=self.colors['text'], bg=self.colors['bg'])
        subtitle.pack(pady=(0, 10))

        # Scoreboard
        self.setup_scoreboard()

        # Game board
        self.setup_game_board()

        # Status
        self.setup_status()

        # Control buttons
        self.setup_controls()

        # Footer
        footer = tk.Label(self.window, text="Made by Mohammad Kasim",
                          font=('Arial', 10, 'italic'),
                          fg="#aaa", bg=self.colors['bg'])
        footer.pack(side="bottom", pady=(5, 10))

    def setup_scoreboard(self):
        score_frame = tk.Frame(self.window, bg=self.colors['secondary'], relief='raised', bd=2)
        score_frame.pack(pady=5, padx=15, fill='x')

        # Use grid for perfect alignment
        score_frame.columnconfigure(0, weight=1)
        score_frame.columnconfigure(1, weight=1)
        score_frame.columnconfigure(2, weight=1)

        # Player X (left)
        x_frame = tk.Frame(score_frame, bg=self.colors['secondary'])
        x_frame.grid(row=0, column=0, padx=20, pady=5, sticky="nsew")
        tk.Label(x_frame, text="❌ Player X",
                 font=('Arial', 12, 'bold'),
                 fg=self.colors['x_color'], bg=self.colors['secondary']).pack()
        self.x_score_label = tk.Label(x_frame, text="0",
                                      font=('Arial', 14, 'bold'),
                                      fg=self.colors['text'], bg=self.colors['secondary'])
        self.x_score_label.pack()

        # Draws (center)
        draw_frame = tk.Frame(score_frame, bg=self.colors['secondary'])
        draw_frame.grid(row=0, column=1, padx=20, pady=5, sticky="nsew")
        tk.Label(draw_frame, text="🤝 Draws",
                 font=('Arial', 12, 'bold'),
                 fg=self.colors['text'], bg=self.colors['secondary']).pack()
        self.draw_score_label = tk.Label(draw_frame, text="0",
                                         font=('Arial', 14, 'bold'),
                                         fg=self.colors['text'], bg=self.colors['secondary'])
        self.draw_score_label.pack()

        # Player O (right)
        o_frame = tk.Frame(score_frame, bg=self.colors['secondary'])
        o_frame.grid(row=0, column=2, padx=20, pady=5, sticky="nsew")
        tk.Label(o_frame, text="⭕ Player O",
                 font=('Arial', 12, 'bold'),
                 fg=self.colors['o_color'], bg=self.colors['secondary']).pack()
        self.o_score_label = tk.Label(o_frame, text="0",
                                      font=('Arial', 14, 'bold'),
                                      fg=self.colors['text'], bg=self.colors['secondary'])
        self.o_score_label.pack()

    def setup_game_board(self):
        board_frame = tk.Frame(self.window, bg=self.colors['accent'], relief='raised', bd=3)
        board_frame.pack(pady=10, padx=30)

        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(board_frame, text='',
                                font=('Arial Black', 26, 'bold'),
                                width=3, height=1,
                                bg=self.colors['secondary'],
                                fg=self.colors['text'],
                                activebackground=self.colors['button_hover'],
                                relief='raised', bd=2,
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=3, pady=3)

                btn.bind('<Enter>', lambda e, b=btn: self.on_hover(b))
                btn.bind('<Leave>', lambda e, b=btn: self.on_leave(b))
                row.append(btn)
            self.buttons.append(row)

    def setup_status(self):
        self.status_label = tk.Label(self.window,
                                     text=f"🎯 Player {self.current_player}'s Turn",
                                     font=('Arial', 14, 'bold'),
                                     fg=self.colors['x_color'],
                                     bg=self.colors['bg'])
        self.status_label.pack(pady=(5, 15))

    def setup_controls(self):
        control_frame = tk.Frame(self.window, bg=self.colors['bg'])
        control_frame.pack(side="bottom", pady=10)

        new_game_btn = tk.Button(control_frame, text="🔄 New Game",
                                 font=('Arial', 12, 'bold'),
                                 bg=self.colors['accent'], fg=self.colors['text'],
                                 activebackground=self.colors['button_hover'],
                                 relief='raised', bd=2, padx=15, pady=5,
                                 command=self.new_game)
        new_game_btn.pack(side='left', padx=15)

        reset_btn = tk.Button(control_frame, text="🗑️ Reset Scores",
                              font=('Arial', 12, 'bold'),
                              bg=self.colors['x_color'], fg=self.colors['text'],
                              activebackground='#c0392b',
                              relief='raised', bd=2, padx=15, pady=5,
                              command=self.reset_scores)
        reset_btn.pack(side='right', padx=15)

    def on_hover(self, button):
        if button['text'] == '':
            button.configure(bg=self.colors['button_hover'])

    def on_leave(self, button):
        if button['text'] == '':
            button.configure(bg=self.colors['secondary'])

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            color = self.colors['x_color'] if self.current_player == 'X' else self.colors['o_color']
            symbol = '❌' if self.current_player == 'X' else '⭕'
            self.buttons[row][col].configure(text=symbol, fg=color, bg=self.colors['accent'])

            if self.check_winner():
                self.handle_game_end(f"🎉 Player {self.current_player} Wins!")
                self.scores[self.current_player] += 1
                self.highlight_winning_line()
            elif self.check_draw():
                self.handle_game_end("🤝 It's a Draw!")
                self.scores['Draw'] += 1
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                color = self.colors['x_color'] if self.current_player == 'X' else self.colors['o_color']
                self.status_label.configure(text=f"🎯 Player {self.current_player}'s Turn", fg=color)

            self.update_scoreboard()

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != '':
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def check_draw(self):
        return all(cell != '' for row in self.board for cell in row)

    def highlight_winning_line(self):
        winning_positions = []
        for i, row in enumerate(self.board):
            if row[0] == row[1] == row[2] != '':
                winning_positions = [(i, 0), (i, 1), (i, 2)]
                break
        if not winning_positions:
            for j in range(3):
                if self.board[0][j] == self.board[1][j] == self.board[2][j] != '':
                    winning_positions = [(0, j), (1, j), (2, j)]
                    break
        if not winning_positions:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
                winning_positions = [(0, 0), (1, 1), (2, 2)]
            elif self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
                winning_positions = [(0, 2), (1, 1), (2, 0)]
        for row, col in winning_positions:
            self.buttons[row][col].configure(bg=self.colors['win_highlight'])

    def handle_game_end(self, message):
        self.game_over = True
        self.status_label.configure(text=message, fg=self.colors['win_highlight'])
        self.window.after(1000, lambda: self.show_game_over_message(message))

    def show_game_over_message(self, message):
        messagebox.showinfo("Game Over", f"{message}\n\nStarting new game in 2 seconds...")
        self.window.after(2000, self.new_game)

    def update_scoreboard(self):
        self.x_score_label.configure(text=str(self.scores['X']))
        self.o_score_label.configure(text=str(self.scores['O']))
        self.draw_score_label.configure(text=str(self.scores['Draw']))

    def new_game(self):
        self.board = [['', '', ''], ['', '', ''], ['', '', '']]
        self.current_player = 'X'
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text='', bg=self.colors['secondary'], fg=self.colors['text'])
        self.status_label.configure(text=f"🎯 Player {self.current_player}'s Turn", fg=self.colors['x_color'])

    def reset_scores(self):
        if messagebox.askyesno("Reset Scores", "Are you sure you want to reset all scores?"):
            self.scores = {'X': 0, 'O': 0, 'Draw': 0}
            self.update_scoreboard()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
