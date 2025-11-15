import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from grid_coverage_planner.core.grid_map import GridMap, CellType


def main():
    grid_map = GridMap(rows=10, cols=10, resolution=0.05, origin=(0.0, 0.0), default_cell_type=CellType.NON_TRAVERSABLE)
    grid_map.metadata['name'] = "test_grid_map"
    grid_map.save("grid_map_save")

if __name__ == "__main__":
    main()