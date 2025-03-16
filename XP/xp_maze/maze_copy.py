"""Maze solver."""
import heapq

global_map_with_costs = []


def find_doors(maze: str) -> dict:
    """Find doors."""
    maze_rows = maze.strip().split("\n")
    maze_w = len(maze_rows[0])
    # maze_h = len(maze_rows)
    maze_y = 0
    maze_x = 0

    doors = {
        "entries": [],
        "exits": []
    }

    for i, row in enumerate(maze_rows):
        for j, symbol in enumerate(row):
            # find the entry door "|"
            if j == 0 and symbol == "|":
                entry = MapCoordinates(maze_y, maze_x, 0)
                doors["entries"].append(entry)
            elif j == maze_w - 1 and symbol == "|":
                exit = MapCoordinates(maze_y, maze_x, 0)
                doors["exits"].append(exit)

            # update y and x for the next point
            maze_x += 1
            if (j + 1) % maze_w == 0:
                maze_x = 0
                maze_y += 1

    return doors


def find_cost(coords_list: list[tuple]) -> list[int]:
    """Docstring."""
    costs = []
    for coords in coords_list:
        for point in global_map_with_costs:
            if point.get_coordinates() == coords:
                point_cost = point.get_cost()
                costs.append(point_cost)
                break
        else:
            costs.append(0)  # unknown elements cost is 0
    return costs


def set_h_cost(y, x, point_y, point_x) -> int:
    """Calculate h cost."""
    cost = 0

    while True:
        # exit condition
        if y == point_y and x == point_x:
            return cost

        # horisontal movement is possible
        if y != point_y and x != point_x:
            cost += 1
            y = adjust_coordinate(y, point_y)
            continue

        # only one coordinate might change
        elif y != point_y and x == point_x:
            cost += 1
            y = adjust_coordinate(y, point_y)
            continue

        elif y == point_y and x != point_x:
            cost += 1
            x = adjust_coordinate(x, point_x)
            continue


def set_g_cost(parent, cost) -> int:
    """Calculate g cost."""
    if parent != "start":
        cost += parent.get_cost()  # total cost
        return set_g_cost(parent.get_parent(), cost)
    else:
        return cost


def initial_cost(initial_point, cost) -> int:
    """Return the initial cost."""
    for point in global_map_with_costs:
        if point.get_coordinates() == initial_point.get_coordinates():
            cost1 = point.get_cost()
            if cost1 > -1:
                cost += cost1
                return cost
    else:
        return 0


def diagonal_move(y, x, point_y, point_x, y_prev, x_prev, cost) -> tuple[int, int, int]:
    """Return the y, x, cost."""
    y, x = adjust_coordinate(y, point_y), adjust_coordinate(x, point_x)

    neighbour1 = MapCoordinates(y, x_prev, -1)
    neighbour2 = MapCoordinates(y_prev, x, -1)

    for point in global_map_with_costs:
        if point.get_coordinates() == neighbour1.get_coordinates():
            neighbour1.set_cost(point.get_cost())
        elif point.get_coordinates() == neighbour2.get_coordinates():
            neighbour2.set_cost(point.get_cost())

    cost1 = neighbour1.get_cost()
    cost2 = neighbour2.get_cost()

    if cost1 > -1 and cost2 > -1:  # might be problems with obstacles (Algorithm)
        if cost1 < cost2:
            cost += cost1
            y, x = neighbour1.get_coordinates()
        else:
            cost += cost2
            y, x = neighbour2.get_coordinates()
    elif cost1 > -1:
        cost += cost1
        y, x = neighbour1.get_coordinates()
    elif cost2 > -1:
        cost += cost2
        y, x = neighbour2.get_coordinates()
    else:
        # don't change the cost, but update the coordinates
        y, x = neighbour1.get_coordinates()

    return y, x, cost


def adjust_coordinate(coord, target) -> int:
    """Adjust a single coordinate towards the target."""
    if coord > target:
        return coord - 1
    elif coord < target:
        return coord + 1
    return coord


class Coordinates:
    """Coordinates."""

    def __init__(self, y: int, x: int, start_y: int, start_x: int, end_y: int, end_x, parent: object = "start", cost: int = -1):
        """Docstring."""
        self.y = y
        self.x = x
        self.g_cost = set_g_cost(parent, cost)
        self.h_cost = set_h_cost(y, x, end_y, end_x)
        self.f_cost = self.g_cost + self.h_cost
        self.parent = parent
        self.cost = cost

    def __repr__(self):
        """Docstring."""
        return f"({self.y}, {self.x})"

    def __lt__(self, other):
        """Docstring."""
        return self.get_f_cost() < other.get_f_cost()

    def get_coordinates(self) -> tuple[int, int]:
        """Docstring."""
        return self.y, self.x

    def get_f_cost(self) -> int:
        """Docstring."""
        return self.f_cost

    def set_f_cost(self, cost) -> None:
        """Docstring."""
        self.f_cost = cost

    def get_g_cost(self) -> int:
        """Docstring."""
        return self.g_cost

    def get_cost(self) -> int:
        """Docstring."""
        return self.cost

    def get_parent(self) -> object | str:
        """Docstring."""
        return self.parent

    def set_parent(self, parent) -> None:
        """Docstring."""
        self.parent = parent


class MapCoordinates:
    """Map coordinates."""

    def __init__(self, y, x, cost):
        """Docstring."""
        self.y = y
        self.x = x
        self.cost = cost

    def __repr__(self):
        """Docstring."""
        return f"({self.y}, {self.x})"

    def get_coordinates(self) -> tuple[int, int]:
        """Docstring."""
        return self.y, self.x

    def get_cost(self) -> int:
        """Docstring."""
        return self.cost

    def set_cost(self, new_cost) -> None:
        """Docstring."""
        self.cost = new_cost


def get_neighbours(point: Coordinates, start: tuple[int, int], goal: tuple[int, int]) -> list:
    """Docstring."""
    start_y, start_x = start
    end_y, end_x = goal
    y, x = point.get_coordinates()

    coords_list = [(y - 1, x), (y + 1, x), (y, x + 1), (y, x - 1)]

    all_costs = find_cost(coords_list)  # should return 4 values as got 4 inputs
    neighbour_top = Coordinates(y - 1, x, start_y, start_x, end_y, end_x, point, all_costs[0])
    neighbour_bot = Coordinates(y + 1, x, start_y, start_x, end_y, end_x, point, all_costs[1])
    neighbour_right = Coordinates(y, x + 1, start_y, start_x, end_y, end_x, point, all_costs[2])
    neighbour_left = Coordinates(y, x - 1, start_y, start_x, end_y, end_x, point, all_costs[3])

    return [neighbour_top, neighbour_bot, neighbour_right, neighbour_left]


class MazeSolver:
    """Maze solver class."""

    def __init__(self, maze_str: str, configuration: dict = None):
        """
        Initialize the solver with map string and configuration.

        Map string can consist of several lines, line break separates the lines.
        Empty lines in the beginning and in the end should be ignored.
        Line can also consist of spaces, so the lines cannot be stripped.

        On the left and right sides there can be several doors (marked with "|").
        Solving the maze starts from a door from the left side and ends at the door on the right side.
        See more @solve().

        Configuration is a dict which indicates which symbols in the map string have what cost.
        Doors (|) are not shown in the configuration and are not used inside the maze.
        Door cell cost is 0.
        When a symbol on the map string is not in configuration, its cost is 0.
        Cells with negative cost cannot be moved on/through.

        Default configuration:
        configuration = {
            ' ': 1,
            '#': -1,
            '.': 2,
            '-': 5,
            'w': 10
        }

        :param maze_str: Map string
        :param configuration: Optional dictionary of symbol costs.
        """
        if configuration is None:
            self.configuration = {
                ' ': 1,
                '#': -1,
                '.': 2,
                '-': 5,
                'w': 10
            }
        else:
            self.configuration = configuration
        self.maze = maze_str
        self.maze_with_costs = self.get_map_with_costs()
        # self.possible_points = self.get_map_with_possible_points()

    def get_map_with_costs(self) -> list[MapCoordinates]:
        """Docstring."""
        # Split the maze string into rows for processing
        maze_rows = self.maze.strip().split("\n")
        maze_w = len(maze_rows[0])
        # maze_h = len(maze_rows)
        maze_y = 0
        maze_x = 0
        map_repr = []

        for i, row in enumerate(maze_rows):
            for j, symbol in enumerate(row):
                # find the cost
                cost = 0
                if symbol in self.configuration.keys():
                    cost = self.configuration[symbol]

                # create a point object
                map_point = MapCoordinates(maze_y, maze_x, cost)
                map_repr.append(map_point)

                # update y and x for the next point
                maze_x += 1
                if (j + 1) % maze_w == 0:
                    maze_x = 0
                    maze_y += 1

        return map_repr

    def set_global_map(self) -> None:
        """Docstring."""
        global global_map_with_costs  # Declare it as global
        global_map_with_costs = self.get_map_with_costs()

    def get_map_with_possible_points(self) -> list[tuple[int, int]]:
        """Docstring."""
        # Split the maze string into rows for processing
        maze_rows = self.maze.strip().split("\n")
        maze_w = len(maze_rows[0])
        maze_y = 0
        maze_x = 0
        map_repr = []

        for i, row in enumerate(maze_rows):
            for j, symbol in enumerate(row):
                # find the cost
                cost = 0
                if symbol in self.configuration.keys():
                    cost = self.configuration[symbol]

                # skip negative because these points are walls
                if cost > -1:
                    # create a point object
                    map_point = (maze_y, maze_x)
                    map_repr.append(map_point)

                # update y and x for the next point
                maze_x += 1
                if (j + 1) % maze_w == 0:
                    maze_x = 0
                    maze_y += 1

        return map_repr

    def generate_map_data(self) -> tuple[list[MapCoordinates], list[tuple[int, int]]]:
        """
        Generate map data containing both costs and possible points.

        Processes the maze once and extracts:
        - A list of MapCoordinates with costs.
        - A list of possible points (coordinates with non-negative costs).

        :return: (map_with_costs, map_with_possible_points)
        """
        maze_rows = self.maze.strip().split("\n")
        maze_w = len(maze_rows[0])
        maze_y = 0
        maze_x = 0
        map_with_costs = []
        map_with_possible_points = []

        for row in maze_rows:
            for j, symbol in enumerate(row):
                # Determine cost based on the configuration
                cost = self.configuration.get(symbol, 0)

                # Create a MapCoordinates object for cost representation
                map_point = MapCoordinates(maze_y, maze_x, cost)
                map_with_costs.append(map_point)

                # Add to possible points if cost is non-negative
                if cost > -1:
                    map_with_possible_points.append((maze_y, maze_x))

                # Update coordinates for the next point
                maze_x += 1
                if (j + 1) % maze_w == 0:
                    maze_x = 0
                    maze_y += 1

        return map_with_costs, map_with_possible_points

    def path_backwards(self, point: object | str, path=None, cost: int = 0) -> tuple[list, int]:
        """Docstring."""
        if path is None:
            path = []

        parent = point.get_parent()
        coords = point.get_coordinates()
        cost += point.get_cost()  # total cost

        path.insert(0, coords)

        if parent != "start":
            return self.path_backwards(parent, path, cost)
        else:
            return path, cost

    def get_shortest_path(self, start: tuple[int, int], goal: tuple[int, int]) -> tuple[list, int] | tuple[None, -1]:
        """
        Return shortest path and the total cost of it.

        If there is no path from the start to goal, the path is None and cost is -1.
        """
        # Generate map data
        global global_map_with_costs  # Declare global variable
        global_map_with_costs, map_with_possible_points = self.generate_map_data()

        start_y, start_x = start
        end_y, end_x = goal
        point_cost = find_cost([start])[0]
        starting_point = Coordinates(start_y, start_x, start_y, start_x, end_y, end_x, "start", point_cost)

        # Initialize open and closed lists
        open_list = []
        heapq.heappush(open_list, (starting_point.get_f_cost(), starting_point))
        closed_set = set()

        while open_list:
            _, current_point = heapq.heappop(open_list)

            if current_point.get_coordinates() == goal:
                return self.path_backwards(current_point)

            closed_set.add(current_point.get_coordinates())

            for neighbour in get_neighbours(current_point, start, goal):
                neighbour_coords = neighbour.get_coordinates()
                if neighbour_coords in closed_set:
                    continue

                if neighbour_coords in map_with_possible_points:
                    heapq.heappush(open_list, (neighbour.get_f_cost(), neighbour))

        return None, -1

    def solve(self) -> tuple[list, int] | tuple[None, -1]:
        """
        Solve the given maze and return the path and the cost.

        Finds the shortest path from one of the doors on the left side to one of the doors on the right side.
        Shortest path is the one with the lowest cost.

        This method uses get_shortest_path method and returns the same values.
        If there are several paths with the same cost, return any of those.

        :return: shortest_path, cost
        """
        # Find the coordinates of the doors
        doors_dict = find_doors(self.maze)
        entries = doors_dict["entries"]
        exits = doors_dict["exits"]

        # Early exit if no doors exist
        if not entries or not exits:
            return None, -1

        # Priority queue to find the shortest path dynamically
        heap = []
        shortest_path = None
        shortest_cost = float('inf')

        for entry_door in entries:
            for exit_door in exits:
                path, cost = self.get_shortest_path(entry_door.get_coordinates(), exit_door.get_coordinates())

                if cost >= 0 and cost < shortest_cost:
                    shortest_path = path
                    shortest_cost = cost
                    heapq.heappush(heap, (cost, path))

        # If a valid path exists, return the best one
        if shortest_path:
            return shortest_path, shortest_cost

        return None, -1


if __name__ == '__main__':
    print("Costs tests.")
    maze = """
########
#      #
|    w |
########
"""
    solver = MazeSolver(maze)
    print(solver.get_map_with_costs())
    # print(set_h_cost(0, 0, 0, 2))  # 0
    # print(set_costs(0, 0, 2, 2))  # 2 (Maybe problems)
    # print(set_costs(2, 0, 2, 4))  # 4
    # print(set_costs(2, 0, 2, 5))  # 14
    # print(set_costs(2, 5, 2, 0))  # 14
    # print(set_costs(2, 0, 2, 7))  # 15
    print()
    print("Coordinates class tests.")
    start_y, start_x = (0, 0)
    end_y, end_x = (0, 1)
    point = Coordinates(start_y, start_x, start_y, start_x, end_y, end_x)
    assert point.get_coordinates() == (0, 0)
    print()
    print("path_backwards tests")
    point1 = Coordinates(0, 0, 0, 0, 3, 3)
    point2 = Coordinates(1, 1, 0, 0, 3, 3, point1)
    point3 = Coordinates(2, 2, 0, 0, 3, 3, point2)
    point4 = Coordinates(3, 3, 0, 0, 3, 3, point3, 10)
    path_backwards = MazeSolver("")
    print(path_backwards.path_backwards(point4))  # ([(0, 0), (1, 1), (2, 2), (3, 3)], something)
    print()
    print("find_cost tests")
    coords_list = [(2 - 1, 4), (2 + 1, 4), (2, 4 + 1), (2, 4 - 1)]
    print(find_cost(coords_list))  # should return 4 values
    print()
    print("get_shortest_path tests")
    print(solver.get_shortest_path((2, 4), (2, 5)))  # ([(2, 4), (2, 5)], 11)
    print(solver.get_shortest_path((2, 4), (2, 7)))  # ([(2, 4), (1, 4), (1, 5), (1, 6), (2, 6), (2, 7)], 5)
    maze = """
########
#      #
#      #
|      |
########
"""
    solver = MazeSolver(maze)
    # print("solver test")
    # solver.solve()
    # assert solver.solve() == ([(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)], 6)
    print(solver.get_shortest_path((3, 0), (3, 1)))  # ([(3, 0), (3, 1)], 1)
    assert solver.get_shortest_path((3, 0), (3, 1)) == ([(3, 0), (3, 1)], 1)
    assert solver.get_shortest_path((3, 0), (2, 0)) == (None, -1)

    maze = """
#####
#   #
| # #
# # |
#####
    """
    solver = MazeSolver(maze)
    print(solver.get_shortest_path((2, 0), (3, 4)))  # ([(2, 0), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4)], 6)
    assert solver.solve() == ([(2, 0), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4)], 6)

    maze = """
#####
#   |
#   |
| # #
#####
| # |
#####
    """
    solver = MazeSolver(maze)
    print(solver.solve())
    # assert solver.solve() == ([(3, 0), (3, 1), (2, 1), (2, 2), (2, 3), (2, 4)], 4)
    print(solver.get_shortest_path((3, 0), (1, 4)))
    # multiple paths possible, let's just assert the cost
    assert solver.get_shortest_path((3, 0), (1, 4))[1] == 4  # using the door at (2, 4)
    assert solver.get_shortest_path((5, 0), (5, 4)) == (None, -1)
    print()

    maze = """
#####
#   |
#   |
| # #
#####
| # |
#####
    """
    print("Check the doors finder function.")
    print(find_doors(maze))
    print()

    print("Try to find a mistake.")  # 18
    maze = """
###############
#         w   |
#    w  www   |
| # #      ####
##########    |
"""
    solver = MazeSolver(maze)
    print(solver.solve())
    print()

    print("Fix bugs.")
    maze = """
EEE
|w|
.-|
###
"""
    solver = MazeSolver(maze)
    print(solver.solve())  # ([(1, 0), (0, 0), (0, 1), (0, 2), (1, 2)], 0)
