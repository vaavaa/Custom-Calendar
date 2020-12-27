from io import StringIO
from timeit import default_timer as timer
from datetime import timedelta, datetime
import pandas as pd


# 0. 37 Code Lines
# 1. Получаем год из даты которую запросили
# 2. Прибавляем к году N лет (в целом можно хоть 1000 лет) (Это доп параметр)
# 3. Генерим возможные варианты дат без ограничений
# 5. Создаем доп колонку с днем недели и тип int32
# 6. Отбираем только те которые вошли в заданные дни недели
# 7. Ищем даты больше требуемой
# 8. Берем первый элемент из итогового массива - это и есть ответ.
def calculate_date_nice(date_string='09.07.2010 23:36',
                        day_matrix='0,45;12;1,2,6;3,6,14,18,21,24,28;1,2,3,4,5,6,7,8,9,10,11,12;',
                        years_count=1):
    start_time = timer()
    if years_count < 1:
        print('Нужно минимум +1 год. Указали {0}.'.format(years_count))

    df = pd.read_csv(StringIO(day_matrix),
                     header=None, usecols=[0, 1, 2, 3, 4], names=['minutes', 'hours', 'weekdays', 'days', 'months'],
                     sep=';', converters={i: str for i in range(5)})
    dfs = {}
    for col in df:
        dfs[col] = df[col].str.split(',', expand=True)
    if years_count == 1:
        years = pd.DataFrame([pd.to_datetime(date_string, format='%d.%m.%Y %H:%M').year])
    else:
        years = pd.DataFrame(
            [pd.to_datetime(date_string, format='%d.%m.%Y %H:%M').year + year for year in range(years_count)])
    dataset = []
    for year in years:
        for month in dfs['months']:
            for day in dfs['days']:
                for hour in dfs['hours']:
                    for minute in dfs['minutes']:
                        dataset.append(datetime(int(years[year][0]),
                                                int(dfs['months'][month][0]),
                                                int(dfs['days'][day][0]),
                                                int(dfs['hours'][hour][0]),
                                                int(dfs['minutes'][minute][0])))

    df_result = pd.DataFrame(dataset, columns=['date'])
    df_result['weekday'] = pd.Series(df_result.date.dt.strftime("%w"), dtype='int32')
    df_result = df_result[df_result['weekday'].isin([int(weekday) - 1 for weekday in dfs['weekdays'].iloc[0]])]

    mask = (df_result['date'] > pd.to_datetime(date_string, format='%d.%m.%Y %H:%M'))
    df_result_final = df_result.loc[mask]

    end_time = timer()
    print('Next date is: {0}; Elapsed time: {1}'.format(df_result_final.iloc[0].date.strftime("%d.%m.%Y %H:%M"),
                                                        timedelta(seconds=end_time - start_time)))
    return df_result_final.iloc[0]
