import numpy as np

def check_answer(true_answers, false_answers):
    answer = input('press + or - to next question...')
    if answer == '+':
        true_answers.append(random_number)  
    elif answer == '-':
        false_answers.append(random_number)
    else:
        print('error! use + or - in answer')
        answer = check_answer(true_answers, false_answers)
    return answer
      
questions_count  = 42
lower_bound = 1
upper_bound = questions_count + 1
previous_questions = []
true_answers = []
false_answers = []
questions_len = upper_bound - lower_bound
i = 0
while len(previous_questions) != questions_len:
    random_number = np.random.randint(lower_bound, upper_bound)
    if random_number in previous_questions:
        continue
    random_info = 'randomed {} in interval [{}, {}]'.format(random_number, lower_bound, questions_count)
    i += 1
    previous_questions.append(random_number)
    print('=' * 50)
    print(random_info)
    answer = check_answer(true_answers, false_answers)
    print('true answers:{}'.format(len(true_answers)))
    print('false answers:{}'.format(len(false_answers)))
    print('question {} of {}'.format(i, questions_len))