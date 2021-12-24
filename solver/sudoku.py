""" Module Representing a Sudoku Puzzle """
from typing import Optional, List

from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, PULP_CBC_CMD, value as v, lpSum, LpBinary, LpConstraint, \
    const, LpStatus

from solver.box import Box, DEFAULT_BOXES
from solver.cell import Cell


class Sudoku:
    """ A Model for a Sudoku Puzzle """

    def __init__(self, rows: int = 9, columns: int = 9, boxes: List[Box] = DEFAULT_BOXES,
                 givens_string: Optional[str] = None):
        # For now, only square-shaped sudokus are allowed
        assert rows == columns
        self.rows = rows
        self.columns = columns

        self.boxes = boxes
        self._validate_boxes()

        self.digits = {}
        if givens_string is not None:
            assert len(givens_string) == self.rows * self.columns
            # It is common to use either a . or 0 to represent an unknown value. This model uses 0 for consistency.
            givens_string = givens_string.replace(".", "0")
            self._add_givens_from_string(givens_string)

    def _add_givens_from_string(self, givens_string: str) -> None:
        """
        Add the given digits based on the string. 0s represent unknowns. All characters must be digits 0-9.

        Precondition: givens_string is equal in length to the number of cells in the sudoku (rows * columns)
        :param givens_string: The string of given and unknown digits
        """
        for index, char in enumerate(givens_string):
            assert char.isdigit()
            digit = int(char)
            row = index // self.rows + 1
            column = index % self.columns + 1
            if digit != 0:
                self.digits.update({Cell(row, column): digit})

    def _validate_boxes(self) -> None:
        """
        Validate the boxes of the sudoku. Valid boxes must not contain overlapping points and must completely cover the
        board. Additionally, all boxes must be the same size.
        """
        assert all([len(box.cells) for box in self.boxes])
        box_cells = set()
        for box in self.boxes:
            for cell in box.cells:
                box_cells.add(cell)

        assert len(box_cells) == self.rows * self.columns

        for row in range(1, self.rows + 1):
            for column in range(1, self.columns + 1):
                assert Cell(row, column) in box_cells

    def solve(self):
        """
        Solve the sudoku using linear programming
        :return:
        """
        min_cell_value = 1
        max_cell_value = max(self.rows, self.columns)
        valid_cell_numbers = list(range(min_cell_value, max_cell_value + 1))

        sudoku = LpProblem("Sudoku Problem", LpMinimize)
        cells = LpVariable.dicts("Cells", (valid_cell_numbers, valid_cell_numbers), min_cell_value, max_cell_value, const.LpInteger)

        # The arbitrary objective function is added
        sudoku += 0, "Arbitrary Objective Function"

        # Add row constraint (no duplicates within a row)
        for row in valid_cell_numbers:
            sudoku += lpSum([cells[row][c] for c in valid_cell_numbers]) == sum(valid_cell_numbers)
            for column in valid_cell_numbers:
                columns_to_right = list(filter(lambda c: c > column, valid_cell_numbers))
                for c in columns_to_right:
                    # Set all different constraint
                    # http://yetanothermathprogrammingconsultant.blogspot.com/2016/05/all-different-and-mixed-integer.html
                    bin_var = LpVariable(f"r{row}c{column}_row_r{row}c{c}", 0, 1, const.LpInteger)
                    sudoku += cells[row][column] <= cells[row][c] - 1 + max_cell_value * bin_var
                    sudoku += cells[row][column] >= cells[row][c] + 1 - max_cell_value * (1 - bin_var)

        # Add column constraint (no duplicates within a column)
        for column in valid_cell_numbers:
            sudoku += lpSum([cells[r][column] for r in valid_cell_numbers]) == sum(valid_cell_numbers)
            for row in valid_cell_numbers:
                rows_to_right = list(filter(lambda r: r > row, valid_cell_numbers))
                for r in rows_to_right:
                    # Set all different constraint
                    # http://yetanothermathprogrammingconsultant.blogspot.com/2016/05/all-different-and-mixed-integer.html
                    bin_var = LpVariable(f"r{row}c{column}_column_r{r}c{column}", 0, 1, const.LpInteger)
                    sudoku += cells[row][column] <= cells[r][column] - 1 + max_cell_value * bin_var
                    sudoku += cells[row][column] >= cells[r][column] + 1 - max_cell_value * (1 - bin_var)

        # Add box constraints (no duplicates within a box)
        for box in self.boxes:
            box.add_box_constraint(sudoku, cells, sum(valid_cell_numbers))

        # Add in all the givens
        for cell, value in self.digits.items():
            sudoku += cells[cell.row][cell.column] == value

        # Solve the sudoku
        sudoku.solve(PULP_CBC_CMD(msg=False))
        assert sudoku.status == const.LpStatusOptimal

        # Temporary Solution: write out 9x9 sudokus to a test file
        # TODO: Implement better return type for this method for easier use (dictionary or 2d list most likely)
        if self.rows == 9:
            # A file called sudokuout.txt is created/overwritten for writing to
            sudokuout = open('sudokuout.txt', 'w')

            # The solution is written to the sudokuout.txt file
            for r in valid_cell_numbers:
                if r % 3 == 1:
                    sudokuout.write("+-------+-------+-------+\n")
                for c in valid_cell_numbers:
                    if c % 3 == 1:
                        sudokuout.write("| ")

                    val = int(v(cells[r][c]))
                    if val > 9 or val < 1:
                        print(f"r{r}c{c} = {val}")
                    sudokuout.write(str(int(v(cells[r][c]))) + " ")

                    if c == 9:
                        sudokuout.write("|\n")
            sudokuout.write("+-------+-------+-------+")
            sudokuout.close()

            # The location of the solution is give to the user
            print("Solution Written to sudokuout.txt")
