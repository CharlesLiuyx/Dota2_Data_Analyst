from util.get_data_stratz_api import get_hero_directory_detail_json_by_endTime
from util.dota_resource import map_heroId_to_heroName_dict
import pandas as pd
import os
import json
import sys
import getopt


# Process the hero detail data to a single excel file

def get_heroes_feature_list(endTime):
    """
    :param endTime
    :return: dict data
    """
    data = get_hero_directory_detail_json_by_endTime(endTime)
    dict = {}
    for hero in data["heroes"]:
        dict[hero["heroId"]] = hero["heroTimeDetail"]["events"]
    return dict


def dump_all_columns_to_excel(output_path, min_endTime, max_endTime, step=1):
    """
    :param output_path: output directory path, pls using os.path.join
    if you want to get time=8
    :param min_endTime: = 8
    :param max_endTime: = 9
    :param step: = 1
    :return: void
    :process: Create the file at output_file
    """
    dir = os.path.join("data", "heroes.json")

    writer = pd.ExcelWriter(output_path)
    for endTime in range(min_endTime, max_endTime, step):
        dict = get_heroes_feature_list(endTime)
        dict_new = {}
        for k in dict:
            dict_new[k] = dict[k][0]
        df = pd.DataFrame(dict_new)
        new_column = df.index
        df = df.reset_index(df.columns).transpose()
        df.columns = new_column
        heroes_name = map_heroId_to_heroName_dict(dir, df.index)
        df.index = heroes_name.values()
        df.to_excel(writer, sheet_name=str(endTime))

        print("Completed Time=%d\n" % endTime)


def test_dump_all_columns_to_excel(output_path):
    dir = os.path.join("data", "data_test_48.json")
    with open(dir, "r") as f:
        data = json.load(f)
    dict = {}
    for hero in data["heroes"]:
        dict[hero["heroId"]] = hero["heroTimeDetail"]["events"]

    writer = pd.ExcelWriter(output_path)
    dict_new = {}
    for k in dict:
        dict_new[k] = dict[k][0]
    df = pd.DataFrame(dict_new)

    print(type(dict_new[1]))

    df = pd.DataFrame(dict_new)
    new_column = df.index
    df = df.reset_index(df.columns).transpose()
    df.columns = new_column
    df.to_excel(writer, sheet_name="test")


def main(argv):
    min_endTime = 6
    max_endTime = 60
    step = 6
    try:
        opts, args = getopt.getopt(argv, "hn:x:s:", ["help", "min=", "max=", "step="])
    except getopt.GetoptError:
        print("default: min_endTime=6 max_endTime=60 step=6\n")
    for opt, arg in opts:
        if opt == '-h':
            print("process_hero_directory_detail_to_csv.py -min <min_endTime_int> -max <max_endTime_int> -s <step_int>")
            sys.exit()
        elif opt in ("-n", "--min"):
            min_endTime = int(arg)
        elif opt in ("-x", "--max"):
            max_endTime = int(arg)
        elif opt in ("-s", "--step"):
            step = int(arg)

    print(min_endTime, max_endTime, step)
    file_name = "data.xlsx"
    output_path = os.path.join("data", file_name)
    dump_all_columns_to_excel(output_path, min_endTime, max_endTime, step)


if __name__ == '__main__':
    main(sys.argv[1:])
