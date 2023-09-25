import datetime
days_of_week = ['понедельник' , 'вторник' , 'среда' , 'четверг' , 'пятница' , 'суббота' , 'воскресенье'] 
# функция , выбирающая матчи , в которых заданная команда не играла      
def select_matches_no_team(
        history_home_names,
        history_away_names,
        team_to_select
    ):
    selected_matches = []
    for i in range(len(history_home_names)):
        home_team_name = history_home_names[i]
        away_team_name = history_away_names[i]
        if home_team_name != team_to_select and away_team_name != team_to_select:
            selected_matches.append(i)
    return selected_matches

def select_matches_with_team(
        history_home_names,
        history_away_names,
        team_to_select
    ):
    selected_matches = []
    for i in range(len(history_home_names)):
        home_team_name = history_home_names[i]
        away_team_name = history_away_names[i]
        if home_team_name == team_to_select or away_team_name == team_to_select:
            selected_matches.append(i)
    return selected_matches

def select_matches_with_team_winner(
        history_home_names,
        history_away_names,
        team_to_select,
        history_home_goals,
        history_away_goals
    ):
    selected_matches = []
    for i in range(len(history_home_names)):
        home_team_name = history_home_names[i]
        away_team_name = history_away_names[i]
        home_goal = history_home_goals[i]
        away_goal = history_away_goals[i]
        if home_team_name == team_to_select:
            if home_goal > away_goal:
                selected_matches.append(i)
        if away_team_name == team_to_select:
            if away_goal > home_goal:
                selected_matches.append(i)
    return selected_matches

def select_matches_deat_heat(
        history_home_names,
        history_away_names,
        team_to_select, 
        history_home_goals, 
        history_away_goals
    ):
    selected_matches = []
    for i in range(len(history_home_names)):
        home_team_name = history_home_names[i]
        away_team_name = history_away_names[i]
        home_goal = history_home_goals[i]
        away_goal = history_away_goals[i]
        if home_team_name == team_to_select:
            if home_goal == away_goal:
                selected_matches.append(i)
        if away_team_name == team_to_select:
            if away_goal == home_goal:
                selected_matches.append(i)
    return selected_matches

def select_matches_with_team_looser(
        history_home_names,
        history_away_names,
        team_to_select,
        history_home_goals,
        history_away_goals
    ):
    selected_matches = []
    for i in range(len(history_home_names)):
        home_team_name = history_home_names[i]
        away_team_name = history_away_names[i]
        home_goal = history_home_goals[i]
        away_goal = history_away_goals[i]
        if home_team_name == team_to_select:
            if home_goal < away_goal:
                selected_matches.append(i)
        if away_team_name == team_to_select:
            if away_goal < home_goal:
                selected_matches.append(i)
    return selected_matches
    

def history_analyse(
        history_home_teams,
        history_away_teams,
        history_goals_home_teams,
        history_goals_away_teams,
        history_date_of_matches
    ):
    psg_home_goals = 0
    history_size = len(history_home_teams)
    print() 
    print('history of {} matches'.format(history_size))
    if history_size == 0:
        print('history without matches')
        return False
    
    # selected_matches =  select_matches_no_team(history_home_teams , history_away_teams , 'PSG' )
    # selected_matches =  select_matches_with_team(history_home_teams , history_away_teams , 'PSG' )
    # selected_matches =  select_matches_with_team_winner(history_home_teams , history_away_teams , 'PSG' , history_goals_home_teams , history_goals_away_teams )
    # selected_matches =  select_matches_deat_heat(history_home_teams , history_away_teams , 'Liverpol' , history_goals_home_teams , history_goals_away_teams )
    selected_matches =  select_matches_with_team_looser(
        history_home_teams,
        history_away_teams,
        'PSG', 
        history_goals_home_teams,
        history_goals_away_teams 
        )

    print('selected {} matches'.format(len(selected_matches)))
    # history analyse
    for i in range(history_size):
        if i not in selected_matches:
            continue
        home_team_goals = history_goals_home_teams[i]
        away_team_goals = history_goals_away_teams[i]
        home_team_name = history_home_teams[i]
        # print(home_team_name , len(home_team_name))
        away_team_name = history_away_teams[i]
        if home_team_name == 'PSG': 
            psg_home_goals = psg_home_goals + home_team_goals
        
        print()
        score_info = '{} {}::{} {}'.format(home_team_name , home_team_goals , away_team_goals , away_team_name)
        print(i)
        print(score_info)
        print(history_date_of_matches[i])
        date_of_match = datetime.datetime.strptime(history_date_of_matches[i],'%Y-%m-%d')
        if home_team_goals > away_team_goals:
            print('home team win')
        if away_team_goals > home_team_goals:
            print('away team win')
        if home_team_goals == away_team_goals:
            print('deat heat')

        match_day_number = datetime.datetime.weekday(date_of_match)
        match_day = days_of_week[match_day_number]
        print(match_day)
    return True





history_home_teams = ['PSG', 'PSG' , 'PSG'  , 'Bayern' , 'PSG' , 'Real Madrid' , 'Liverpol' , 'Liverpol' , 'Crystal Palace' , 'Wolves' , 'Liverpol' , 'Real Madrid']
history_away_teams = ['Brest' , 'Nant' , 'Marseille' , 'PSG' , 'Losk Lille' , 'Liverpol' , 'Mun Unt' , 'Real Madrid' , 'Liverpol' , 'Liverpol' , 'PSG' , 'Barselona']
history_goals_home_teams = [ 2 , 4 , 3 , 2 , 4 , 1 , 7 , 2 , 0 , 3  , 4  , 3]
history_goals_away_teams = [ 1 , 2 , 0 , 0 , 3 , 0 , 0 , 6 , 0 , 0  , 5  , 3]
history_date_of_matches = ['2023-03-11' , '2023-03-04' , '2023-01-26' , '2023-03-08' , '2023-01-19' , '2023-03-15' , '2023-03-05' , '2023-02-21' , '2023-02-25' ,  '2023-02-04' , '2023-03-27' , '2023-04-01'  ]
# result = history_analyse(history_away_teams , history_home_teams , history_goals_away_teams , history_goals_home_teams , history_date_of_matches)
# print(result)
history_size = len(history_home_teams)
scores_info = []
for i in range(history_size): 
    home_team_goals = history_goals_home_teams[i]
    away_team_goals = history_goals_away_teams[i]
    home_team_name = history_home_teams[i]

    away_team_name = history_away_teams[i]
    score_info = '{} {} {}:{} {}'.format(i , home_team_name , home_team_goals , away_team_goals , away_team_name)
    print(score_info)
    scores_info.append(score_info)
match_number_str = input('Введите номер матча:')
# d\s if буква in '1234567890'-букву можно перевести в число
corrected_match_number_str = ''  
for letter in match_number_str:
    if letter in '1234567890':
        # corrected_match_number_str += letter
        corrected_match_number_str = corrected_match_number_str + letter 
if len(corrected_match_number_str) == 0:
    print('Ошибка: не было введено ни одной цифры')
    exit()  
match_number = int(corrected_match_number_str)
print(corrected_match_number_str)
if match_number >= history_size:
    print('Ошибка: номер матча должен быть от 0 до {}'.format(history_size - 1))
    exit()
print('Выбран матч:',scores_info[match_number])
print() 
print('PROGRAM FINISH')         