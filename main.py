import datetime

from clear_python import calculate_date_faster
from pandas_python import calculate_date_nice

if __name__ == '__main__':
    count_times = 1000
    total_timeCount = 0

    for i in range(count_times):
        #result = calculate_date_faster(day_matrix='45;12;1;29;2;', years_count=200)
        result = calculate_date_nice(day_matrix='45;12;1;29;2;', years_count=200)
        total_timeCount = total_timeCount + result[1].microseconds

    print('Total execution times: {0} Average time is {1} microsec.'.format(count_times, int(total_timeCount/count_times)/1000))