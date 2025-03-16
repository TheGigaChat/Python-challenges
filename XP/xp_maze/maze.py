"""Maze."""

import heapq

class MazeSolver:
    """
    A class to solve mazes represented as strings with configurable cell costs.

    This class finds the shortest path through a maze from doors ('|') on the left side to
    doors on the right side, considering varying movement costs and impassable cells.
    """

    def __init__(self, maze_str: str, configs: dict = None):
        """
        Initialize the MazeSolver with a maze string and optional configuration.

        The maze string should consist of multiple lines separated by line breaks.
        Lines represent rows of the maze, and each character represents a cell.
        Leading and trailing empty lines are ignored, but spaces within lines are preserved.

        Configuration specifies the movement cost for each symbol in the maze.
        Symbols not present in the configuration have a default cost of 0.
        Cells with a cost of -1 are considered impassable. Doors ('|') always have a cost of 0.

        :param maze_str: A string representation of the maze.
        :param configs: A dictionary mapping symbols to movement costs.
        """
        if configs is None:
            configs = {
                ' ': 1,
                '#': -1,
                '.': 2,
                '-': 5,
                'w': 10
            }

        self.maze = [list(line) for line in maze_str.strip().split("\n")]
        self.configs = configs
        self.height = len(self.maze)
        self.width = len(self.maze[0])

        # Identify doors on the left and right edges of the maze
        self.start_doors = [(i, 0) for i in range(self.height) if self.maze[i][0] == '|']
        self.end_doors = [(i, self.width - 1) for i in range(self.height) if self.maze[i][self.width - 1] == '|']

    def locate(self, area: str, x: int, y: int, unknown: str = None) -> list:
        """
        Identify potential locations of a smaller known area within the larger maze.

        The method compares the provided area to every possible location in the maze.
        If the area matches a subsection of the maze, the coordinates of the match are returned.

        :param area: A string representing the smaller area to locate within the maze.
        :param x: The x-coordinate of the target position relative to the area.
        :param y: The y-coordinate of the target position relative to the area.
        :param unknown: A character representing unknown cells in the area. These cells are ignored in matching.
        :return: A list of tuples representing all potential matching coordinates (y, x).
        """
        area = [list(line) for line in area.strip().split("\n")]
        area_height = len(area)
        area_width = len(area[0])

        possible_locations = []

        for i in range(self.height - area_height + 1):
            for j in range(self.width - area_width + 1):
                match = True
                for ai in range(area_height):
                    for aj in range(area_width):
                        if area[ai][aj] == unknown:
                            continue
                        if area[ai][aj] != self.maze[i + ai][j + aj]:
                            match = False
                            break
                    if not match:
                        break
                if match:
                    possible_locations.append((i + y, j + x))

        return possible_locations

    def get_shortest_path(self, start: tuple, goal: tuple) -> tuple:
        """
        Compute the shortest path and its cost between two points in the maze.

        The path is calculated using Dijkstra's algorithm, which considers movement costs
        and avoids impassable cells. If no path exists, returns None and a cost of -1.

        :param start: A tuple (y, x) representing the starting cell's coordinates.
        :param goal: A tuple (y, x) representing the goal cell's coordinates.
        :return: A tuple containing the path as a list of coordinates and the total cost.
        """
        y_start, x_start = start
        y_goal, x_goal = goal

        visited = set()
        pq = [(0, y_start, x_start, [])]  # Priority queue: (cost, y, x, path)

        while pq:
            current_cost, y, x, path = heapq.heappop(pq)

            if (y, x) in visited:
                continue

            visited.add((y, x))
            path = path + [(y, x)]

            if (y, x) == (y_goal, x_goal):
                return path, current_cost

            for (ny, nx), move_cost in self.get_neighbors(y, x):
                if (ny, nx) not in visited:
                    heapq.heappush(pq, (current_cost + move_cost, ny, nx, path))

        return None, -1

    def solve(self) -> tuple:
        """
        Solve the maze by finding the shortest path from any start door to any end door.

        The method evaluates all possible combinations of start and end doors to find
        the path with the lowest cost. If no path exists, returns None and a cost of -1.

        :return: A tuple containing the shortest path as a list of coordinates and the total cost.
        """
        best_path, best_cost = None, float('inf')

        for start in self.start_doors:
            for goal in self.end_doors:
                path, cost = self.get_shortest_path(start, goal)
                if cost != -1 and cost < best_cost:
                    best_path, best_cost = path, cost

        return (best_path, best_cost) if best_path else (None, -1)

    def get_neighbors(self, y, x):
        """
        Identify valid neighboring cells and their movement costs.

        This method checks adjacent cells in all four cardinal directions (up, down, left, right).
        Only cells within the maze bounds and with non-negative movement costs are returned.

        :param y: The y-coordinate of the current cell.
        :param x: The x-coordinate of the current cell.
        :return: A list of tuples ((ny, nx), cost) where (ny, nx) is the neighbor's coordinates and cost is the movement cost.
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.height and 0 <= nx < self.width:
                cost = self.configs.get(self.maze[ny][nx], 0)
                if cost >= 0:  # Valid cell
                    neighbors.append(((ny, nx), cost))
        return neighbors
