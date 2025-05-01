import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for modern widgets
import time
import sys
import os


# Add the parent directory of 'solver' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'solver')):
    raise ImportError("The 'solver' module could not be found. Ensure it exists in the parent directory.")
from solver.board import Board
from solver.trie import build_trie_from_file
from solver.solver import find_words, suggest_word 

SCORING = {3: 1, 4: 1, 5: 2, 6: 3, 7: 5}

class BoggleGUI(tk.Tk):
    def __init__(self, board_size=4, time_limit=180):
        super().__init__()
        self.title("AL Dar Word Game")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Use a modern theme
        self.board_size = board_size
        self.time_limit = time_limit
        self.remaining = time_limit
        self.board = None
        self.trie = None
        self.all_valid = set()
        self.found = set()
        self.score = 0
        self.mode = "user"
        self.create_widgets()

    def create_widgets(self):
        # Mode selection
        mode_frame = ttk.Frame(self, padding=10)
        mode_frame.pack(pady=5)
        ttk.Label(mode_frame, text="Select Mode:").pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="user")
        ttk.Radiobutton(mode_frame, text="User", variable=self.mode_var, value="user").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="AI Solve", variable=self.mode_var, value="ai").pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="Assisted", variable=self.mode_var, value="assist").pack(side=tk.LEFT)

        # Board frame
        self.board_frame = ttk.Frame(self, padding=10)
        self.board_frame.pack(pady=10)
        self.letter_labels = [[None] * self.board_size for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                lbl = ttk.Label(self.board_frame, text=" ", width=4, anchor="center",
                                font=("Helvetica", 20), relief="ridge", borderwidth=2)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.letter_labels[i][j] = lbl

        # Entry and submit
        entry_frame = ttk.Frame(self, padding=10)
        entry_frame.pack(pady=5)
        self.entry = ttk.Entry(entry_frame, font=("Helvetica", 14), width=20)
        self.entry.pack(side=tk.LEFT, padx=(0, 10))
        self.submit_btn = ttk.Button(entry_frame, text="Submit", command=self.submit_word)
        self.submit_btn.pack(side=tk.LEFT)

        # Info label
        self.info_label = ttk.Label(self, text="Score: 0    Time: 0", font=("Helvetica", 14))
        self.info_label.pack(pady=5)

        # Found words list
        self.listbox = tk.Listbox(self, height=10, width=20, font=("Helvetica", 12), borderwidth=2, relief="ridge")
        self.listbox.pack(pady=5)

        # Control buttons
        ctrl_frame = ttk.Frame(self, padding=10)
        ctrl_frame.pack(pady=5)
        self.start_btn = ttk.Button(ctrl_frame, text="Start Game", command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.quit_btn = ttk.Button(ctrl_frame, text="Quit", command=self.destroy)
        self.quit_btn.pack(side=tk.LEFT, padx=5)

    def start_game(self):
        self.mode = self.mode_var.get()
        self.board = Board(size=self.board_size)
        words_file_path = os.path.join(os.path.dirname(__file__), '..', 'words.txt')
        if not os.path.exists(words_file_path):
            messagebox.showerror("Error", "The 'words.txt' file is missing. Please add it to the project directory.")
            self.start_btn.config(state="normal")
            return

        self.trie = build_trie_from_file(words_file_path)
        self.all_valid = find_words(self.board, self.trie)
        self.found.clear()
        self.score = 0
        self.remaining = self.time_limit

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.letter_labels[i][j].config(text=self.board.grid[i][j])

        self.listbox.delete(0, tk.END)
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.start_btn.config(state="disabled")
        self.update_info()

        if self.mode == "ai":
            self.solve_with_ai()
        elif self.mode == "assist":
            self.after(5000, self.suggest_word)
        else:
            self.after(1000, self.countdown)

    def solve_with_ai(self):
        self.listbox.delete(0, tk.END)
        for word in sorted(self.all_valid):
            pts = SCORING.get(len(word), 11 if len(word) >= 8 else 0)
            self.listbox.insert(tk.END, f"{word} (+{pts})")
        messagebox.showinfo("AI Solve", f"AI found {len(self.all_valid)} words! Total score: {sum(SCORING.get(len(w), 11 if len(w) >= 8 else 0) for w in self.all_valid)}")
        self.start_btn.config(state="normal")

    def suggest_word(self):
        if self.mode == "assist" and self.remaining > 0:
            suggestion = suggest_word(self.all_valid, self.found)
            if suggestion:
                messagebox.showinfo("Suggestion", f"Try this word: {suggestion}")
            self.after(5000, self.suggest_word)

    def submit_word(self):
        word = self.entry.get().strip().upper()
        self.entry.delete(0, tk.END)
        if not word:
            return
        if word in self.found:
            messagebox.showinfo("Info", f"Already found '{word}'")
        elif word in self.all_valid:
            self.found.add(word)
            pts = SCORING.get(len(word), 11 if len(word) >= 8 else 0)
            self.score += pts
            self.listbox.insert(tk.END, f"{word} (+{pts})")
        else:
            messagebox.showwarning("Invalid", f"'{word}' not on board or not valid.")
        self.update_info()

    def countdown(self):
        if self.remaining > 0:
            self.remaining -= 1
            self.update_info()
            self.after(1000, self.countdown)
        else:
            self.end_game()

    def update_info(self):
        self.info_label.config(text=f"Score: {self.score}    Time: {self.remaining}")

    def end_game(self):
        messagebox.showinfo("Time's up", f"Game over! Your score: {self.score}")
        for w in sorted(self.all_valid):
            mark = "*" if w in self.found else " "
            pts = SCORING.get(len(w), 11 if len(w) >= 8 else 0)
            self.listbox.insert(tk.END, f"{mark} {w} ({pts})")
        self.start_btn.config(state="normal")

if __name__ == '__main__':
    app = BoggleGUI(board_size=4, time_limit=120)
    app.mainloop()