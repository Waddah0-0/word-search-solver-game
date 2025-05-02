import tkinter as tk # Import the tkinter library for GUI creation
from tkinter import messagebox # Import messagebox for displaying messages
from tkinter import ttk  # Import ttk for modern widgets
import time # For time-related functions
import random  # For random number generation
import sys # For system-specific parameters and functions
import os # For file and directory manipulation
# Also ensures the script is run from the correct directory


# Adds the parent directory of 'solver' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'solver')):
    raise ImportError("The 'solver' module could not be found. Ensure it exists in the parent directory.")
from solver.board import Board # Import the Board class from the solver module
from solver.trie import build_trie_from_file # Import the function to build a trie from a file
from solver.solver import find_words, suggest_word  # Import the functions to find words and suggest a word

SCORING = {3: 1, 4: 1, 5: 2, 6: 3, 7: 5} # Scoring dictionary for word lengths

class BoggleGUI(tk.Tk):
    def __init__(self, board_size=4, time_limit=180):
        super().__init__()
        self.title("word search game") # Set the title of the window
        self.style = ttk.Style(self)    # Create a style object for the GUI
        self.style.theme_use("clam")  # Use a modern theme
        self.board_size = board_size    # Set the size of the Boggle board
        self.time_limit = time_limit   # Set the time limit for the game
        self.remaining = time_limit # Initialize remaining time
        self.board = None # Initialize the board
        self.trie = None # Initialize the trie for word validation
        self.all_valid = set() # Set to store all valid words
        self.found = set() # Set to store found words
        self.score = 0 # Initialize score
        self.mode = "user" # Initialize game mode
        self.create_widgets() # Call the method to create the GUI widgets

    def create_widgets(self):   # Create the GUI widgets
        # Mode selection
        mode_frame = ttk.Frame(self, padding=10) # Create a frame for mode selection
        mode_frame.pack(pady=5) # Add padding around the frame
        ttk.Label(mode_frame, text="Select Mode:").pack(side=tk.LEFT, padx=5) # Label for mode selection
        self.mode_var = tk.StringVar(value="user") # Variable to store the selected mode
        ttk.Radiobutton(mode_frame, text="User", variable=self.mode_var, value="user").pack(side=tk.LEFT) # Radio button for user mode
        ttk.Radiobutton(mode_frame, text="AI Solve", variable=self.mode_var, value="ai").pack(side=tk.LEFT) # Radio button for AI mode
        ttk.Radiobutton(mode_frame, text="Assisted", variable=self.mode_var, value="assist").pack(side=tk.LEFT) # Radio button for assisted mode
        ttk.Label(mode_frame, text="Time Limit (seconds):").pack(side=tk.LEFT, padx=5) # Label for time limit

        # Board frame
        self.board_frame = ttk.Frame(self, padding=10) # Create a frame for the Boggle board
        self.board_frame.pack(pady=10) # Add padding around the frame
        self.letter_labels = [[None] * self.board_size for _ in range(self.board_size)] # Create a 2D list for letter labels
        for i in range(self.board_size): # Loop through the rows of the board
            for j in range(self.board_size): # Loop through the columns of the board
                lbl = ttk.Label(self.board_frame, text=" ", width=4, anchor="center", 
                                font=("Helvetica", 20), relief="ridge", borderwidth=2) # Create a label for each letter
                lbl.grid(row=i, column=j, padx=2, pady=2) # Place the label in the grid
                self.letter_labels[i][j] = lbl # Store the label in the 2D list

        # Entry and submit
        entry_frame = ttk.Frame(self, padding=10) # Create a frame for the entry and submit button
        entry_frame.pack(pady=5) # Add padding around the frame
        self.entry = ttk.Entry(entry_frame, font=("Helvetica", 14), width=20) # Create an entry widget for user input
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
        ctrl_frame = ttk.Frame(self, padding=10) # Create a frame for control buttons
        ctrl_frame.pack(pady=5) # Add padding around the frame
        self.start_btn = ttk.Button(ctrl_frame, text="Start Game", command=self.start_game) # Button to start the game
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.quit_btn = ttk.Button(ctrl_frame, text="Quit", command=self.destroy) # Button to quit the game
        self.quit_btn.pack(side=tk.LEFT, padx=5) # Pack the quit button

    def start_game(self): # Method to start the game
        self.mode = self.mode_var.get() # Get the selected mode from the radio buttons
        self.board = Board(size=self.board_size) # Create a new Boggle board
        words_file_path = os.path.join(os.path.dirname(__file__), '..', 'words.txt')
        if not os.path.exists(words_file_path): # Check if the words file exists
            messagebox.showerror("Error", "The 'words.txt' file is missing. Please add it to the project directory.")
            self.start_btn.config(state="normal")
            return

        self.trie = build_trie_from_file(words_file_path) # Build the trie from the words file
        self.all_valid = find_words(self.board, self.trie) # Find all valid words on the board
        self.found.clear() # Clear the set of found words
        self.score = 0 # Reset the score
        self.remaining = self.time_limit # Reset the remaining time

        for i in range(self.board_size): # Loop through the rows of the board
            for j in range(self.board_size): # Loop through the columns of the board
                self.letter_labels[i][j].config(text=self.board.grid[i][j])

        self.listbox.delete(0, tk.END)
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.start_btn.config(state="disabled")
        self.update_info()

        if self.mode == "ai": # If AI mode is selected
            self.solve_with_ai()
        elif self.mode == "assist": # If assisted mode is selected
            self.after(5000, self.suggest_word)
        else: # If user mode is selected
            self.after(1000, self.countdown)

    def solve_with_ai(self): # Method to solve the game using AI
        self.listbox.delete(0, tk.END) # Clear the listbox
        for word in sorted(self.all_valid): # Loop through all valid words
            pts = SCORING.get(len(word), 11 if len(word) >= 8 else 0) # Get the score for the word
            self.listbox.insert(tk.END, f"{word} (+{pts})") # Insert the word into the listbox with its score
        messagebox.showinfo("AI Solve", f"AI found {len(self.all_valid)} words! Total score: {sum(SCORING.get(len(w), 11 if len(w) >= 8 else 0) for w in self.all_valid)}")
        self.start_btn.config(state="normal") # Enable the start button again

    def suggest_word(self): # Method to suggest a word in assisted mode
        if self.mode == "assist" and self.remaining > 0:
            suggestion = suggest_word(self.all_valid, self.found)
            if suggestion:
                messagebox.showinfo("Suggestion", f"Try this word: {suggestion}")
            self.after(5000, self.suggest_word)

    def submit_word(self): # Method to submit a word
        word = self.entry.get().strip().upper()
        self.entry.delete(0, tk.END)
        if not word:
            return
        if word in self.found: # Check if the word has already been found
            messagebox.showinfo("Info", f"Already found '{word}'")
        elif word in self.all_valid: # Check if the word is valid
            self.found.add(word)
            pts = SCORING.get(len(word), 11 if len(word) >= 8 else 0)
            self.score += pts
            self.listbox.insert(tk.END, f"{word} (+{pts})")
        else:
            messagebox.showwarning("Invalid", f"'{word}' not on board or not valid.")
        self.update_info()

    def countdown(self): # Method to handle the countdown timer
        if self.remaining > 0:
            self.remaining -= 1
            self.update_info()
            self.after(1000, self.countdown)
        else:
            self.end_game()

    def update_info(self): # Method to update the info label with score and time
        self.info_label.config(text=f"Score: {self.score}    Time: {self.remaining}")

    def end_game(self): # Method to end the game
        messagebox.showinfo("Time's up", f"Game over! Your score: {self.score}")
        for w in sorted(self.all_valid): # Loop through all valid words
            mark = "*" if w in self.found else " "
            pts = SCORING.get(len(w), 11 if len(w) >= 8 else 0)
            self.listbox.insert(tk.END, f"{mark} {w} ({pts})") # Insert the words into the listbox with their scores
        self.start_btn.config(state="normal") # Enable the start button again

if __name__ == '__main__': 
    app = BoggleGUI(board_size=4, time_limit=180)
    app.mainloop()