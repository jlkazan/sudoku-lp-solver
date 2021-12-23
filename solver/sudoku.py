""" Module Representing a Sudoku Puzzle """
from typing import Optional, List

from solver.box import Box, DEFAULT_BOXES
from solver.cell import Cell


class Sudoku:
    """ A Model for a Sudoku Puzzle """

    def __init__(self, rows: int = 9, columns: int = 9, boxes: List[Box] = DEFAULT_BOXES, givens_string: Optional[str] = None):
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
