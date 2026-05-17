from typing import Dict, List
from collections import OrderedDict

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
def count_player_deaths(cs_data , player_to_find):
    deaths_count = 0
    for i in range(len(cs_data)):
        player_name = cs_data[i]['player_name']
        if player_name == player_to_find:
            deaths_count += cs_data[i]['deaths']
    return deaths_count
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
def filter_player_names(cs_data, player_names):
    out = []
    for player_game in cs_data:
        player_name = player_game['player_name']
        if player_name in player_names:
            out.append(player_game)
    return out

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

def group_player_matches(cs_data):
    out = {}
    for player_match in cs_data:
        name = player_match['player_name']
        if name not in out:
            out[name] = []
        out[name].append(player_match)
    return out

def group_team_matches(cs_data):
    out = {}
    for player_match in cs_data:
        name = player_match['team']
        if name not in out:
            out[name] = []
        out[name].append(player_match)
    return out
def group_event(cs_data):
    out = {}
    for player_match in cs_data:
        name = player_match['event_name']
        if name not in out:
            out[name] = []
        out[name].append(player_match)
    return out

def format_event(event_group, event_name):
    event_matches = event_group[event_name]
    event_players = map_player_names(event_matches)
    event_teams = map_team_names(event_matches)
    event_info = f'{event_name}: with {len(event_teams)} teams and {len(event_players)} players'
    return event_info

def format_event_teams(event_group, event_name):
    event_matches = event_group[event_name]
    event_teams = group_team_matches(event_matches)
    event_info = ''
    for team_name in event_teams.keys():
        team_matches = event_teams[team_name]
        team_players = map_player_names(team_matches)
        event_info += f'{event_name}: {team_name}:{team_players}\n'
    return event_info

def format_event_matches(event_group, event_name):
    event_matches = event_group[event_name]
    event_teams = group_team_matches(event_matches)
    event_info = ''
    visited_matches = []
    for match in event_matches:
        match_id = match['match_id']
        if match_id in visited_matches:
            continue
        visited_matches.append(match_id)
        team_1_name = match['team']
        team_2_name = match['opponent']
        team_1_matches = event_teams[team_1_name]
        team_2_matches = event_teams[team_2_name]
        team_1_players = map_player_names(team_1_matches)
        team_2_players = map_player_names(team_2_matches)
        event_info += f'{event_name}: {team_1_name}:{team_1_players} vs {team_2_name}:{team_2_players}\n'
    return event_info
