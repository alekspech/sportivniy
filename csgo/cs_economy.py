import json
import os
from pprint import pprint
from typing import Dict, List
from collections import OrderedDict
import cs_tools

data_path = r'C:\Users\User\sasha_the_coder\datasets\csgo.dataset\csgo.dataset\cs_go.economy.json'
with open(data_path, 'r') as f:
    cs_economy = json.load(f)
pprint(cs_economy[5])

def format_economy(cs_economy: List[Dict]):
    out = []
    for match in cs_economy:
        match_info = f"{match['date']}: {match['team_1']} vs {match['team_2']}"
        out.append(match_info)
    return out

pprint(format_economy(cs_economy[:10]))

def map_rounds_economy(cs_economy_match:Dict):
    out_t1 = []
    out_t2 = []
    for round in range(1,31):
        # print(round)
        t1_key = f'{round}_t1'
        t2_key = f'{round}_t2'
        # print(cs_economy_match[t1_key])
        out_t1.append(cs_economy_match[t1_key])
        out_t2.append(cs_economy_match[t2_key])
    return out_t1, out_t2

t1_economy, t2_economy = map_rounds_economy(cs_economy[4])
