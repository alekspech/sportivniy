import json
from typing import Dict, List

def home_name_score_from_match(match_data):
    home_team_name = match_data['homeTeam']['name']
    score = match['score']['fullTime']
    home_score = score['homeTeam']
    return home_team_name, home_score 

def away_name_score_from_match(match_data):
    away_team_name = match_data['awayTeam']['name']
    score = match['score']['fullTime']
    away_score = score['awayTeam']
    return away_team_name, away_score 

    
    
data_path = '/Users/ila/sasha_the_coder/soccer_premier_league_statistic.json'
data_file = open(data_path, mode='r')#чтение из файла
data: Dict = json.load(data_file)
data_file.close()  
matches_data: List[Dict] = data['matches'] 
print(len(matches_data))
match_number = 0
for match in matches_data:
    match_number += 1 
    
    home_team_name, home_score = home_name_score_from_match(match)
    away_team_name, away_score = away_name_score_from_match(match)
    # 1. вывести дату матча подсказка внутри матча ключ utcDate
    # 2. из прошлого файла выписать имена наших функций и что они делают
    # select_matches_no_team - выбрать номера матчей, где команда не играла  
    # ... и так все функции  
    # 3. повторить вопросы
    utсDate = match['utcDate']


    score_info = '{} {} {}:{} {} {}'.format(
        match_number,
        home_team_name,
        home_score,
        away_score,
        away_team_name,
        utсDate
    )
    print(score_info)

# select_matches_no_team выбрать матч где не играла команда
# select_matches_with_team выбрать матч где играла команда
# select_matches_with_team_winner выбрать матч где команда играла и выиграла 
# select_matches_deat_heat выбрать матч где команда сыгралп в ничью 
# select_matches_with_team_looser вабрапть матч где команда играла и проиграла
# history_analyse история анализа  
text = 'gt556r556657tyhghhyrt'
if '!' in text:
    print('восклицательный знак найден')
else:
    print('восклицательный знак не найден')
# digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] 
digits = '0, 1, 2, 3, 4, 5, 6, 7, 8, 9'
for i in range(len(text)):
    if text[i] in digits:
        print('{} число'.format(text[i]))
    else:
        print('{} не число'.format(text[i]))