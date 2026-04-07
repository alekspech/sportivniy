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
players_assists = cs_tools.map_player_names(kills_filtered)


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
# pprint(format_players_info(deaths_filtered))

player_filtered = filter_player_names(cs_data, ['s1mple', 'ZywOo'])
player_filtered = sorted(player_filtered, key=lambda x: x['kills'], reverse=True)
format_games = format_players_info(player_filtered)
# pprint(format_games)
# sort_all = sorted(cs_data, key=lambda x: (x['kills'], x['assists']))
# pprint(format_players_info(sort_all[-5:]))
# pprint(format_players_info(sort_all[:5]))

sort_all = sorted(cs_data, key=lambda x: (x['deaths']), reverse=True)
# pprint(format_players_info(sort_all[-5:]))
# pprint(format_players_info(sort_all[:5]))

sort_all = sorted(cs_data, key=lambda x: (x['adr']), reverse=True)
# pprint(format_players_info(sort_all[-5:]))
print(sort_all[0])