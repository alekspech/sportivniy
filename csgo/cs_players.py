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

# team_info(cs_data, 'FaZe')
teams = get_team_names(cs_data)
# pprint(teams)
# 1. написать функцию player_names, которая принимает cs_data, проходит по всем матчам игроков и сохраняет имя игрока в список, потом из списка делает set (множество), попробуй вызвать функцию
# 2. написать функцию player_deaths, которая принимает два параметра cs_data и player_name, считает количество смертей в отдельную переменную deaths_count, возвращает из функции эту переменную, протестируй с именами нескольких игр
def map_player_names(cs_data):
    out = []
    for i in range(len(cs_data)):
        player_name = cs_data[i]['player_name']
        out.append(player_name)
    out = set(out)
    return out

players = map_player_names(cs_data)
# pprint(players)
# print(len(players))
def map_player_deaths(cs_data , player_to_find):
    deaths_count = 0
    for i in range(len(cs_data)):
        player_name = cs_data[i]['player_name']
        if player_name == player_to_find:
            deaths_count += cs_data[i]['deaths']
    return deaths_count

d = map_player_deaths(cs_data, 's1mple')
# print(d)
def filter_kills_gt(cs_data, kills): #gt - greater than
    out = []
    for player_game in cs_data:
        player_kills = player_game['kills']
        if player_kills >= kills:
            out.append(player_game)
    return out

kills_filtered = filter_kills_gt(cs_data, kills=50)
# pprint(kills_filtered)
players_50_kills = map_player_names(kills_filtered)
print(players_50_kills)