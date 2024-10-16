import os
from collections import deque, defaultdict
from utils.data_structures import Point
from utils.io import write_output


# TODO: FIXME: NOT SOLVED. Needs further analysis

def read_input():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as file:
        input = []
        for line in file:
            start_point = [int(x) for x in line.strip().split("~")[0].split(",")]
            end_point = [int(x) for x in line.strip().split("~")[1].split(",")]
            input.append((Point(*start_point), Point(*end_point)))
        return input


def calculate_shape_points(tuple):
    start, end = tuple
    x_range = set(range(min(start.x, end.x), max(start.x, end.x) + 1))
    y_range = set(range(min(start.y, end.y), max(start.y, end.y) + 1))
    z_range = set(range(min(start.z, end.z), max(start.z, end.z) + 1))
    return (x_range, y_range, z_range)


def is_possible(p1, p2):
    (p1_x_range, p1_y_range, p1_z_range) = calculate_shape_points(p1)
    (p2_x_range, p2_y_range, p2_z_range) = calculate_shape_points(p2)
    if (
        len(p1_x_range.intersection(p2_x_range)) > 0
        and len(p1_y_range.intersection(p2_y_range)) > 0
        and len(p1_z_range.intersection(p2_z_range)) > 0
    ):
        return False
    return True


def move_down(tuple):
    start, end = tuple
    new_shape_start = Point(start.x, start.y, start.z - 1)
    new_shape_end = Point(end.x, end.y, end.z - 1)
    return (new_shape_start, new_shape_end)


def update_seen(items_at_z, item):
    for i in range(item[0].z, item[1].z + 1):
        items_at_z[i].append(item)


def solve_1(input):
    input.sort(key=lambda x: x[1].z)
    items_at_z = defaultdict(lambda: [])
    top_z_index = 0
    depends_from = defaultdict(lambda: [])
    for i in range(len(input)):
        if input[i][0].z == 1:
            # already on floor
            update_seen(items_at_z, input[i])
            top_z_index = max(top_z_index, input[i][1].z)
            depends_from[input[i]] = []
        else:
            # try to move down
            new_shape = input[i]

            # start positioning from top of last item
            start, end = new_shape
            new_shape_diff = end.z - start.z
            new_shape_start = Point(start.x, start.y, top_z_index + 1)
            new_shape_end = Point(end.x, end.y, new_shape_start.z + new_shape_diff)
            new_shape = (new_shape_start, new_shape_end)

            end_found = False
            while not end_found:
                possible_new_shape = move_down(new_shape)
                if possible_new_shape[0].z < 1 or possible_new_shape[1].z < 1:
                    end_found = True
                else:
                    possible_new_shape_z_range = list(
                        range(possible_new_shape[0].z, possible_new_shape[1].z + 1)
                    )
                    for index in possible_new_shape_z_range:
                        for item in items_at_z[index]:
                            if not is_possible(item, possible_new_shape):
                                end_found = True
                                depends_from[new_shape].append(item)

                    if not end_found:
                        new_shape = possible_new_shape

            # if new_shape != input[i]:
            input[i][0].z = new_shape[0].z
            input[i][1].z = new_shape[1].z
            update_seen(items_at_z, input[i])
            top_z_index = max(top_z_index, input[i][1].z)
            
    depends_from = defaultdict(lambda: [])
    connected = defaultdict(lambda: [])
    for i in range(len(input)):
        item = i + 1
        possible_new_shape = move_down(input[i])

        for j in range(i - 1, -1, -1):
            if not is_possible(input[j], possible_new_shape):
                # i depends on j
                depends_from[input[i]].append(input[j])
                connected[input[j]].append(input[i])

    critical = set()
    for k, v in depends_from.items():
        if len(v) == 1:
            critical.add(v[0])
    
    xxxx = 0
    counter = []
    for c in critical:
        counter = []
        visited = set()
        queue = deque()
        queue.append(c)
        while queue:
            item = queue.popleft()
            visited.add(item)
            counter.append(item)
            
            for connect in connected[item]:
                all_deps = depends_from[connect]
                if len(set(all_deps).intersection(visited)) == len(all_deps):
                    # all items are visited, can proceed
                    queue.append(connect)
                else:
                    # item has other sub-items do not proceed
                    pass
        # print("count", DICTTT[c], counter)
        xxxx += len(counter)-1
        
    print("Solution 1", len(input) - len(critical))
    print("Solution 2", xxxx)
    
    


def solve_2(input):
    return "??"


input = read_input()
write_output(solve_1(input), solve_2(input))
