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
for i in range(len(cs_data)):
    player_match = cs_data[i]
    player_pretty_name = crasivoe_name(player_match)
    if player_match['player_name'] =='s1mple':
        print(player_pretty_name)