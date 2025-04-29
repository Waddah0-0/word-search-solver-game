# Boggle Game Solver

A Python implementation of the classic Boggle word game with a graphical interface using Tkinter. This repository includes:

- **Board generation**: Random 4×4 (or custom size) letter grid.
- **Dictionary lookup**: Uses a Trie for efficient prefix and word checks based on `words.txt`.
- **Backtracking solver**: Finds all valid words on the board using depth‑first search and prefix pruning.
- **Graphical UI**: Player can start a timed game, enter words, see live score and final results.

---

## 📂 Repository Structure

```plain
├── README.md           # This file
├── board.py            # Board class and neighbor logic
├── trie.py             # Trie implementation and dictionary loader
├── solver.py           # Backtracking Boggle solver
├── gui.py              # Tkinter-based game interface
└── words.txt           # Newline-delimited word list (dictionary)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or newer
- Tkinter (usually included with standard Python installations)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/boggle-solver.git
   cd boggle-solver
   ```
2. Ensure you have a `words.txt` file in the root. You can use the included sample or generate your own word list.

### Running the Game

```bash
python gui.py
```

- Click **Start Game** to generate a new board and begin the timer.
- Type words into the entry box and press **Submit**.
- Your score updates in real time; when time expires, all possible words are revealed.

---

## 🛠️ Customization

- **Board size**: In `gui.py`, modify `board_size` when creating `BoggleGUI`, e.g. `BoggleGUI(board_size=5)`.  
- **Time limit**: In `gui.py`, modify `time_limit` in seconds, e.g. `BoggleGUI(time_limit=120)`.  
- **Dictionary**: Replace or expand `words.txt` with any newline-separated word list.  
- **Scoring rules**: Adjust the `SCORING` dictionary in `gui.py` to change points per word length.

---

## 📖 Usage Examples

- **Solver only**: Run the command-line solver to list words on a fixed board:
  ```bash
  python solver.py
  ```

- **Board display**: Test the board and neighbor logic:
  ```bash
  python main_board_test.py  # if you add a simple test script
  ```

---


