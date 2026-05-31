import json
import os
from pprint import pprint
from typing import Dict
from collections import OrderedDict
import cs_tools

players_data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.players.main_stats_2020.json'
with open(players_data_path, 'r') as f:
    data = json.load(f)

economy_data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.economy.json'
with open(economy_data_path, 'r') as f:
    economy = json.load(f)

def build_matches(cs_data, cs_economy):
    matches = {}
    for player_game in cs_data:
        match_id = player_game['match_id']
        if match_id not in matches:
            matches[match_id] =  {
                'match_id':match_id, 
                'players':[],
                'economy':[]
            }
        matches[match_id]['players'].append(player_game)
    
    # Загрузили игры, грузим экономику
    for economy in cs_economy:
        match_id = economy['match_id']
        if match_id not in matches:
            # matches[match_id] =  {
            #     'match_id':match_id, 
            #     'players':[],
            #     'economy':[]
            # }
            continue
        matches[match_id]['economy'].append(economy)
    return matches

cs_matches = build_matches(cs_economy=economy, cs_data=data)
pprint(len(cs_matches[2339385]['players']))