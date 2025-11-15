import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from grid_coverage_planner.core.grid_map import GridMap, CellType

def main():
    grid_map = GridMap()
    grid_map.load(dir_path="/home/serene/grid-coverage-planner/grid_map_save/test_grid_map")
    print(grid_map.data)
    print(grid_map.metadata)
    print(grid_map.get_all_traversable_cells())
    print(grid_map.get_all_cuttable_cells())
    print(grid_map.get_all_non_traversable_cells())
    print(grid_map.get_all_cells_of_type(CellType.TRAVERSABLE))
    print(grid_map.get_all_cells_of_type(CellType.CUTTABLE))

if __name__ == "__main__":
    main()

