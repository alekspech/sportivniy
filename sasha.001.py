import random
# 1. Какие три основных типа данных используются в компьютере для представления величин реального мира? Привести один-два предмета или его свойства, представленного с помощью каждого из типа данных.

# 2. Что делает функция type()?

# 3. Что делает функция len()?

# 4. Какое ключевое слово и какой символ используется для вставки переменной в указанное место строки?

# 5. Одинаковые ли строки '2023-03-11' и '2023-03-11 '?

# 6. Ко всем ли типам данных можно обращаться с помощью индекса (операции []) и функции len()?

a = 10
b = 'Sasha Pichugin'
c = [ 1, 2, 3, 8,2412,124,12,41,24,12,41,4,12,341,23,123,1,24,12,51]
d = 23.33

# для каждой из переменных выше попробовать операцию выбора элемента по индесу через [] и попробовать функцию len

#===========решение тут===============
# print('+'*10)
# print('check a =', a)
# # print(len(a)) # TypeError: object of type 'int' has no len()
# # print(a[5]) # TypeError: 'int' object is not subscriptable
# print('+'*10)
# print('check b =', b)
# print(len(b))
# print(type(b))
# print(b[0:5])
# print(b[6:14])
# print(b[6:len(b)])
# print('+'*10)

# print('check c =', c)
# print('+'*10)

# print('check d =', d)
# print('+'*10)

# exit()
#=====================================

# 7. С помощью какого ключевого слова проверяется условие? Как проверить, что переменная строго равна определенному значению?

random_value = random.randint(0, 150)

# проверить, что random_value меньше 100, проверить, что число не равно 0
 
#===========решение тут===============
# print('value = ', random_value)
# if random_value < 100:
#     print('random_value < 100')
# else:
#     print('>=100')
# if random_value != 0:
#     print('!=0')

# exit()
#=====================================


# 8. Где применяются и как работают ключевые слова and и or?

random_value = random.randint(-150, 150)

# проверить, что число random_value положительное число и меньше 100

#===========решение тут===============
# print('check', random_value)
# if random_value >= 0 and random_value < 100:
#     print('число random_value положительное число и меньше 100')
# else:
#     print('no')
# exit()
#=====================================

# 9. С помощью какой функции можно быстро сделать интервал чисел от 0 до 100?

interval = list(range(500, 550))

# пройтись по значениям в этом интервале и вывести каждое из них с новой строчки в консоль
# сделать интервал от 500 до 550

#===========решение тут===============
# for i in range(500,550):
    # print(i)/
# exit()
#=====================================

# 10. С помощью какой функции можно дать пользователю ввести значение переменной с клавиатуры во время запуска программы?

# 11. С помощью какой функции можно моментально выйти из программы?

# 12. С помощью какого ключевого слова можно по очереди получить каждый элемент списка или каждый символ строки?

# 13. С помощью какого ключевого слова мы создаем функцию? Зачем у функции скобки?

random_value = random.randint(0, 100)

# написать функцию, первый аргумент которой принимает random_value (с другим именем переменной), второй аргумент - значение с которым мы сравниваем
# при вызове функции она должна в переменную записать True или False в зависимости от того больше ли второй аргумент первого

#===========решение тут===============
# def check(random_number , compare_with):
#     if compare_with > random_number:
#         return True
#     else:
#         return False
# check_with = 12345
# print('check if {} less {}'.format(random_value , check_with))
# result = check(random_value, check_with)
# print(result)
# exit() 
#=====================================

# 14. Зачем используется двоеточие и в каких случаях оно ставится в Python?

# найти в коде и перечислить все ключевые слова, после употребления которых встречается двоеточие

# ===========решение тут (в комментарии перечисли название найденных ключевых слов)==============

# =====================================

# 15. Зачем в Python используется табуляция (начало строки не с красной, а с одним или несколькими отступами)?

# 16. Как работают ключевые слова break и continue? В любом ли участке кода можно использовать эти слова?

sample_str = '12312412 dasdasg 124rqds 91035812'
spaces_counter = 0

# пройти по значениям sample_str и найти число пробелов ' ' (если символ не подходит делаем continue, иначе увеличиваем счетчик пробелов spaces_counter 

#===========решение тут===============

#=====================================


# 17. Как работает и где используется ключевое слово return?
#  
# 18. Как вывести несколько переменных с помощью функции print(), не используя форматирование через ''.format?

# 19. Как проверить наличие симлова в строке или списке?

shool_name = 'Gymnasium#23'

# проверить, что в названии школы shool_name есть номер 23

#===========решение тут===============

#=====================================

# 20. Как проверить, что символы в тексте являются числами?

# 21. С какого значения считается первый индекс элемента в строке? Возможна ли отрицательная индексация text[-3] и что она обозначает?

shool_name = 'Gymnasium#23'

# вывести первый символ из shool_name 
# вывести последний символ из shool_name 
# вывести последние два символа из shool_name (подсказка для интервала значений print(переменная[индекс_откуда:индекса_до_куда]))

#===========решение тут===============

#=====================================