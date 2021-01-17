from clear_python import calculate_date_faster
from pandas_python import calculate_date_nice
from rx_python import calculate_date_rx

if __name__ == '__main__':
    count_times = 1
    total_timeCount = 0
    clear_or_nice_or_rx = 2  # 0-clear; 1-nice; 2-rx

    for i in range(count_times):
        if clear_or_nice_or_rx == 0:
            # Clear
            result = calculate_date_faster(day_matrix='45;12;1;29;2;', years_count=200)
        elif clear_or_nice_or_rx == 1:
            # Nice
            result = calculate_date_nice(day_matrix='45;12;1;29;2;', years_count=200)
        elif clear_or_nice_or_rx == 2:
            result = calculate_date_rx(years_count=2)

        total_timeCount = total_timeCount + result[1].microseconds

    print('Total execution times: {0} Average time is {1} microsec.'.format(count_times,
                                                                            int(total_timeCount / count_times) / 1000))
