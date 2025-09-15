import tkinter as tk
from tkinter import messagebox
import random
import pygame

# Initialize pygame for sounds
pygame.mixer.init()

def play_sound(file):
    try:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
    except:
        pass

# Helper function to interpolate colors
def interpolate_color(c1, c2, t):
    # c1, c2 are '#RRGGBB', t in [0,1]
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f'#{r:02x}{g:02x}{b:02x}'

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title('KIZHI Tic Tac Toe')
        self.current_player = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []
        self.button_colors = []
        self.ai_level = 'medium'
        self.vs_ai = True
        self.dark_mode = True

        self.create_ui()

    # ------------------------- Methods -------------------------
    def set_mode(self, mode):
        self.vs_ai = (mode == 'PVC')
        self.reset_game()

    def set_level(self, level):
        self.ai_level = level

    def switch_theme(self):
        self.dark_mode = not self.dark_mode
        bg = 'black' if self.dark_mode else 'white'
        fg = 'white' if self.dark_mode else 'black'
        self.frame.config(bg=bg)
        self.bottom_frame.config(bg=bg)
        self.title_label.config(bg=bg, fg=fg)
        self.turn_label.config(bg=bg, fg=fg)
        for i, btn in enumerate(self.buttons):
            btn.config(fg=fg, bg=self.button_colors[i])

    def player_move(self, idx):
        if self.board[idx] == '':
            self.board[idx] = self.current_player
            self.buttons[idx].config(text=self.current_player)
            play_sound('move.mp3')
            if self.check_winner(self.current_player):
                play_sound('win.mp3')
                winner = 'Player 1' if self.current_player == 'X' else ('Player 2' if not self.vs_ai else 'AI')
                messagebox.showinfo('Game Over', f'{winner} ({self.current_player}) wins!')
                self.reset_game()
                return
            elif '' not in self.board:
                messagebox.showinfo('Game Over', 'Draw!')
                self.reset_game()
                return

            # Switch turn
            if self.vs_ai:
                if self.current_player == 'X':
                    self.current_player = 'O'
                    self.turn_label.config(text='Turn: AI (O)')
                    self.root.after(500, self.ai_move)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                player_text = 'Player 1 (X)' if self.current_player == 'X' else 'Player 2 (O)'
                self.turn_label.config(text=f'Turn: {player_text}')

    def ai_move(self):
        idx = self.get_ai_move()
        if idx is not None:
            self.board[idx] = 'O'
            self.buttons[idx].config(text='O')
            play_sound('move.mp3')
            if self.check_winner('O'):
                play_sound('win.mp3')
                messagebox.showinfo('Game Over', 'AI (O) wins!')
                self.reset_game()
                return
            self.current_player = 'X'
            self.turn_label.config(text='Turn: Player 1 (X)')

    def get_ai_move(self):
        empty = [i for i, v in enumerate(self.board) if v == '']
        if not empty:
            return None
        if self.ai_level == 'low':
            return random.choice(empty)
        elif self.ai_level == 'medium':
            if random.random() < 0.5:
                return random.choice(empty)
            else:
                return self.minimax('O')['index']
        else:
            return self.minimax('O')['index']

    def minimax(self, player):
        opponent = 'O' if player == 'X' else 'X'
        empty = [i for i, v in enumerate(self.board) if v == '']
        if self.check_winner('O'):
            return {'score': 1}
        elif self.check_winner('X'):
            return {'score': -1}
        elif not empty:
            return {'score': 0}
        moves = []
        for i in empty:
            self.board[i] = player
            result = self.minimax(opponent)
            moves.append({'index': i, 'score': result['score']})
            self.board[i] = ''
        return max(moves, key=lambda x: x['score']) if player == 'O' else min(moves, key=lambda x: x['score'])

    def show_hint(self):
        if self.vs_ai:
            hint = self.minimax('X')['index']
            messagebox.showinfo('Hint', f'Best move: {hint+1}')
        else:
            messagebox.showinfo('Hint', 'Hint available only in PVC mode')

    def check_winner(self, player):
        win_cond = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in win_cond:
            if self.board[a]==self.board[b]==self.board[c]==player:
                return True
        return False

    def reset_game(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        for i, btn in enumerate(self.buttons):
            btn.config(text='', bg=self.button_colors[i])
        self.turn_label.config(text='Turn: Player 1 (X)')

    # ------------------------- UI -------------------------
    def create_ui(self):
        self.root.state('zoomed')
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=5)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.title_label = tk.Label(self.root, text='KIZHI TIC TAC TOE', font=('Arial',36,'bold'), fg='white', bg='black')
        self.title_label.grid(row=0, column=0, sticky='nsew', pady=10)

        self.frame = tk.Frame(self.root, bg='black')
        self.frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)

        # Create buttons with smooth animation
        self.button_colors = ['#FF6F61','#6B5B95','#88B04B','#F7CAC9','#92A8D1','#955251','#B565A7','#009B77','#DD4124']
        for i in range(9):
            btn = tk.Button(self.frame, text='', font=('Arial',36,'bold'), bg=self.button_colors[i], fg='white',
                            relief='raised', bd=6, command=lambda idx=i: self.player_move(idx))
            btn.grid(row=i//3, column=i%3, sticky='nsew', padx=5, pady=5)
            self.add_hover_animation(btn, self.button_colors[i], '#FFFF00')  # Hover color yellow
            self.buttons.append(btn)

        self.bottom_frame = tk.Frame(self.root, bg='black')
        self.bottom_frame.grid(row=2, column=0, sticky='ew', pady=10)

        self.mode_var = tk.StringVar(value='PVC')
        tk.Label(self.bottom_frame, text='Mode:', bg='black', fg='white').pack(side='left', padx=5)
        tk.OptionMenu(self.bottom_frame, self.mode_var, 'PVC','PVP', command=self.set_mode).pack(side='left')

        self.level_var = tk.StringVar(value='medium')
        tk.Label(self.bottom_frame, text='AI Level:', bg='black', fg='white').pack(side='left', padx=5)
        tk.OptionMenu(self.bottom_frame, self.level_var, 'low','medium','tough', command=self.set_level).pack(side='left')

        self.hint_btn = tk.Button(self.bottom_frame, text='Hint', command=self.show_hint, bg='purple', fg='white', font=('Arial',12,'bold'), relief='raised', bd=4)
        self.hint_btn.pack(side='left', padx=5)
        self.theme_btn = tk.Button(self.bottom_frame, text='Switch Theme', command=self.switch_theme, bg='orange', fg='white', font=('Arial',12,'bold'), relief='raised', bd=4)
        self.theme_btn.pack(side='left', padx=5)
        self.reset_btn = tk.Button(self.bottom_frame, text='Reset', command=self.reset_game, bg='red', fg='white', font=('Arial',12,'bold'), relief='raised', bd=4)
        self.reset_btn.pack(side='left', padx=5)

        self.turn_label = tk.Label(self.root, text='Turn: Player 1 (X)', font=('Arial',18,'bold'), fg='white', bg='black')
        self.turn_label.grid(row=3, column=0, sticky='ew', pady=5)

    # ------------------------- Hover Animation -------------------------
    def add_hover_animation(self, btn, base_color, hover_color):
        steps = 10
        duration = 30  # ms per step

        def fade(to_color, step=0):
            if step > steps:
                return
            t = step / steps
            btn.config(bg=interpolate_color(btn.cget('bg'), to_color, t))
            self.root.after(duration, lambda: fade(to_color, step+1))

        def on_enter(event):
            fade(hover_color)

        def on_leave(event):
            fade(base_color)

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

# ------------------------- Run -------------------------
if __name__ == '__main__':
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
