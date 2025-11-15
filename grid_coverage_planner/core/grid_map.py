from enum import IntEnum
from typing import Tuple

import numpy as np

class CellType(IntEnum):
    """
    The type of a cell in the grid map.
    Red --> Non-traversable
    Yellow --> Traversable, but not Cuttable
    Green --> Traversable and Cuttable
    """
    RED = 0
    Yellow = 1
    Green = 2


class GridMap:
    """
    A grid map is a 2D grid of cells.
    """

    def __init__(
        self,
        rows: int, 
        cols: int,
        resolution=0.05,
        origin: Tuple(float, float)=(0.0, 0.0),
        default_cell_type: CellType = CellType.Green
    ):
        """
        Initialize the grid map.

        Args:
            rows: The number of rows in the grid.
            cols: The number of columns in the grid.
            resolution: The resolution of the grid.
            origin: The origin of the grid.
            default_cell_type: The default cell type of the grid.

        Returns:
            None

        """

        self.grid_map = np.array

        pass





