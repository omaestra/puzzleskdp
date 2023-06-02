import random
import sys
from string import ascii_uppercase


def generate_word_search(words, size):
    """
    Generates a word search puzzle grid and word positions based on a set of words and grid size.

    Parameters:
    - words (list): A list of words to include in the puzzle.
    - size (int): The size of the word search grid.

    Returns:
    - grid (list): A 2D list representing the word search puzzle grid.
    - word_positions (dict): A dictionary mapping the positions of the words in the grid.
    """
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    word_positions = {}

    for word in words:
        word = word.upper()
        if word in word_positions:
            continue  # Skip duplicate words
        placed = False
        attempts = 0
        max_attempts = 100

        while not placed and attempts < max_attempts:
            direction = random.choice(['horizontal', 'vertical', 'diagonal'])
            row, col = random.randint(0, size - 1), random.randint(0, size - 1)

            if direction == 'horizontal':
                if col + len(word) <= size:
                    valid_placement = all(grid[row][col + i] in (' ', word[i]) for i in range(len(word)))
                    if valid_placement:
                        for i in range(len(word)):
                            grid[row][col + i] = word[i]
                            word_positions[(row, col + i)] = word
                        placed = True

            elif direction == 'vertical':
                if row + len(word) <= size:
                    valid_placement = all(grid[row + i][col] in (' ', word[i]) for i in range(len(word)))
                    if valid_placement:
                        for i in range(len(word)):
                            grid[row + i][col] = word[i]
                            word_positions[(row + i, col)] = word
                        placed = True

            elif direction == 'diagonal':
                if row + len(word) <= size and col + len(word) <= size:
                    valid_placement = all(grid[row + i][col + i] in (' ', word[i]) for i in range(len(word)))
                    if valid_placement:
                        for i in range(len(word)):
                            grid[row + i][col + i] = word[i]
                            word_positions[(row + i, col + i)] = word
                        placed = True

            attempts += 1

    for row in range(size):
        for col in range(size):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(ascii_uppercase)

    return grid, word_positions


def generate_html_template(grid, word_positions):
    """
    Generates an HTML template for displaying the word search puzzle grid.

    Parameters:
    - grid (list): A 2D list representing the word search puzzle grid.
    - word_positions (dict): A dictionary mapping the positions of the words in the grid.

    Returns:
    - template (str): The HTML template for displaying the word search puzzle grid.
    """
    size = len(grid)
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Word Search Puzzle</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
            .word-search {
                /* display: inline-block; */
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
            }
            .cell {
                width: 40px;
                height: 40px;
                text-align: center;
                line-height: 40px;
                border: 1px solid #ccc;
                font-weight: bold;
                font-size: 18px;
            }
            .highlight {
                background-color: yellow;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center mt-5">
                <div class="col">
                    <div class="word-search">
                        <div class="row justify-content-center mb-3">
                            <h3>Word Search Puzzle</h3>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col">
                                <div class="row justify-content-center">

    """

    for row in range(size):
        template += '<div class="grid-row">'
        for col in range(size):
            if (row, col) in word_positions:
                template += f'<div class="col cell highlight">{grid[row][col]}</div>'
            else:
                template += f'<div class="col cell">{grid[row][col]}</div>'
        template += '</div>'

    template += """
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    return template


def generate_word_search_puzzle(size, words_num, words_file):
    words = []
    with open(words_file) as f:
        words_list = list(f.read().upper().splitlines())
        words = random.sample(words_list, words_num)

    grid, word_positions = generate_word_search(words, size)
    template = generate_html_template(grid, word_positions)

    return template


def main():
    """
    Main entry point for executing the word search puzzle generation. 
    Parses command line arguments, generates the word search puzzle, and saves it to an HTML file.

    Command Line Arguments:
    - size (int): The size of the word search grid.
    - words_num (int): The number of words to include in the puzzle.
    - words_file (str): Path to a file containing the word vocabulary.
    - output (optional, str): Path to the output HTML file. If not provided, 'word_search_puzzle.html' will be used.

    Usage Example:
    ```
    python word_search_puzzle.py 10 5 vocabulary.txt
    ```

    This example generates a word search puzzle with a grid size of 10x10, including 5 words randomly selected from the vocabulary file 'vocabulary.txt'. The output is saved to 'word_search_puzzle.html'.
    """
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python word_search_puzzle.py <size> <words_num> <words_file> [output]")

    size = int(sys.argv[1])
    words_num = int(sys.argv[2])
    words_file = sys.argv[3]

    puzzle_html = generate_word_search_puzzle(size, words_num, words_file)

    output_file = 'word_search_puzzle.html'
    with open(output_file, 'w') as f:
        f.write(puzzle_html)

    print('Word search puzzle generated successfully.')

if __name__ == '__main__':
    main()