""" Module Representing a sudoku box """
from typing import List

from solver.cell import Cell


class Box:
    """ A Sudoku Box containing cells """

    def __init__(self, cells: List[Cell]):
        self.cells = cells
        self._validate_cells()

    def _validate_cells(self) -> None:
        """
        Validate the cells of the box by making sure they are all connected and unique (and not empty)
        """
        # Check that the box contains at least one cell
        assert len(self.cells) > 0

        # check for Uniqueness
        assert len(set(self.cells)) == len(self.cells)

        # check for connectedness by starting at the first cell and visiting all of its neighbors iteratively
        visited_cells = set()
        cell_queue = set()

        cell_queue.add(self.cells[0])

        while len(cell_queue) > 0:
            cell = cell_queue.pop()
            if cell in visited_cells:
                continue
            visited_cells.add(cell)
            neighbors = list(filter(lambda c: cell.is_orthogonal(c), self.cells))
            for neighbor in neighbors:
                cell_queue.add(neighbor)

        # If all cells have been visited, the region is connected
        assert len(visited_cells) == len(self.cells)



DEFAULT_BOXES = [
    Box([Cell(1, 1), Cell(1, 2), Cell(1, 3), Cell(2, 1), Cell(2, 2), Cell(2, 3), Cell(3, 1), Cell(3, 2), Cell(3, 3)]),
    Box([Cell(4, 1), Cell(4, 2), Cell(4, 3), Cell(5, 1), Cell(5, 2), Cell(5, 3), Cell(6, 1), Cell(6, 2), Cell(6, 3)]),
    Box([Cell(7, 1), Cell(7, 2), Cell(7, 3), Cell(8, 1), Cell(8, 2), Cell(8, 3), Cell(9, 1), Cell(9, 2), Cell(9, 3)]),
    Box([Cell(1, 4), Cell(1, 5), Cell(1, 6), Cell(2, 4), Cell(2, 5), Cell(2, 6), Cell(3, 4), Cell(3, 5), Cell(3, 6)]),
    Box([Cell(4, 4), Cell(4, 5), Cell(4, 6), Cell(5, 4), Cell(5, 5), Cell(5, 6), Cell(6, 4), Cell(6, 5), Cell(6, 6)]),
    Box([Cell(7, 4), Cell(7, 5), Cell(7, 6), Cell(8, 4), Cell(8, 5), Cell(8, 6), Cell(9, 4), Cell(9, 5), Cell(9, 6)]),
    Box([Cell(1, 7), Cell(1, 8), Cell(1, 9), Cell(2, 7), Cell(2, 8), Cell(2, 9), Cell(3, 7), Cell(3, 8), Cell(3, 9)]),
    Box([Cell(4, 7), Cell(4, 8), Cell(4, 9), Cell(5, 7), Cell(5, 8), Cell(5, 9), Cell(6, 7), Cell(6, 8), Cell(6, 9)]),
    Box([Cell(7, 7), Cell(7, 8), Cell(7, 9), Cell(8, 7), Cell(8, 8), Cell(8, 9), Cell(9, 7), Cell(9, 8), Cell(9, 9)]),
]