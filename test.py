import random

random_number = random.randint(1, 10)
input_value = input('Введите число от 1 до 10:')
if not input_value.isdigit():
    print('Введите число')
    exit()
input_value = int(input_value)
if input_value == random_number:
    print('Правильно')
else:
    print('не правильно')
    print(random_number)