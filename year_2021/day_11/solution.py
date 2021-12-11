import os


def read_input():
    matrix = []
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        for line in file:
            matrix.append([int(x) for x in list(line.strip())])
    return matrix


def get_adjacent_points(x, y, matrix):
    possible_adjacent_points = [
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    ]
    return {
        point
        for point in possible_adjacent_points
        if point[0] in range(len(matrix)) and point[1] in range(len(matrix[0]))
    }


# Cover the case:
# Adjacent flashes can cause an octopus to flash on a step even if it begins that step with very little energy.
def is_special_point(i, j, input):
    not_flashing_adjacent_points = [
        p for p in get_adjacent_points(i, j, input) if input[p[0]][p[1]] < 10
    ]
    return len(not_flashing_adjacent_points) == 0


def solve_1():
    input = read_input()
    total_flashes = 0

    for _ in range(100):

        # increment points
        for i in range(len(input)):
            for j in range(len(input[i])):
                input[i][j] += 1

        # search flashing points
        flashing_points_set = set()
        for i in range(len(input)):
            for j in range(len(input[i])):
                if input[i][j] == 10 or is_special_point(i, j, input):
                    input[i][j] = 10
                    flashing_points_set.add((i, j))
                    total_flashes += 1

        # perform flashes
        found = flashing_points_set.copy()
        while len(flashing_points_set) > 0:
            point = flashing_points_set.pop()
            for adj in get_adjacent_points(point[0], point[1], input):
                if adj not in found:
                    input[adj[0]][adj[1]] += 1
                    if input[adj[0]][adj[1]] == 10:
                        new_flashing_point = (adj[0], adj[1])
                        flashing_points_set.add(new_flashing_point)
                        found.add(new_flashing_point)
                        total_flashes += 1

        # normalize (10 -> 0)
        for i in range(len(input)):
            for j in range(len(input[i])):
                input[i][j] = input[i][j] % 10

    return total_flashes


def solve_2():
    input = read_input()
    first_synchronized_flash = 0
    step = 0

    while first_synchronized_flash == 0:
        step += 1

        # increment points
        for i in range(len(input)):
            for j in range(len(input[i])):
                input[i][j] += 1

        # search flashing points
        flashing_points_set = set()
        for i in range(len(input)):
            for j in range(len(input[i])):
                if input[i][j] == 10 or is_special_point(i, j, input):
                    input[i][j] = 10
                    flashing_points_set.add((i, j))

        # perform flashes
        found = flashing_points_set.copy()
        while len(flashing_points_set) > 0:
            point = flashing_points_set.pop()
            for adj in get_adjacent_points(point[0], point[1], input):
                if adj not in found:
                    input[adj[0]][adj[1]] += 1
                    if input[adj[0]][adj[1]] == 10:
                        new_flashing_point = (adj[0], adj[1])
                        flashing_points_set.add(new_flashing_point)
                        found.add(new_flashing_point)

        # normalize (10 -> 0)
        synchronized_flashes = 0
        for i in range(len(input)):
            for j in range(len(input[i])):
                if input[i][j] == 10:
                    synchronized_flashes += 1
                input[i][j] = input[i][j] % 10

        if synchronized_flashes == 100:
            first_synchronized_flash = step

    return first_synchronized_flash


def write_output(output_1, output_2):
    output = f"{output_1}\n{output_2}"
    print(output)
    with open(os.path.join(os.path.dirname(__file__), "output.txt"), "w") as file:
        file.write(output)


write_output(solve_1(), solve_2())
