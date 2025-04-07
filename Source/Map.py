import random

def input_raw(map_input_path):
    try:
        f = open(map_input_path, "r")
    except:
        print("Can not read file \'" + map_input_path + "\'. Please check again!")
        return None

    pacman_pos = [int(x) for x in next(f).split()]
    raw_map = [[int(num) for num in line if num != '\n'] for line in f]

    return (pacman_pos[0], pacman_pos[1]), raw_map


# random pacman position
def input_raw_2(map_input_path, random_pacman=True):
    try:
        f = open(map_input_path, "r")
    except:
        print("Can not read file '" + map_input_path + "'. Please check again!")
        return None

    pacman_pos = [int(x) for x in next(f).split()]
    raw_map = [[int(num) for num in line if num != '\n'] for line in f]
    print("Pacman position1: ", pacman_pos)

    if random_pacman:
        valid_positions = [(x, y) for y in range(len(raw_map))
                           for x in range(len(raw_map[y]))
                           if raw_map[y][x] == 0]  # chỉ chọn ô trống
        pacman_pos = random.choice(valid_positions)  # đây đã là tuple rồi!

    else:
        pacman_pos = (pacman_pos[0], pacman_pos[1])  # chuyển list thành tuple nếu không random

    print("Pacman position2: ", pacman_pos)

    return pacman_pos, raw_map


def read_map_level_1_monster(map_input_path):
    pacman_pos, raw_map = input_raw_2(map_input_path)
    monster_pos = None

    graph_map = {}
    empty_positions = []  # Danh sách các vị trí trống để tạo monster ngẫu nhiên

    for y in range(len(raw_map)):
        for x in range(len(raw_map[y])):
            if raw_map[y][x] != 1:  # Nếu không phải tường
                cur = (x, y)
                graph_map[cur] = []

                if x - 1 >= 0 and raw_map[y][x - 1] != 1:
                    left = (x - 1, y)
                    graph_map[left] = graph_map[left] + [cur]
                    graph_map[cur] = graph_map[cur] + [left]

                if y - 1 >= 0 and raw_map[y - 1][x] != 1:
                    up = (x, y - 1)
                    graph_map[up] = graph_map[up] + [cur]
                    graph_map[cur] = graph_map[cur] + [up]

                # Thêm vị trí trống vào danh sách
                empty_positions.append((x, y))

    # Chọn ngẫu nhiên một vị trí từ danh sách trống để đặt monster
    if empty_positions:
        monster_pos = random.choice(empty_positions)

        # Đặt giá trị monster vào vị trí ngẫu nhiên
        mx, my = monster_pos
        raw_map[my][mx] = 2  # Giả sử 2 là giá trị đại diện cho monster

    return graph_map, pacman_pos, monster_pos

