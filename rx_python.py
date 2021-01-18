import rx
import datetime
from timeit import default_timer as timer
from datetime import timedelta, datetime
from clear_python import convert_string_to_date

gen_dates = []


def calculate_date_rx(date_string='09.07.2010 23:36',
                      day_matrix='0,45;12;1,2,6;3,6,14,18,21,24,28;1,2,3,4,5,6,7,8,9,10,11,12;',
                      years_count=1):
    start_time = timer()
    print('Method RX. date_string = {0} day_matrix={1} years_count={2}'.format(date_string, day_matrix, years_count))
    if years_count < 1:
        print('Нужно минимум +1 год. Указали {0}.'.format(years_count))
        end_time = timer()
        return None, timedelta(seconds=end_time - start_time)

    init_date = convert_string_to_date(date_string)
    years_set = rx.range(init_date.year, init_date.year + years_count, 1)
    split_result = split_string_by_sep(day_matrix, ';')
    matrix = []
    for i in split_result:
        matrix.append(rx.from_list(list(map(int, i.split(',')))))

    years_set.subscribe(
        on_next=lambda yr: matrix[4].subscribe(
            lambda mn: matrix[3].subscribe(
                lambda day: matrix[1].subscribe(
                    lambda hr: matrix[0].subscribe(
                        lambda minute: create_date(yr, mn, day, hr, minute, init_date, matrix[2])
                    )
                )
            )
        )
    )

    end_time = timer()
    return None, timedelta(seconds=end_time - start_time)


def split_string_by_sep(string, delimiter):
    result = [x for x in string.split(delimiter)]
    return result[:-1]


def create_date(yr, mn, d, hr, minute, date_time, weekdays):
    # Формируем дату для загрузки в сет
    try:
        day_date_time = datetime(int(yr), int(mn), int(d), int(hr), int(minute))
        if day_date_time > date_time:
            # Получаем американский формат дня недели
            weekdays.subscribe(
                lambda week_day: add_date(week_day,day_date_time)
            )
    except ValueError:
        pass


def add_date(week_day, day_date_time):
    if int(day_date_time.strftime("%w")) == week_day:  # weekdays:
        # Если полученная дата больше чем исходная, то загружаем в сет
        gen_dates.append(day_date_time)
