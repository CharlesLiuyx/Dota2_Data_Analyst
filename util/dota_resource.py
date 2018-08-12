import json
import os


def _load_json_file(dir):
    """
    :param dir: file directory
    :return: load json file as return
    """
    # directory = os.path.join(os.path.pardir, "data", "heroes.json")
    with open(dir, "r", encoding="utf-8") as f:
        json_file = json.load(f)
    return json_file


def get_mata_data_directory():
    """
    :return: path about heroes.json which contains info about heroes
    """
    return os.path.join(os.path.pardir, "data", "heroes.json")


def get_patch_heroes_num():
    """
    :return: [integer]the num of patch total heroes
    7.17 TODO need to description at README.md and modify by dota2 patch
    """
    return 115


def map_heroId_to_heroName_dict(dir, heroIds):
    """
    :param dir: json file directory
    :param heroIds: heroIds list
    :return: dict of heroes_name
    dict = {heroId[integer] : hero_name[string]}
    """
    json_file = _load_json_file(dir)

    heroes_names = {}
    for heroId in heroIds:
        heroes_names[heroId] = json_file[str(heroId)]["localized_name"]

    # print(len(json_file))

    return heroes_names


def get_heroID_list(dir):
    """
    :return: heroID_list: [list of string] heroID is not consecutive
    dir is needed because of the out-place reference
    """
    json_file = _load_json_file(dir)
    heroID_list = []
    for _, v in json_file.items():
        heroID_list.append(v["id"])

    return heroID_list


def map_heroName_to_heroId_dict(dir):
    """
    :param dir: json file directory
    :return: heroId dict[dict]
    {hero_name[string]:hero_id[integer]}
    """
    heroes_name_dict = map_heroId_to_heroName_dict(dir, get_heroID_list(dir))
    heroId_dict = {value: key for key, value in heroes_name_dict.items()}
    return heroId_dict


def get_heroID_to_heroName_dict():
    """
    :return: dict {heroId[integer]:hero_name[string]} 115 heroes
    """
    dir = get_mata_data_directory()
    heroIds = get_heroID_list(dir)
    return map_heroId_to_heroName_dict(dir, heroIds)


# main for test
if __name__ == '__main__':
    dir = get_mata_data_directory()
    heroIds = [16, 17, 99, 112, 81, 47, 119, 77, 57, 100]
    print(map_heroId_to_heroName_dict(dir, heroIds))

    print(get_heroID_list(dir))
