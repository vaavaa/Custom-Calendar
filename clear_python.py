import datetime
from timeit import default_timer as timer
from datetime import timedelta

# 0. 60 Code Lines
# 1. Получаем год из даты которую запросили
# 2. Прибавляем к году N лет (в целом можно хоть 1000 лет) (Это доп параметр)
# 3. Генерим возможные варианты дат c ограничением по дню недели
# 4. Сравниваем каждую получившуюся дату с запрошенной,
# 5. Если дата больше, то записываем ее в итоговый массив
# 6. Сортируем массив по возрастанию.
# 7. Берем первый элемент из итового массива - это и есть ответ.
def calculate_date_faster(date_string='09.07.2010 23:36',
                          day_matrix='0,45;12;1,2,6;3,6,14,18,21,24,28;1,2,3,4,5,6,7,8,9,10,11,12;',
                          # '0,45;0,4,8,12,17,22;2,6;1,2,3,4,5,11,18,24;1,2,3,9,11;',
                          years_count=0):
    start_time = timer()
    if years_count < 0:
        print('Нужно минимум +1 год. Указали {0}.'.format(years_count))

    date_time = convert_string_to_date(date_string)
    daymatrix = format('{0}{1}').format(day_matrix, str(date_time.year))
    for yr in range(years_count):
        daymatrix = format('{0},{1}').format(daymatrix, str(date_time.year + yr + 1))
    daymatrix = format('{0}{1}').format(daymatrix, ';')

    matrix = split_string_by_sep(daymatrix, ';', ',')
    minutes = matrix[0]
    hours = matrix[1]
    weekdays = matrix[2]
    days = matrix[3]
    month = matrix[4]
    years = matrix[5]

    # df_matrix_dates = pd.DataFrame()
    gen_dates = []
    for yr in years:
        for mn in month:
            for d in days:
                for hr in hours:
                    for min in minutes:
                        date_str = '{0}.{1}.{2} {3}:{4}'.format(d, mn, yr, hr, min)
                        day_date_time = convert_string_to_date(date_str)
                        # Получаем американский формат дня недели
                        if int(day_date_time.strftime("%w")) in weekdays:
                            if day_date_time > date_time:
                                gen_dates.append(day_date_time)

    gen_dates.sort()
    next_date = gen_dates[0]
    end_time = timer()
    print('Next date is: {0}; Elapsed time: {1}'.format(next_date, timedelta(seconds=end_time - start_time)))
    return next_date


def split_string_by_sep(string, delimiter, delimiter1):
    result = [x for x in string.split(delimiter)]
    result = result[:-1]
    minutes = [u for u in (result[0].split(delimiter1))]
    hours = [u for u in (result[1].split(delimiter1))]
    # Нестанадртные вводные данные по дню недели:
    # используется американский календарь,
    # в котором 1 – это воскресенье, 2 – понедельник и т.д.
    # Мы должны отнять 1 от вводных данных
    weekdays = [int(u) - 1 for u in (result[2].split(delimiter1))]
    days = [u for u in (result[3].split(delimiter1))]
    month = [u for u in (result[4].split(delimiter1))]
    years = [u for u in (result[5].split(delimiter1))]
    return [minutes, hours, weekdays, days, month, years]


def convert_string_to_date(date_string):
    format_str = '%d.%m.%Y %H:%M'  # The format
    datetime_obj = datetime.datetime.strptime(date_string, format_str)
    return datetime_obj
