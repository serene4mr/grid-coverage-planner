from enum import IntEnum
from typing import Tuple, List, Dict
from pathlib import Path
import json

import numpy as np

from grid_coverage_planner.utils.logger import LOGGER


class CellType(IntEnum):
    """
    The type of a cell in the grid map.
    Non-traversable --> 0
    Traversable --> 1
    Cuttable --> 2
    """
    NON_TRAVERSABLE = 0
    TRAVERSABLE = 1
    CUTTABLE = 2


class GridMap:
    """
    A grid map is a 2D grid of cells.
    """

    def __init__(
        self,
        rows: int = 100,
        cols: int = 100,
        resolution: float =0.05,
        origin: Tuple[float, float]=(0.0, 0.0),
        default_cell_type: CellType = CellType.NON_TRAVERSABLE,
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

        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be greater than 0")
        if resolution <= 0:
            raise ValueError("Resolution must be greater than 0")
        if not isinstance(origin, tuple) or len(origin) != 2:
            raise ValueError("Origin must be a tuple of two elements")
        
        self.rows = rows
        self.cols = cols
        self.resolution = resolution
        self.origin = origin

        # Create 2D NumPy array filled with default cell type
        self.data: np.ndarray = np.full(
            shape=(rows, cols),
            fill_value=default_cell_type.value,
            dtype=np.uint8
        )

        self.metadata = {
            "name": "",
            "description": "",
            "resolution": resolution,
            "origin": origin
        }

    @classmethod
    def from_world_size(cls, world_size: Tuple[float, float], resolution: float = 0.05, origin: Tuple[float, float]=(0.0, 0.0), default_cell_type: CellType = CellType.NON_TRAVERSABLE):
        """
        Create a grid map from the world size.
        """
        rows = int(world_size[0] / resolution)
        cols = int(world_size[1] / resolution)
        return cls(rows, cols, resolution, origin, default_cell_type)

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get_cell(self, row: int, col: int) -> CellType:
        """
        Get the cell type at the given row and column.
        """
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self.data[row, col]

    def set_cell(self, row: int, col: int, cell_type: CellType):
        """
        Set the cell type at the given row and column.
        """
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        self.data[row, col] = cell_type.value

    def is_traversable(self, row: int, col: int) -> bool:
        """
        Check if the cell at the given row and column is traversable.
        """
        if not self.is_valid_position(row, col):
            raise ValueError(f"Invalid position: ({row}, {col})")
        return self.data[row, col] == CellType.TRAVERSABLE.value    

    def is_cuttable(self, row: int, col: int) -> bool:
        """
        Check if the cell at the given row and column is cuttable.
        """
        return self.data[row, col] == CellType.CUTTABLE.value
    
    def is_non_traversable(self, row: int, col: int) -> bool:
        """
        Check if the cell at the given row and column is non-traversable.
        """
        return self.data[row, col] == CellType.NON_TRAVERSABLE.value
    
    def get_all_cells_of_type(self, cell_type: CellType) -> List[Tuple[int, int]]:
        """
        Get all cells of the given type.
        """
        return np.where(self.data == cell_type.value)
    
    def get_all_traversable_cells(self) -> List[Tuple[int, int]]:
        """
        Get all traversable cells.
        """
        return self.get_all_cells_of_type(CellType.TRAVERSABLE)
    
    def get_all_cuttable_cells(self) -> List[Tuple[int, int]]:
        """
        Get all cuttable cells.
        """
        return self.get_all_cells_of_type(CellType.CUTTABLE)
    
    def get_all_non_traversable_cells(self) -> List[Tuple[int, int]]:
        """
        Get all non-traversable cells.
        """
        return self.get_all_cells_of_type(CellType.NON_TRAVERSABLE)

    def grid_to_world(self, row: int, col: int) -> Tuple[float, float]:
        """
        Convert grid coordinates to world coordinates. (row, col) --> (x, y)
        """
        return self.origin[0] + col * self.resolution, self.origin[1] + row * self.resolution
    
    def world_to_grid(self, x: float, y: float) -> Tuple[int, int]:
        """
        Convert world coordinates to grid coordinates. (x, y) --> (row, col)
        """ 
        return int((x - self.origin[0]) / self.resolution), int((y - self.origin[1]) / self.resolution)
    
    def grid_to_world_path(self, path: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
        """
        Convert grid coordinates to world coordinates. (row, col) --> (x, y)
        """
        return [self.grid_to_world(row, col) for row, col in path]
    
    def world_to_grid_path(self, path: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
        """
        Convert world coordinates to grid coordinates. (x, y) --> (row, col)
        """
        return [self.world_to_grid(x, y) for x, y in path]

    @property
    def world_bounds(self) -> Dict[str, float]:
        """World coordinate bounds"""
        return {
            'x_min': self.origin[0],
            'x_max': self.origin[0] + self.cols * self.resolution,
            'y_min': self.origin[1],
            'y_max': self.origin[1] + self.rows * self.resolution,
        }
    
    @property
    def width_m(self) -> float:
        """Width in meters"""
        return self.cols * self.resolution
    
    @property
    def height_m(self) -> float:
        """Height in meters"""
        return self.rows * self.resolution

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get the neighbors of the given cell.
        """

        neighbors = []

        directions = (-1, 0, 1)
        for dr in directions:
            for dc in directions:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                
                if self.is_valid_position(nr, nc):
                    neighbors.append((nr, nc))
        
        return neighbors

    def get_traversable_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get the traversable neighbors of the given cell.
        """
        return [neighbor for neighbor in self.get_neighbors(row, col) if self.is_traversable(neighbor)]
    
    def get_cuttable_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get the cuttable neighbors of the given cell.
        """
        return [neighbor for neighbor in self.get_neighbors(row, col) if self.is_cuttable(neighbor)]
    
    def get_non_traversable_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get the non-traversable neighbors of the given cell.
        """
        return [neighbor for neighbor in self.get_neighbors(row, col) if self.is_non_traversable(neighbor)]

    def save(self, dir_path: str):
        """
        Save the grid map to a file .gm.npy
        Save the metadata to a file .gm.json
        """

        if self.metadata['name'] == '':
            raise ValueError("Grid map name is not set")

        save_path = Path(dir_path) / f"{self.metadata['name']}"
        if not save_path.is_dir():
            save_path.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError(f"Grid map directory already exists: {save_path}")
        
        np.save(save_path / "data.gm.npy", self.data)
        with open(save_path / "metadata.gm.json", "w") as f:
            json.dump(self.metadata, f)
        
        LOGGER.info(f"Grid map saved to {save_path} successfully")

    def load(self, dir_path: str):
        """
        Load the grid map from a file.
        """

        load_path = Path(dir_path)
        if not load_path.is_dir():
            raise ValueError(f"Grid map directory does not exist: {load_path}")
        
        self.data = np.load(load_path / "data.gm.npy")
        with open(load_path / "metadata.gm.json", "r") as f:
            self.metadata = json.load(f)
        
        LOGGER.info(f"Grid map loaded from {load_path} successfully")
    

    
    

    




    






