import tkinter as tk 
from tkinter import messagebox 
import time
import sys
import os

# Add the parent directory of 'solver' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Ensure the 'solver' module is accessible
if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'solver')):
    raise ImportError("The 'solver' module could not be found. Ensure it exists in the parent directory.")
from solver.board import Board
from solver.trie import build_trie_from_file
from solver.solver import find_words, suggest_word

# Boggle scoring rules
SCORING = {3: 1, 4: 1, 5: 2, 6: 3, 7: 5}

class BoggleGUI(tk.Tk): # Boggle game GUI
    def __init__(self, board_size=4, time_limit=180):
        super().__init__()
        self.title("Boggle Game")
        self.board_size = board_size
        self.time_limit = time_limit
        self.remaining = time_limit
        self.board = None
        self.trie = None
        self.all_valid = set()
        self.found = set()
        self.score = 0
        self.mode = "user"  # Default mode
        self.create_widgets()

    def create_widgets(self): # Create GUI components
        # Mode selection
        mode_frame = tk.Frame(self)
        mode_frame.pack(pady=5)
        tk.Label(mode_frame, text="Select Mode:").pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="user")
        tk.Radiobutton(mode_frame, text="User", variable=self.mode_var, value="user").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="AI Solve", variable=self.mode_var, value="ai").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Assisted", variable=self.mode_var, value="assist").pack(side=tk.LEFT)

        # Board frame
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(pady=10)
        self.letter_labels = [[None]*self.board_size for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                lbl = tk.Label(self.board_frame, text=" ", width=4, height=2,
                               font=("Helvetica", 20), borderwidth=2, relief="ridge")
                lbl.grid(row=i, column=j, padx=2, pady=2)
                self.letter_labels[i][j] = lbl

        # Entry and submit
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=5)
        self.entry = tk.Entry(entry_frame, font=("Helvetica", 14))
        self.entry.pack(side=tk.LEFT, padx=(0,10))
        self.submit_btn = tk.Button(entry_frame, text="Submit", command=self.submit_word)
        self.submit_btn.pack(side=tk.LEFT)

        # Info label
        self.info_label = tk.Label(self, text="Score: 0    Time: 0", font=("Helvetica", 14))
        self.info_label.pack(pady=5)

        # Found words list
        self.listbox = tk.Listbox(self, height=10, width=20)
        self.listbox.pack(pady=5)

        # Control buttons
        ctrl_frame = tk.Frame(self)
        ctrl_frame.pack(pady=5)
        self.start_btn = tk.Button(ctrl_frame, text="Start Game", command=self.start_game)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.quit_btn = tk.Button(ctrl_frame, text="Quit", command=self.destroy)
        self.quit_btn.pack(side=tk.LEFT, padx=5)

    def start_game(self): # Start a new game
        # Initialize game
        self.mode = self.mode_var.get()  # Get selected mode
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

        # Update board display
        for i in range(self.board_size): 
            for j in range(self.board_size): # Fill in letters
                self.letter_labels[i][j].config(text=self.board.grid[i][j])

        self.listbox.delete(0, tk.END)
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.start_btn.config(state="disabled")
        self.update_info()

        if self.mode == "ai":
            self.solve_with_ai()
        elif self.mode == "assist":
            self.after(5000, self.suggest_word)  # Suggest a word every 5 seconds
        else:
            self.after(1000, self.countdown)

    def solve_with_ai(self):
        """AI solves the board and displays all valid words."""
        self.listbox.delete(0, tk.END)
        for word in sorted(self.all_valid):
            pts = SCORING.get(len(word), 11 if len(word) >= 8 else 0)
            self.listbox.insert(tk.END, f"{word} (+{pts})")
        messagebox.showinfo("AI Solve", f"AI found {len(self.all_valid)} words! Total score: {sum(SCORING.get(len(w), 11 if len(w) >= 8 else 0) for w in self.all_valid)}")
        self.start_btn.config(state="normal")

    def suggest_word(self):
        """Suggest a word to the user in Assisted mode."""
        if self.mode == "assist" and self.remaining > 0:
            suggestion = suggest_word(self.all_valid, self.found)
            if suggestion:
                messagebox.showinfo("Suggestion", f"Try this word: {suggestion}")
            self.after(5000, self.suggest_word)  # Continue suggesting words

    def submit_word(self): # Handle word submission
        # Get word from entry, check validity, and update score
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

    def countdown(self):    # Countdown timer
        if self.remaining > 0: 
            self.remaining -= 1 # Decrease remaining time
            self.update_info() # Update time display
            self.after(1000, self.countdown)
        else:
            self.end_game()

    def update_info(self): # Update score and time display
        self.info_label.config(text=f"Score: {self.score}    Time: {self.remaining}")

    def end_game(self):
        messagebox.showinfo("Time's up", f"Game over! Your score: {self.score}")
        # Reveal all words
        for w in sorted(self.all_valid):
            mark = "*" if w in self.found else " "
            pts = SCORING.get(len(w), 11 if len(w) >= 8 else 0)
            self.listbox.insert(tk.END, f"{mark} {w} ({pts})")
        self.start_btn.config(state="normal")

if __name__ == '__main__':
    app = BoggleGUI(board_size=4, time_limit=120)
    app.mainloop()