import random
from string import ascii_uppercase


def generate_word_search(words):
    size = max(len(word) for word in words)
    grid = [[' ' for _ in range(size)] for _ in range(size)]
    word_positions = {}  # Dictionary to store the positions of the words
    sorted_words = sorted(words, key=len)
    
    for word in words:
        word = word.upper()
        placed = False
        attempts = 0
        max_attempts = 100  # Maximum number of attempts to find a valid placement

        while not placed and attempts < max_attempts:
            direction = random.choice(['horizontal', 'vertical', 'diagonal'])
            row, col = random.randint(0, size - 1), random.randint(0, size - 1)

            if direction == 'horizontal':
                if col + len(word) <= size:
                    valid_placement = True
                    for i in range(len(word)):
                        if grid[row][col + i] != ' ' and grid[row][col + i] != word[i]:
                            valid_placement = False
                            break
                    if valid_placement:
                        for i in range(len(word)):
                            grid[row][col + i] = word[i]
                            word_positions[(row, col + i)] = word
                        placed = True

            elif direction == 'vertical':
                if row + len(word) <= size:
                    valid_placement = True
                    for i in range(len(word)):
                        if grid[row + i][col] != ' ' and grid[row + i][col] != word[i]:
                            valid_placement = False
                            break
                    if valid_placement:
                        for i in range(len(word)):
                            grid[row + i][col] = word[i]
                            word_positions[(row + i, col)] = word
                        placed = True

            elif direction == 'diagonal':
                if row + len(word) <= size and col + len(word) <= size:
                    valid_placement = True
                    for i in range(len(word)):
                        if grid[row + i][col + i] != ' ' and grid[row + i][col + i] != word[i]:
                            valid_placement = False
                            break
                    if valid_placement:
                        for i in range(len(word)):
                            grid[row + i][col + i] = word[i]
                            word_positions[(row + i, col + i)] = word
                        placed = True

            attempts += 1

    letters = ascii_uppercase#.replace('Q', '')

    for row in range(size):
        for col in range(size):
            if grid[row][col] == ' ':
                grid[row][col] = random.choice(letters)

    return grid, word_positions


def generate_html_template(grid, word_positions):
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


def main():
        # Ask the user for the number of words
    num_words = int(input("Enter the number of words: "))

    # Ask the user to provide a list of words
    words = []
    for i in range(num_words):
        word = input(f"Enter word {i+1}: ")
        words.append(word.upper())
        
    grid, word_positions = generate_word_search(words)
    template = generate_html_template(grid, word_positions)

    with open('word_search_puzzle.html', 'w') as f:
        f.write(template)

    print('Word search puzzle generated successfully.')


if __name__ == '__main__':
    main()


