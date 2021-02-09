import multiprocessing
import time
from enum import Enum
from threading import current_thread
import rx
from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops
from datetime import timedelta
from time import sleep
from timeit import default_timer as timer

from clear_python import calculate_date_faster
from pandas_python import calculate_date_nice
from rx_python import calculate_date_rx


class ClearNiceRx(Enum):
    clear = 0
    nice = 1
    rx = 2


def one_thread(count_times=100000, clear_or_nice_or_rx=ClearNiceRx.clear):
    start_time = timer()
    total_timeCount = 0

    for i in range(count_times):
        if clear_or_nice_or_rx == 0:
            # Clear
            result = calculate_date_faster(day_matrix='45;12;1;29;2;', years_count=200)
        elif clear_or_nice_or_rx == 1:
            # Nice
            result = calculate_date_nice(day_matrix='45;12;1;29;2;', years_count=200)
            # RX
        elif clear_or_nice_or_rx == 2:
            result = calculate_date_rx(day_matrix='45;12;1;29;2;', years_count=200)

        total_timeCount = total_timeCount + result[1].microseconds
        end_time_mid = timer()
        print('Iteration: {0}. Time elapsed so far {1}'.format(i, timedelta(seconds=end_time_mid - start_time)))

    end_time = timer()

    print('Total execution times: {0} Average time is {1} microsec. Total elapsed time is : {2}'
          .format(count_times,
                  int(total_timeCount / count_times) / 1000,
                  timedelta(seconds=end_time - start_time)))


def multi_threads(count_times=100000, clear_or_nice_or_rx=ClearNiceRx.clear):
    start_time = timer()
    total_timeCount = 0

    end_time = timer()

    # calculate cpu count, using which will create a ThreadPoolScheduler
    thread_count = multiprocessing.cpu_count()
    thread_pool_scheduler = ThreadPoolScheduler(thread_count)
    print("Cpu count is : {0}".format(thread_count))

    range_list = range(count_times)
    chunks = split_list(range_list,int(count_times/thread_count))

    for cpu_c in chunks:
        rx.from_(cpu_c) \
            .pipe(
            ops.map(lambda a: calculate_date_faster(day_matrix='45;12;1;29;2;', years_count=200)),
            ops.subscribe_on(thread_pool_scheduler)
        ) \
            .subscribe(
            lambda s: print(""),
            lambda error: print(error),
            lambda: print("Task {0} complete. Total done is {1}".format(cpu_c, total_timeCount)),
            lambda on_next: print("Total done is {1}".format(on_next, total_timeCount + 1))
        )


def split_list(the_list, chunk_size):
    result_list = []
    while the_list:
        result_list.append(the_list[:chunk_size])
        the_list = the_list[chunk_size:]
    return result_list

if __name__ == '__main__':
    multi_threads(count_times=10000)
