import sys

from crossword.crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            # Get the length of the variable
            length = variable.length
            # Get the set of possible words for the variable
            words = self.domains[variable]
            # Create a new set to store the consistent words
            consistent_words = set()
            # Loop through each word in the original set
            for word in words:
                # Check if the word has the same length as the variable
                if len(word) == length:
                    # Add the word to the new set
                    consistent_words.add(word)
            # Update the domain of the variable with the new set
            self.domains[variable] = consistent_words

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Get the overlap between x and y
        overlap = self.crossword.overlaps[x, y]
        # If there is no overlap, return False
        if overlap is None:
            return False
        # Get the index of the overlapping letter for x and y
        i, j = overlap
        # Get the set of possible words for x and y
        words_x = self.domains[x]
        words_y = self.domains[y]
        # Create a new set to store the revised words for x
        revised_words_x = set()
        # Create a flag to indicate if a revision was made
        revised = False
        # Loop through each word in the original set for x
        for word_x in words_x:
            # Get the overlapping letter for x
            letter_x = word_x[i]
            # Create a flag to indicate if there is a consistent word for y
            consistent = False
            # Loop through each word in the set for y
            for word_y in words_y:
                # Get the overlapping letter for y
                letter_y = word_y[j]
                # Check if the letters match
                if letter_x == letter_y:
                    # Set the flag to True and break the loop
                    consistent = True
                    break
            # If there is a consistent word for y, add the word for x to the new set
            if consistent:
                revised_words_x.add(word_x)
            # Otherwise, set the revision flag to True
            else:
                revised = True
        # Update the domain of x with the new set
        self.domains[x] = revised_words_x
        # Return the revision flag
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each arc is arc-consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is None, initialize it with all the arcs in the problem
        if arcs is None:
            arcs = []
            # Loop through each variable
            for x in self.crossword.variables:
                # Loop through each neighbor of x
                for y in self.crossword.neighbors(x):
                    # Add the arc (x, y) to the list
                    arcs.append((x, y))
        # Loop until there are no more arcs to process
        while arcs:
            # Pop an arc from the list
            x, y = arcs.pop()
            # Try to revise the domain of x with respect to y
            if self.revise(x, y):
                # If x's domain is empty, return False
                if len(self.domains[x]) == 0:
                    return False
                # Otherwise, add all the arcs (z, x) to the list, where z is a neighbor of x other than y
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))
        # Return True if all domains are consistent
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if every variable in the crossword has a value assigned in the assignment
        return all(variable in assignment for variable in self.crossword.variables)


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if every value in the assignment is distinct
        if len(set(assignment.values())) != len(assignment):
            return False
        # Loop through each variable and value in the assignment
        for variable, value in assignment.items():
            # Check if the value has the same length as the variable
            if len(value) != variable.length:
                return False
            # Loop through each neighbor of the variable
            for neighbor in self.crossword.neighbors(variable):
                # If the neighbor is also assigned a value
                if neighbor in assignment:
                    # Get the overlap between the variable and the neighbor
                    i, j = self.crossword.overlaps[variable, neighbor]
                    # Check if the overlapping letters are different
                    if value[i] != assignment[neighbor][j]:
                        return False
        # Return True if all constraints are satisfied
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one that rules out the fewest values among the neighbors of `var`.
        """
        # Create a dictionary to store the number of values ruled out for each value in var's domain
        n_values = dict()
        # Loop through each value in var's domain
        for value in self.domains[var]:
            # Initialize the counter to zero
            n_values[value] = 0
            # Loop through each neighbor of var that is not assigned a value yet
            for neighbor in self.crossword.neighbors(var) - assignment.keys():
                # Get the overlap between var and neighbor
                i, j = self.crossword.overlaps[var, neighbor]
                # Loop through each value in neighbor's domain
                for value2 in self.domains[neighbor]:
                    # If the overlapping letters are different, increment the counter by one
                    if value[i] != value2[j]:
                        n_values[value] += 1
        # Sort the values by the number of values ruled out in ascending order and return them as a list
        return sorted(n_values.keys(), key=lambda x: n_values[x])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest degree.
        If there is a tie, any of the tied variables are acceptable return values.
        """
        # Create a list to store the unassigned variables
        unassigned = []
        # Loop through each variable in the crossword
        for variable in self.crossword.variables:
            # If the variable is not assigned a value yet, add it to the list
            if variable not in assignment:
                unassigned.append(variable)
                # Create a dictionary to store the number of remaining values and degree for each unassigned variable
                info = dict()
                # Loop through each unassigned variable
                for variable in unassigned:
                    # Get the number of remaining values in its domain
                    n_values = len(self.domains[variable])
                    # Get its degree (number of neighbors)
                    degree = len(self.crossword.neighbors(variable))
                    # Store them as a tuple in the dictionary
                    info[variable] = (n_values, degree)
               
                # Sort the unassigned variables by their number of remaining values in ascending order
                sorted_by_values = sorted(info.keys(), key=lambda x: info[x][0])
                # Get the minimum number of remaining values
                min_values = info[sorted_by_values[0]][0]
                # Filter out any variables that have more than min_values remaining values
                candidates = [variable for variable in sorted_by_values if info[variable][0] == min_values]
                # If there is only one candidate left, return it
                if len(candidates) == 1:
                    return candidates[0]
                # Otherwise, sort them by their degree in descending order
                sorted_by_degree = sorted(candidates, key=lambda x: info[x][1], reverse=True)
                # Return any of them (the first one by default)
                return sorted_by_degree[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if the assignment is complete
        if self.assignment_complete(assignment):
            # Return the assignment as a solution
            return assignment
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)
        # Loop through each value in the domain of the variable in order
        for value in self.order_domain_values(var, assignment):
            # Create a copy of the assignment
            new_assignment = assignment.copy()
            # Assign the value to the variable in the copy
            new_assignment[var] = value
            # Check if the new assignment is consistent
            if self.consistent(new_assignment):
                # Recursively try to extend the new assignment
                result = self.backtrack(new_assignment)
                # If a solution is found, return it
                if result is not None:
                    return result
        # If no solution is found, return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
