import datetime
from timeit import default_timer as timer
from datetime import timedelta


# 0. 53 Code Lines
# 1. Получаем год из даты которую запросили
# 2. Прибавляем к году N лет (в целом можно хоть 1000 лет) (Это доп параметр)
# 3. Генерим возможные варианты дат c ограничением по дню недели
# 4. Сравниваем каждую получившуюся дату с запрошенной,
# 5. Если дата больше, то записываем ее в итоговый массив
# 6. Сортируем массив по возрастанию.
# 7. Берем первый элемент из итогового массива - это и есть ответ.
def calculate_date_faster(date_string='09.07.2010 23:36',
                          day_matrix='0,45;12;1,2,6;3,6,14,18,21,24,28;1,2,3,4,5,6,7,8,9,10,11,12;',
                          years_count=2):
    start_time = timer()
    if years_count < 1:
        print('Нужно минимум +1 год. Указали {0}.'.format(years_count))
        end_time = timer()
        return None, timedelta(seconds=end_time - start_time)

    date_time = convert_string_to_date(date_string)
    day_matrix = format('{0}{1}').format(day_matrix, str(date_time.year))
    for yr in range(years_count - 1):
        day_matrix = format('{0},{1}').format(day_matrix, str(date_time.year + yr + 1))
    day_matrix = format('{0};').format(day_matrix)

    matrix = split_string_by_sep(day_matrix, ';', ',')

    gen_dates = []
    for yr in matrix[5]:  # years:
        for mn in matrix[4]:  # month:
            for d in matrix[3]:  # days:
                for hr in matrix[1]:  # hours:
                    for minute in matrix[0]:  # minutes:
                        # Формируем дату для загрузки в сет
                        try:
                            day_date_time = datetime.datetime(int(yr), int(mn), int(d), int(hr), int(minute))
                            # Получаем американский формат дня недели
                            if int(day_date_time.strftime("%w")) in matrix[2]:  # weekdays:
                                # Если полученная дата больше чем исходная, то загружаем в сет
                                if day_date_time > date_time:
                                    gen_dates.append(day_date_time)
                        except ValueError:
                            pass

    gen_dates.sort()
    end_time = timer()
    return_value = [None] * 2
    if len(gen_dates) > 0:
        return gen_dates[0], timedelta(seconds=end_time - start_time)
    else:
        return None, timedelta(seconds=end_time - start_time)


def split_string_by_sep(string, delimiter, delimiter1):
    result = [x for x in string.split(delimiter)]
    result = result[:-1]
    minutes = [u for u in (result[0].split(delimiter1))]
    hours = [u for u in (result[1].split(delimiter1))]
    # Нестанадртные вводные данные по дню недели:
    # используется американский календарь,
    # в котором 1 – это воскресенье, 2 – понедельник и т.д.
    # Мы должны отнять 1 от вводных данных, т.е. week начинается с 0 in python
    weekdays = [int(u) - 1 for u in (result[2].split(delimiter1))]
    days = [u for u in (result[3].split(delimiter1))]
    month = [u for u in (result[4].split(delimiter1))]
    years = [u for u in (result[5].split(delimiter1))]
    return [minutes, hours, weekdays, days, month, years]


def convert_string_to_date(date_string):
    datetime_obj = datetime.datetime.strptime(date_string, '%d.%m.%Y %H:%M')
    return datetime_obj
