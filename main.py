import datetime

from clear_python import calculate_date_faster
from pandas_python import calculate_date_nice

if __name__ == '__main__':
    count_times = 1000
    total_timeCount = 0

    for i in range(count_times):
        result =calculate_date_faster()
        #result = calculate_date_nice()
        total_timeCount = total_timeCount + result[1].microseconds

    print('Total execution times: {0} Average time is {1} microsec.'.format(count_times, int(total_timeCount/count_times)/1000))