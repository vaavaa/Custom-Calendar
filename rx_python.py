from operator import methodcaller

import rx
from rx import of, operators as op
from timeit import default_timer as timer
from datetime import timedelta, datetime
from rx.subject import Subject

from clear_python import convert_string_to_date


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
    result_set = []
    for i in split_result:
        result_set.append(rx.from_list(list(map(int, i.split(',')))).filter())

    end_time = timer()
    return None, timedelta(seconds=end_time - start_time)


def split_string_by_sep(string, delimiter):
    result = [x for x in string.split(delimiter)]
    return result[:-1]
