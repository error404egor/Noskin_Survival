from consts import Tiles_dict


def load_layer_as_list(file: str) -> list:
    with open(file, "r") as map_:
        level_map = []
        for line in map_:
            line = line.strip()
            level_map.append(line)
        return level_map


def rework_map_as_0_1(level):
    result = []
    data = level[0][0]
    for elem in data:
        pr_result = []
        for elem_1 in elem:
            pr_result.append(int(Tiles_dict[elem_1]['transparency']))
        result.append(pr_result)
    return result