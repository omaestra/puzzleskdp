class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with starting point, direction, and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == Variable.DOWN else 0),
                 self.j + (k if self.direction == Variable.ACROSS else 0))
            )

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.direction == other.direction) and
            (self.length == other.length)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():

    def __init__(self, structure_file, words_file):

        # Determine structure of crossword
        with open(structure_file) as f:
            contents = f.read().splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            self.structure = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    if j >= len(contents[i]):
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                self.structure.append(row)

        # Save vocabulary list
        with open(words_file) as f:
            self.words = set(f.read().upper().splitlines())

        # Determine variable set
        self.variables = set()
        for i in range(self.height):
            for j in range(self.width):

                # Vertical words
                starts_word = (
                    self.structure[i][j]
                    and (i == 0 or not self.structure[i - 1][j])
                )
                if starts_word:
                    length = 1
                    for k in range(i + 1, self.height):
                        if self.structure[k][j]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.DOWN,
                            length=length
                        ))

                # Horizontal words
                starts_word = (
                    self.structure[i][j]
                    and (j == 0 or not self.structure[i][j - 1])
                )
                if starts_word:
                    length = 1
                    for k in range(j + 1, self.width):
                        if self.structure[i][k]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.ACROSS,
                            length=length
                        ))

        # Compute overlaps for each word
        # For any pair of variables v1, v2, their overlap is either:
        #    None, if the two variables do not overlap; or
        #    (i, j), where v1's ith character overlaps v2's jth character
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )

    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var]
        )

class Structure:

    def __init__(self, size):
        """
        Create a new structure with a given size.
        `size` is a tuple of (rows, columns).
        """
        # Store the size as an attribute
        self.size = size
        # Initialize an empty set of variables
        self.variables = set()
        # Initialize the score to zero
        self.score = 0
        # Initialize a dictionary of overlaps
        self.overlaps = dict()

    def add_variable(self, variable):
        """
        Add a variable to the structure if it is valid.
        `variable` is an instance of Variable class.
        Return True if the variable is added; return False otherwise.
        """
        # Check if the variable fits in the grid
        if not self.in_bounds(variable):
            return False
        # Check if the variable overlaps with any existing variable
        if self.overlaps_with(variable):
            return False
        # Add the variable to the set
        self.variables.add(variable)
        # Update the score based on some criteria
        self.update_score(variable)
        # Update the overlaps dictionary
        self.update_overlaps(variable)
        # Return True if successful
        return True

    def in_bounds(self, variable):
        """
        Check if a variable is within the bounds of the grid.
        `variable` is an instance of Variable class.
        Return True if it is in bounds; return False otherwise.
        """
        # Get the size of the grid
        rows, columns = self.size
        # Get the position and length of the variable
        i, j = variable.i, variable.j
        length = variable.length
        # Check if the variable is horizontal or vertical
        if variable.direction == Variable.ACROSS:
            # Check if the variable exceeds the right or left edge of the grid
            if j < 0 or j + length > columns:
                return False
        else:
            # Check if the variable exceeds the top or bottom edge of the grid
            if i < 0 or i + length > rows:
                return False
        # Return True if none of the above conditions are met
        return True

    def overlaps_with(self, variable):
        """
        Check if a variable overlaps with any existing variable in the structure.
        `variable` is an instance of Variable class.
        Return True if it overlaps; return False otherwise.
        """
        
        # Loop through each existing variable in the structure
        for other in self.variables:
           # Get their positions and lengths
           i1, j1 = variable.i, variable.j
           i2, j2 = other.i, other.j
           l1 = variable.length
           l2 = other.length
           # Check if both variables are horizontal
           if variable.direction == Variable.ACROSS and other.direction == Variable.ACROSS:
              # Check if they have the same row and overlapping columns
              if i1 == i2 and (j1 <= j2 < j1 + l1 or j2 <= j1 < j2 + l2):
                 return True
           # Check if both variables are vertical
           elif variable.direction == Variable.DOWN and other.direction == Variable.DOWN:
              # Check if they have the same column and overlapping rows
              if j1 == j2 and (i1 <= i2 < i1 + l1 or i2 <= i1 < i2 + l2):
                 return True
           # Check if one variable is horizontal and the other is vertical
           elif variable.direction != other.direction:
              # Get the horizontal and vertical variables
              horizontal = variable if variable.direction == Variable.ACROSS else other
              vertical = other if other.direction == Variable.DOWN else variable
              # Get their positions and lengths
              i_h, j_h = horizontal.i, horizontal.j
              i_v, j_v = vertical.i, vertical.j
              l_h = horizontal.length
              l_v = vertical.length
              # Check if they intersect at any point
              if i_h >= i_v and i_h < i_v + l_v and j_v >= j_h and j_v < j_h + l_h:
                 return True
        # Return False if none of the above conditions are met
        return False
