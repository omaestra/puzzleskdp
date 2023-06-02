import sys
import random
from enum import Enum

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

    def generate_html(self, puzzle):
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
    
    puzzle.generate_html(generated_puzzle)
    html_incomplete = puzzle.generate_html(incomplete_puzzle)
    html_solved = puzzle.generate_html(solved_puzzle)

    return (html_incomplete, html_solved)

def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python sudoku.py {{ difficulty }} {{ times }} [output]")

    difficulty = sys.argv[1]
    times = int(sys.argv[2])

    for i in range(times):
        (html_incomplete, html_solved) = generate_puzzle(difficulty)

        with open("sudoku_puzzle_incomplete_{}.html".format(i), "w") as file:
            file.write(html_incomplete)

        with open("sudoku_puzzle_solved_{}.html".format(i), "w") as file:
            file.write(html_solved)

if __name__ == "__main__":
    main()