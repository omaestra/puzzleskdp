import sys
import random
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw


class SudokuPuzzle:
    class DIFFICULTY(Enum):
        EASY = "easy"
        MEDIUM = "medium"
        HARD = "hard"
        
    def __init__(self, difficulty):
        self.puzzle = [[0] * 9 for _ in range(9)]
        self.incomplete_puzzle = None
        self.solved_puzzle = None
        self.difficulty = SudokuPuzzle.DIFFICULTY(difficulty)

    def clues_to_remove(self):
        if self.difficulty == SudokuPuzzle.DIFFICULTY.EASY: return 35
        if self.difficulty == SudokuPuzzle.DIFFICULTY.MEDIUM: return 45
        if self.difficulty == SudokuPuzzle.DIFFICULTY.HARD: return 55

    def generate_puzzle(self):
        self._fill_diagonal_grids()
        self._solve_puzzle()
        return self.puzzle

    def generate_incomplete_puzzle(self):
        incomplete_puzzle = [row.copy() for row in self.puzzle]
        num_clues = self.clues_to_remove()

        for _ in range(num_clues):
            while True:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if incomplete_puzzle[row][col] != 0:
                    incomplete_puzzle[row][col] = 0
                    break

        return incomplete_puzzle

    def _fill_diagonal_grids(self):
        for i in range(0, 9, 3):
            digits = list(range(1, 10))
            random.shuffle(digits)
            for j in range(3):
                for k in range(3):
                    self.puzzle[i+j][i+k] = digits.pop()

    def _solve_puzzle(self):
        find = self._find_empty()
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if self._is_valid(num, row, col):
                self.puzzle[row][col] = num

                if self._solve_puzzle():
                    return True

                self.puzzle[row][col] = 0

        return False

    def _is_valid(self, num, row, col):
        for i in range(9):
            if self.puzzle[row][i] == num:
                return False

        for i in range(9):
            if self.puzzle[i][col] == num:
                return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.puzzle[start_row + i][start_col + j] == num:
                    return False

        return True

    def _find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    return i, j
        return None

def generate_html(puzzle):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sudoku Puzzle</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            .grid {
                display: grid;
                grid-template-columns: repeat(9, 1fr);
                grid-template-rows: repeat(9, 1fr);
                
                border: 2px solid #333;
                
                width: max-content;
                margin: 50px auto;
                border-radius: 10px;
                background-color: #fff;
                font-family: Arial, sans-serif;
                font-size: 24px;
                font-weight: bold;
                overflow: hidden;
            }
            .cell {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
                width: 50px;
                padding: 8px;
                border: 1px solid #333;
            }
            .cell.small-grid {
                background-color: #f0f0f0;
            }
            .cell.empty {
                color: #aaa;
            }
        </style>
    </head>
    <body>
        <div class="grid">
    """

    for i in range(9):
        for j in range(9):
            value = puzzle[i][j]
            cell_class = "cell"
            if (i // 3) % 2 == (j // 3) % 2:
                cell_class += " small-grid"
            if value == 0:
                cell_class += " empty"
                value = ""
            html += f'            <div class="{cell_class}">{value}</div>\n'

    html += """
        </div>
    </body>
    </html>
    """

    return html


def generate_puzzle(difficulty):
    puzzle = SudokuPuzzle(difficulty=difficulty)
    generated_puzzle = puzzle.generate_puzzle()
    
    solved_puzzle = [row.copy() for row in generated_puzzle]
    incomplete_puzzle = puzzle.generate_incomplete_puzzle()

    puzzle.incomplete_puzzle = incomplete_puzzle
    puzzle.solved_puzzle = solved_puzzle

    return (puzzle)

def generate_html_file(puzzle, output_file):
    html = generate_html(puzzle)

    with open("{}.html".format(output_file), "w") as file:
        file.write(html)

    return (html)

def generate_sudoku_grid(puzzle, output_file):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    ax.set_xlim([0, 9])
    ax.set_ylim([0, 9])
    ax.axis("off")

    # Draw the main grid
    for i in range(9):
        for j in range(9):
            cell_color = "white"
            if (i // 3 + j // 3) % 2 == 0:
                cell_color = "#f2f2f2"  # Light gray

            rect = Rectangle((j, i), 1, 1, linewidth=0.5, edgecolor="gray", facecolor=cell_color)
            ax.add_patch(rect)

            if puzzle[i][j] != 0:
                ax.text(j + 0.5, i + 0.5, str(puzzle[i][j]), color="black",
                        fontsize=16, ha="center", va="center")

    # Draw the outer border
    #outer_border = Rectangle((0, 0), 9, 9, linewidth=2, edgecolor="black", facecolor="none")
    #ax.add_patch(outer_border)

    # Draw the inner grid lines (excluding top and left edges)
    for i in range(3, 9):
        ax.axhline(i, color="gray", linewidth=1)
        ax.axvline(i, color="gray", linewidth=1)
        
    plt.tight_layout()
    plt.savefig("{}.png".format(output_file), transparent=True, dpi=300)
    #plt.savefig("{}.png".format(output_file), transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close()

def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python sudoku.py {{ difficulty }} {{ times }} [output]")

    difficulty = sys.argv[1]
    times = int(sys.argv[2])

    for i in range(times):
        puzzle = generate_puzzle(difficulty)

        #generate_html_file(puzzle.solved_puzzle, "puzzle_solved_{}".format(i))
        #generate_html_file(puzzle.incomplete_puzzle, "puzzle_incomplete_{}".format(i))

        generate_sudoku_grid(puzzle.solved_puzzle, "puzzle_solved_{0}_{1}".format(difficulty, i))
        generate_sudoku_grid(puzzle.incomplete_puzzle, "puzzle_{0}_{1}".format(difficulty, i))

if __name__ == "__main__":
    main()