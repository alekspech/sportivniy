import json
import os
from pprint import pprint
from typing import Dict
from collections import OrderedDict

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
def count_player_deaths(cs_data , player_to_find):
    deaths_count = 0
    for i in range(len(cs_data)):
        player_name = cs_data[i]['player_name']
        if player_name == player_to_find:
            deaths_count += cs_data[i]['deaths']
    return deaths_count

d = count_player_deaths(cs_data, 's1mple')
# print(d)
def filter_kills_gte(cs_data, kills): #gt - greater than, gte - greater than or equal
    out = []
    for player_game in cs_data:
        player_kills = player_game['kills']
        if player_kills >= kills:
            out.append(player_game)
    return out

def map_main_stats(cs_data):
    out = []
    for player_game in cs_data:
        new_data = OrderedDict({
            'player_name': player_game['player_name'],
            'team': player_game['team'],
            'opponnent': player_game['opponent'],
            'event_name': player_game['event_name'],
            'format': player_game['best_of'],
            'kills': player_game['kills'],
            'deaths': player_game['deaths'],
            'assists': player_game['assists'],
            'headshots': player_game['hs'],
            'assists': player_game['assists'],
            'adr': player_game['adr'],
        })
        out.append(new_data)
    return out


def filter_deaths_lte(cs_data, deaths): #lt - less than , lte - less than or equal
    out = []
    for player_game in cs_data:
        if player_game['deaths'] <= deaths:
            out.append(player_game)
    return out

def filter_deaths_gte(cs_data, deaths): 
    out = []
    for player_game in cs_data:
        if player_game['deaths'] >= deaths:
            out.append(player_game)
    return out

def filter_kills_lte(cs_data, kills): 
    out = []
    for player_game in cs_data:
        player_kills = player_game['kills']
        if player_kills <= kills:
            out.append(player_game)
    return out

kills_filtered = filter_kills_gte(cs_data, kills=50)
# pprint(kills_filtered)
players_kills = map_player_names(kills_filtered)
# print(players_kills)

# cs_data_main = map_main_stats(cs_data)
# print(len(players_kills))
# deaths_kills_filtered = filter_deaths_lt(kills_filtered, deaths=20)
# print((map_player_names(deaths_kills_filtered)))
# noobs_kills_filtered = filter_kills_lt(cs_data, kills=20)
# noobs_deaths_filtered = filter_deaths_gt(noobs_kills_filtered, deaths=50)
# print('noobs death filter', (noobs_deaths_filtered))
# print('noobs kill filter', len(noobs_kills_filtered))

def filter_assists_gte(cs_data, assists): 
    out = []
    for player_game in cs_data:
        if player_game['assists'] >= assists:
            out.append(player_game)
    return out

def filter_assists_lte(cs_data, assists): 
    out = []
    for player_game in cs_data:
        player_assists = player_game['assists']
        if player_assists <= assists:
            out.append(player_game)
    return out

assists_filtered = filter_assists_gte(cs_data, assists=30)
kills_assists_filtered = filter_kills_lte(assists_filtered, kills=60)
players_assists = map_player_names(kills_filtered)


# cs_data_main = map_main_stats(cs_data)
# assists_filtered = filter_assists_gt(cs_data, assists=30)
# noobs_kills_filtered = filter_kills_lt(kills_filtered, kills=60)
# print('assists filter', (assists_filtered))
# print('noob kills filter', len(noobs_kills_filtered))


def format_players_info(cs_data):
    out = []
    for player_game in cs_data:
        player_name = player_game['player_name']
        player_deaths = player_game['deaths']
        player_kills = player_game['kills']
        player_assists = player_game['assists']
        player_info = f'{player_name}: {player_kills}; {player_assists}; {player_deaths}; {player_game['hs']}'
        out.append(player_info)
    return out
# pprint(format_players_info(kills_assists_filtered))

def filter_player_names(cs_data, player_names):
    out = []
    for player_game in cs_data:
        player_name = player_game['player_name']
        if player_name in player_names:
            out.append(player_game)
    return out
s1mple_games = filter_player_names(cs_data, ['s1mple', 'electronic'])
# pprint(format_players_info(s1mple_games))

def filter_headshots_gte(cs_data, headshots): 
    out = []
    for player_game in cs_data:
        if player_game['hs'] >= headshots:
            out.append(player_game)
    return out

def filter_headshots_lte(cs_data, headshots): 
    out = []
    for player_game in cs_data:
        player_headshots = player_game['hs']
        if player_headshots <= headshots:
            out.append(player_game)
    return out
# s1mple_kills_filtered = filter_kills_gte(cs_data, kills=20)
# kills_assists_filtered = filter_headshots_gte(s1mple_kills_filtered, headshots=10)
# pprint(format_players_info(s1mple_games))

def filter_adr_gte(cs_data, adr): 
    out = []
    for player_game in cs_data:
        if player_game['adr'] >= adr:
            out.append(player_game)
    return out

def filter_adr_lte(cs_data, adr): 
    out = []
    for player_game in cs_data:
        player_adr = player_game['adr']
        if player_adr <= adr:
            out.append(player_game)
    return out
deaths_filtered = filter_deaths_gte(cs_data, deaths=30)
adr_filtered = filter_adr_lte(deaths_filtered, adr=55)
pprint(format_players_info(deaths_filtered))