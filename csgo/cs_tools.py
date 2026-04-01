from typing import Dict, List

def crasivoe_name(match: Dict):
    name = f'{match['date']}:{match['team']}:{match['player_name']}'
    return name

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

def map_team_names(cs_data):
    names = []
    for i in range(len(cs_data)):
        names.append(cs_data[i]['team'])
        names.append(cs_data[i]['opponent'])
    names = set(names)
    return names 

def map_player_names(cs_data):
    out = []
    for i in range(len(cs_data)):
        player_name = cs_data[i]['player_name']
        out.append(player_name)
    out = set(out)
    return out