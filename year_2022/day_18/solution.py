import os
from collections import defaultdict
from utils.data_structures import Point
from utils.io import write_output
from utils.utils import sum_tuples, tuple_to_point

adjacent_deltas = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
]


class CubesRepository:
    def __init__(self):
        self.all_cubes = set()
        self.by_x = defaultdict(set)
        self.by_y = defaultdict(set)
        self.by_z = defaultdict(set)

    def add_cube(self, point):
        self.by_x[point.x].add(point)
        self.by_y[point.y].add(point)
        self.by_z[point.z].add(point)
        self.all_cubes.add(point)

    def query(self, x=None, y=None, z=None):
        result = self.all_cubes
        if x is not None:
            result = result.intersection(self.by_x[x])
        if y is not None:
            result = result.intersection(self.by_y[y])
        if z is not None:
            result = result.intersection(self.by_z[z])
        return result


def read_input():
    cubes = CubesRepository()
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            x, y, z = line.strip().split(",")
            cubes.add_cube(Point(int(x), int(y), int(z)))
    return cubes


def is_internal_cube(cube, cubes_repo: CubesRepository, internal_cubes_seen: set):
    internal_cubes_seen.add(cube)

    lower_bound_x = upper_bound_x = False
    for c in cubes_repo.query(x=None, y=cube.y, z=cube.z):
        lower_bound_x = True if c.x < cube.x else lower_bound_x
        upper_bound_x = True if c.x > cube.x else upper_bound_x

    lower_bound_y = upper_bound_y = False
    for c in cubes_repo.query(x=cube.x, y=None, z=cube.z):
        lower_bound_y = True if c.y < cube.y else lower_bound_y
        upper_bound_y = True if c.y > cube.y else upper_bound_y

    lower_bound_z = upper_bound_z = False
    for c in cubes_repo.query(x=cube.x, y=cube.y, z=None):
        lower_bound_z = True if c.z < cube.z else lower_bound_z
        upper_bound_z = True if c.z > cube.z else upper_bound_z

    is_internal = (
        lower_bound_x
        and upper_bound_x
        and lower_bound_y
        and upper_bound_y
        and lower_bound_z
        and upper_bound_z
    )

    if not is_internal:
        return False

    # check if adjacent cubes are internal as well
    for adj in adjacent_deltas:
        adjacent = tuple_to_point(sum_tuples(cube, adj))
        if adjacent not in cubes_repo.all_cubes and adjacent not in internal_cubes_seen:
            is_internal = is_internal_cube(adjacent, cubes_repo, internal_cubes_seen)
            if not is_internal:
                return False

    return True


def solve_1(cubes_repo: CubesRepository):
    total_faces = 0
    for cube in cubes_repo.all_cubes:
        faces = 6
        for adj in adjacent_deltas:
            adjacent = sum_tuples(cube, adj)
            if adjacent in cubes_repo.all_cubes:
                # adjacent cube found
                faces -= 1
        total_faces += faces
    return total_faces


def solve_2(cubes_repo):
    total_faces = 0
    internal_cubes = set()
    for cube in input.all_cubes:
        faces = 6
        for adj in adjacent_deltas:
            adjacent = tuple_to_point(sum_tuples(cube, adj))
            if adjacent in input.all_cubes:
                # adjacent cube found
                faces -= 1
            else:
                # adjacent cube that could be an internal cube
                tmp_internal = set(internal_cubes)
                if is_internal_cube(adjacent, cubes_repo, tmp_internal):
                    internal_cubes.update(tmp_internal)
                    faces -= 1
        total_faces += faces
    return total_faces


input = read_input()
write_output(solve_1(input), solve_2(input))
