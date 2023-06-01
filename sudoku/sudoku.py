import random

# Generate a Sudoku puzzle
def generate_puzzle():
    # Create an empty puzzle grid
    puzzle = [[0] * 9 for _ in range(9)]

    # Fill the diagonal 3x3 grids with random values
    for i in range(0, 9, 3):
        digits = list(range(1, 10))
        random.shuffle(digits)
        for j in range(3):
            for k in range(3):
                puzzle[i+j][i+k] = digits.pop()

    # Solve the puzzle to create a valid Sudoku
    solve_puzzle(puzzle)

    return puzzle

# Solve the Sudoku puzzle using backtracking
def solve_puzzle(puzzle):
    find = find_empty(puzzle)
    if not find:
        return True
    else:
        row, col = find

    for num in range(1, 10):
        if is_valid(puzzle, num, row, col):
            puzzle[row][col] = num

            if solve_puzzle(puzzle):
                return True

            puzzle[row][col] = 0

    return False

# Check if the given digit is valid at the given position
def is_valid(puzzle, num, row, col):
    # Check row
    for i in range(9):
        if puzzle[row][i] == num:
            return False

    # Check column
    for i in range(9):
        if puzzle[i][col] == num:
            return False

    # Check 3x3 grid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if puzzle[start_row + i][start_col + j] == num:
                return False

    return True

# Find an empty cell in the puzzle
def find_empty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

# Generate the HTML/CSS representation of the Sudoku puzzle
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
    <h1>Vamos a hacer demasiado billete con chatGPT</h1>
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

# Generate a Sudoku puzzle
puzzle = generate_puzzle()

# Copy the puzzle to create an incomplete version
incomplete_puzzle = [row.copy() for row in puzzle]

# Remove clues to create an incomplete puzzle
difficulty = "medium"
clues_to_remove = {
    "easy": 35,
    "medium": 45,
    "hard": 55
}
num_clues = clues_to_remove[difficulty]

for _ in range(num_clues):
    while True:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if incomplete_puzzle[row][col] != 0:
            incomplete_puzzle[row][col] = 0
            break

# Solve the complete puzzle
solved_puzzle = [row.copy() for row in puzzle]
solve_puzzle(solved_puzzle)

# Generate the HTML/CSS representations
html_incomplete = generate_html(incomplete_puzzle)
html_solved = generate_html(solved_puzzle)

# Save the HTML representations to files
with open("sudoku_puzzle_incomplete.html", "w") as file:
    file.write(html_incomplete)

with open("sudoku_puzzle_solved.html", "w") as file:
    file.write(html_solved)

