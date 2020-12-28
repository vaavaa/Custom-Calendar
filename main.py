import datetime

from clear_python import calculate_date_faster
from pandas_python import calculate_date_nice

if __name__ == '__main__':
    count_times = 1
    total_timeCount = 0
    clear_or_nice = False

    for i in range(count_times):
        if clear_or_nice:
            # Clear
            result = calculate_date_faster(day_matrix='45;12;1;29;2;', years_count=200)
        else:
            # Nice
            result = calculate_date_nice(day_matrix='45;12;1;29;2;', years_count=200)
        total_timeCount = total_timeCount + result[1].microseconds

    print('Total execution times: {0} Average time is {1} microsec.'.format(count_times, int(total_timeCount/count_times)/1000))