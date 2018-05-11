from util.get_data_stratz_api import get_heroes_dryad_by_heroID, dump_dict_to_json
from util.dota_resource import get_heroID_list, get_mata_data_directory, map_heroId_to_heroName_dict, \
    get_patch_heroes_num
import pandas as pd
import os
import json
import sys, getopt


def _get_meta_data(json_file, type_select="with", content_name="synergy"):
    """
    :param json_file: json file to process
    :param type_select[string]: with or vs
    :param content_name[string]: value of the data name
    :return: matrix_raw[dict]
    """
    matrix_raw = {}
    for data in json_file[0][type_select]:
        matrix_raw[data["heroId2"]] = data[content_name]
    return matrix_raw


def get_matrix_raw_dict(json_file, is_with=True, content_name="synergy"):
    """
    :param json_file: the json file to process
    :param is_with: True - with & False - vs
    :param content_name:
                "matchCount": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "networth": 0,
                "duration": 0,
                "firstBloodTime": 0,
                "cs": 0,
                "dn": 0,
                "goldEarned": 0,
                "xp": 0,
                "heroDamage": 0,
                "towerDamage": 0,
                "heroHealing": 0,
                "level": 0,
                "synergy": 0,
                "wins": 0
    :return: matrix_raw[dict]
    """
    if is_with == True:
        matrix_raw = _get_meta_data(json_file, "with", content_name)
    else: # is_with = False
        matrix_raw = _get_meta_data(json_file, "vs", content_name)
    return matrix_raw


def average_matrix(matrix1, matrix2, num):
    """
    :param matrix1: adder
    :param matrix2: adder2
    {"heroId1": {"heroId2":value ...} ... }
    :param num: the amount of the total terms
    :return:
    """
    dict = {}

    matrix_result = {}
    matrix_result[matrix1.keys()[0]] = dict


def get_all_heroes_sc_matrix_dict(week, matchlimit=-1, content_name="synergy"):
    """
    :param week: the week you want - week=2519 is 04/09/2018 - 04/15/2018
                 leave week=0 return current week number
    :param matchlimit: leave matchlimit=-1 will set this value as default
    :param content_name: the value you want to query
                    default is "synergy"
    :param week_num: the weeks you want to use.
    :return: with_matrix, vs_matrix
    { "heroId1" :
        {
            "heroId2" : value
            ... 70<num of rows<115
        }
      ...115
    }
    """
    dir = os.path.join("data", "heroes.json")
    hero_ids = get_heroID_list(dir)
    with_matrix = {}
    vs_matrix = {}
    for hero_id in hero_ids:
        json_temp, current_week = get_heroes_dryad_by_heroID(hero_id, week, matchlimit=matchlimit)
        with_matrix[hero_id] = get_matrix_raw_dict(json_temp, True, content_name)
        vs_matrix[hero_id] = get_matrix_raw_dict(json_temp, False, content_name)

    return with_matrix, vs_matrix


def average_all_heroes_sc_matrix_dict(week_start, week_num, matchlimit=-1, content_name="synergy"):
    """
    :param week_start: the start week, leave the api url week param 0, get the current week number
    :param week_num: amount of weeks
    :param matchlimit: 0 for 115
    :param content_name: default is "synergy"
    :return: with_matrix, vs_matrix
    """
    with_matrix = {}
    vs_matrix = {}
    with_array = []
    vs_array = []
    for i in range(week_num):
        week = week_start - i
        with_matrix_temp, vs_matrix_temp = get_all_heroes_sc_matrix_dict(week, matchlimit, content_name)
        with_array.append(with_matrix_temp)
        vs_array.append(vs_matrix_temp)

    dir = os.path.join("data", "heroes.json")
    heroId_list = get_heroID_list(dir)
    for heroId_main in heroId_list:
        with_matrix[heroId_main] = {}
        vs_matrix[heroId_main] = {}
        for heroId_target in heroId_list:
            with_average = 0
            vs_average = 0
            for i in range(week_num):
                if heroId_main != heroId_target:
                    with_average += with_array[i][heroId_main][heroId_target]
                    vs_average += vs_array[i][heroId_main][heroId_target]

            with_average /= week_num
            with_matrix[heroId_main][heroId_target] = with_average

            vs_average /= week_num
            vs_matrix[heroId_main][heroId_target] = vs_average

    # save json file to /data/
    with open(os.path.join("data","with_{0}_115by115.json".format(content_name)), "w") as f:
        json.dump(with_matrix, f)
    with open(os.path.join("data","vs_{0}_115by115.json".format(content_name)), "w") as f:
        json.dump(vs_matrix, f)
    print("Save json to local successful!")

    return with_matrix, vs_matrix


def dump_matrix_json_to_excel(matrix_name, matrix):
    """
    :param matrix_name: file name
    :param matrix[dict]: the json file you want to convert
    :return: pass
    generate the excel .xlsx file to /data directory
    """
    dir_heroes = os.path.join("data", "heroes.json")
    df = pd.DataFrame(matrix)
    df.columns = [int(x) for x in df.columns]
    df.index = [int(x) for x in df.index]
    df = df.sort_index()
    df = df.sort_index(axis=1)
    heroes_name1 = map_heroId_to_heroName_dict(dir_heroes, df.columns)
    df.columns = heroes_name1.values()
    heroes_name2 = map_heroId_to_heroName_dict(dir_heroes, df.index)
    df.index = heroes_name2.values()
    df = df.T
    # print(heroes_name1.values())
    writer = pd.ExcelWriter("{0}_115by115.xlsx".format(matrix_name))
    df.to_excel(writer, sheet_name='Sheet')
    writer.save()
    # print(df)


def process_heroes_with_vs_matrix_to_excel(is_update=True, week_num=0, content_name="synergy"):
    """
    :param is_update: Set True download data from Stratz.com
                      Set False load json file locally
    :param week_num: 0 as default with 1 week (current week)
                     >0 weeks amount
    :return: pass
    process data to dump the json to excel locally
    """
    if is_update:
        # TODO change the params here
        if week_num == 0:
            with_synergy_matrix, vs_synergy_matrix = get_all_heroes_sc_matrix_dict(
                week=2521,  # week=0 is current week
                matchlimit=0,  # make sure all 115 heroes contained
                content_name=content_name
            )
        else:
            with_synergy_matrix, vs_synergy_matrix = average_all_heroes_sc_matrix_dict(
                #  Please access Stratz API using
                #  https://api.stratz.com/api/v1/Hero/1/dryad?take=115&rank=6,7&matchlimit=0
                #  to get the current week number, for example 2522 is 4/30 - 5/6
                week_start=2522,
                #  the weeks amount
                week_num=3,
                #  matchlimit = 0 refer to the 115 heroes with no limitation
                matchlimit=0,
                #  the schema name
                content_name="synergy"
            )
    else:
        dir_with = os.path.join("data", "with_{0}_115by115.json".format(content_name))
        with open(dir_with, "r") as f:
            with_synergy_matrix = json.load(f)
        dir_vs = os.path.join("data", "vs_{0}_115by115.json".format(content_name))
        with open(dir_vs, "r") as f:
            vs_synergy_matrix = json.load(f)

    dump_matrix_json_to_excel("with_{0}".format(content_name), with_synergy_matrix)
    dump_matrix_json_to_excel("vs_{0}".format(content_name), vs_synergy_matrix)
    # print(with_matrix)
    # print(vs_matrix)


if __name__ == '__main__':
    process_heroes_with_vs_matrix_to_excel(
        is_update=False, # if you want to update to the latest match, change it to True
        week_num=0, # >0 means gather data of weeks
        content_name="synergy"
    )
