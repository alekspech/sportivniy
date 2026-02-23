import json
import os
from pprint import pprint
from typing import Dict

def crasivoe_name(match: Dict):
    name = f'{match['date']}:{match['team']}:{match['player_name']}'
    return name

# data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.players.main_stats_01k_2020.json'
data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.players.main_stats_2020.json'
with open(data_path, 'r') as f:
    cs_data = json.load(f)
# pprint(cs_data[-2])
# player_match = cs_data[-2]
# print(player_match['player_name'])
# print(player_match['team'])
# player_pretty_name = crasivoe_name(player_match)
# print(player_pretty_name)
# for i in range(len(cs_data)):
#     player_match = cs_data[i]
#     player_pretty_name = crasivoe_name(player_match)
#     if player_match['player_name'] =='s1mple':
#         print(player_pretty_name)



# for i in range(len(cs_data)):
    # match_id = cs_data[i]
    # player_match = cs_data[i]
    # player_pretty_name = crasivoe_name(player_match)
    # if match_id ['match_id']== 2339390:
        # print(player_pretty_name)

def team_info(cs_data, team_name):
    player_counter = 0        
    player_names = []
    for i in range(len(cs_data)):
        player_match = cs_data[i]
        player_pretty_name = crasivoe_name(player_match)
        if player_match['team']== team_name:
            print(player_pretty_name)
            player_counter += 1
            player_names.append(player_match['player_name'])
    print('players', player_counter)
    player_names = set(player_names)        
    print(player_names)
    return player_names

def get_team_names(cs_data):
    names = []
    for i in range(len(cs_data)):
        names.append(cs_data[i]['team'])
        names.append(cs_data[i]['opponent'])
    names = set(names)
    return names

team_info(cs_data, 'FaZe')
teams = get_team_names(cs_data)
pprint(teams)