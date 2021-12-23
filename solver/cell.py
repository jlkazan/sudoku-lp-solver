""" Module for a sudoku Cell with row, column position """


class Cell:
    """ A Sudoku cell """

    def __init__(self, row: int, column: int):
        """
        A Cell at the given row and column
        :param row: The 1-indexed row of the cell
        :param column: The 1-indexed column of the cell
        """
        self.row = row
        self.column = column

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Cell) and self.row == o.row and self.column == o.column

    def __hash__(self) -> int:
        return hash((self.row, self.column))

    def __repr__(self):
        return f"r{self.row}c{self.column}"

    def is_orthogonal(self, other: 'Cell') -> bool:
        return (
            self.column == other.column and abs(self.row - other.row) == 1 or
            self.row == other.row and abs(self.column - other.column) == 1
        )
