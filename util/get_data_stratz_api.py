import os
import json
import urllib.request
from util.dota_resource import get_patch_heroes_num

PATH = "data"


def _get_multiple_params(strings, name):
    """
    :param strings: list of input strings
    :return: string of url param
    """

    res_str = ""
    for string in strings:
        res_str += "&" + name + "=" + string
    return res_str.strip("&")


def download_json(url):
    """
    :param url: address to download data
    :return: void
    :process: download the data
    """

    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))

    return data


def dump_json_to_file(url, file_name):
    """
    :param url: address to download data
    :param file_name: the .json file name
    :return: void
    :process: dump a .json file to /data directory
    """

    # download the data
    json_data = download_json(url)

    # save data to .json file
    dest_dir = os.path.join(os.path.pardir, PATH, file_name)
    with open(dest_dir, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


def dump_dict_to_json(dict, file_name):
    """
    :param dict: the dict data
    :param file_name: output file name
    :return:
    """
    dest_dir = os.path.join(os.path.pardir, PATH, file_name)
    with open(dest_dir, 'w', encoding='utf-8') as json_file:
        json.dump(dict, json_file, ensure_ascii=False)


def generate_heroes_dryad_url(heroID, rank, take, week=0, matchlimit=-1):
    """
    :param heroID: [integer] the hero you want to query
    :param rank: [list of str] 1-7 map to lowest tier to highest tier
    :param take: [integer]the matchup amount of heroes you want. ie 115 for every
    :param week: [integer]leave null is current week
    :return: request url to get the synergy and counter rating data
    """

    url = "https://api.stratz.com/api/v1/Hero/" + str(heroID) \
          + "/dryad?take=" + str(take) + "&"
    url += _get_multiple_params(rank, "rank")
    if week != 0:
        url += "&week=" + str(week)
    if matchlimit != -1:
        url += "&matchlimit=" + str(matchlimit)

    print(url)

    return url


def get_heroes_dryad_by_heroID(heroID, week=0, matchlimit=-1):
    """
    :param heroID: the heroID you want to query
    :param week: if you leave week empty, means current week
    :param matchlimit: the limit of the count games in order to make the statistic results more reliable
    :return: json_file[dict] from api.stratz.com
    :return: current_week[integer] leave week=0 and get the current week
    """
    rank = ["6", "7"]
    download_url = generate_heroes_dryad_url(heroID, rank, get_patch_heroes_num(), week, matchlimit)
    json_file = download_json(download_url)
    current_week = json_file[0]["with"][0]["week"]

    # Info test
    print(current_week)

    return json_file, current_week


def generate_hero_directory_detail_url(rank, minTime=0, maxTime=45):
    """
    :param heroId: list of string
    :param week: Unix timestamp - integer
    :param rank: list of string
    :param lane: list of string
    :param role: list of string
    :param minTime: integer
    :param maxTime: integer
    :param orderBy: list of string: Available value: Win, Loss, Pick, Synergy, Advantage, Disadvantage
    :return: final url
    :instruction:
    In order to make the request more simple, several entities will be left with null as default
    """

    url = "https://api.stratz.com/api/v1/Hero/directory/detail?"
    # url += get_multiple_params(heroId, "heroId")
    # url += "&week=" + str(week)
    url += _get_multiple_params(rank, "rank")
    # url += "&" + get_multiple_params(lane, "lane")
    # url += "&" + get_multiple_params(role, "role")
    url += "&minTime=" + str(minTime)
    url += "&maxTime=" + str(maxTime)
    # url += "&orderBy=" + orderBy

    return url


def get_hero_directory_detail_json_by_endTime(endTime):
    """
    :param endTime: end time of the game filter
    :return: json file
    default: rank = 6 & 7 for Ancient & Divine
    """

    rank = ["6", "7"]  # Ancient & Divine
    url = generate_hero_directory_detail_url(rank, 0, endTime)
    json_data = download_json(url)
    return json_data


# main for test
if __name__ == '__main__':
    rank_list = ["6", "7"]  # Ancient & Divine
    url = generate_hero_directory_detail_url(rank_list, 0, 12)
    print(url)
    # dump_json_to_file(url, "data_test_48.json")
