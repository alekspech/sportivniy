import json
import os
from pprint import pprint
from typing import Dict
from collections import OrderedDict
import cs_tools

# data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.players.main_stats_01k_2020.json'
data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.players.main_stats_2020.json'
with open(data_path, 'r') as f:
    cs_data = json.load(f)

# team_info(cs_data, 'FaZe')
teams = cs_tools.map_team_names(cs_data)


players = cs_tools.map_player_names(cs_data)
# pprint(players)
# print(len(players))


d = cs_tools.count_player_deaths(cs_data, 's1mple')
# print(d)
kills_filtered = cs_tools.filter_kills_gte(cs_data, kills=50)
# pprint(kills_filtered)
players_kills = cs_tools.map_player_names(kills_filtered)
# print(players_kills)

# cs_data_main = map_main_stats(cs_data)
# print(len(players_kills))
# deaths_kills_filtered = filter_deaths_lt(kills_filtered, deaths=20)
# print((map_player_names(deaths_kills_filtered)))
# noobs_kills_filtered = filter_kills_lt(cs_data, kills=20)
# noobs_deaths_filtered = filter_deaths_gt(noobs_kills_filtered, deaths=50)
# print('noobs death filter', (noobs_deaths_filtered))
# print('noobs kill filter', len(noobs_kills_filtered))



assists_filtered = cs_tools.filter_assists_gte(cs_data, assists=30)
kills_assists_filtered = cs_tools.filter_kills_lte(assists_filtered, kills=60)
players_assists = cs_tools.map_player_names(kills_filtered)


# cs_data_main = map_main_stats(cs_data)
# assists_filtered = filter_assists_gt(cs_data, assists=30)
# noobs_kills_filtered = filter_kills_lt(kills_filtered, kills=60)
# print('assists filter', (assists_filtered))
# print('noob kills filter', len(noobs_kills_filtered))



# pprint(format_players_info(kills_assists_filtered))


deaths_filtered = cs_tools.filter_deaths_gte(cs_data, deaths=30)
adr_filtered = cs_tools.filter_adr_lte(deaths_filtered, adr=55)
# pprint(format_players_info(deaths_filtered))

player_filtered = cs_tools.filter_player_names(cs_data, ['s1mple', 'ZywOo'])
player_filtered = sorted(player_filtered, key=lambda x: x['kills'], reverse=True)
format_games = cs_tools.format_players_info(player_filtered)
# pprint(format_games)
# sort_all = sorted(cs_data, key=lambda x: (x['kills'], x['assists']))
# pprint(format_players_info(sort_all[-5:]))
# pprint(format_players_info(sort_all[:5]))

sort_all = sorted(cs_data, key=lambda x: (x['deaths']), reverse=True)
# pprint(format_players_info(sort_all[-5:]))
# pprint(format_players_info(sort_all[:5]))

sort_all = sorted(cs_data, key=lambda x: (x['adr']), reverse=True)
# pprint(format_players_info(sort_all[-5:]))
# print(sort_all[0])

def group_player_matches(cs_data):
    out = {}
    for player_match in cs_data:
        name = player_match['player_name']
        if name not in out:
            out[name] = []
        out[name].append(player_match)
    return out

player_group = group_player_matches(cs_data)
# pprint(player_group['apEX'])

def group_team_matches(cs_data):
    out = {}
    for player_match in cs_data:
        name = player_match['team']
        if name not in out:
            out[name] = []
        out[name].append(player_match)
    return out

team_group = group_team_matches(cs_data)
team_games = team_group['Vitality']
pprint(cs_tools.map_player_names(team_games))
