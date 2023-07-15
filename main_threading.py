import concurrent
import multiprocessing
import threading
from enum import Enum
import rx
from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops
from datetime import timedelta
from timeit import default_timer as timer

from clear_python import calculate_date_faster
from clear_python_mypy import calculate_date_mypy
from pandas_python import calculate_date_nice
from rx_python import calculate_date_rx


class ClearNiceRx(Enum):
    clear = 0
    nice = 1
    rx = 2
    mypy = 3


def split_list(the_list, chunk_size):
    result_list = []
    while the_list:
        result_list.append(the_list[:chunk_size])
        the_list = the_list[chunk_size:]
    return result_list


def final_time(start_time):
    end_time = timer()
    print('Total elapsed time is : {0}'.format(timedelta(seconds=end_time - start_time)))


def one_thread(count_times=1000, clear_or_nice_or_rx=ClearNiceRx.mypy):
    start_time = timer()
    total_timeCount = 0

    for i in range(count_times):
        if clear_or_nice_or_rx == ClearNiceRx.clear:
            # Clear
            result = calculate_date_faster()
        elif clear_or_nice_or_rx == ClearNiceRx.mypy:
            # Clear
            result = calculate_date_mypy()
        elif clear_or_nice_or_rx == ClearNiceRx.nice:
            # Nice
            result = calculate_date_nice(day_matrix='45;12;1;29;2;', years_count=200)
            # RX
        elif clear_or_nice_or_rx == ClearNiceRx.rx:
            result = calculate_date_rx(day_matrix='45;12;1;29;2;', years_count=200)

        total_timeCount = total_timeCount + result[1].microseconds
        end_time_mid = timer()
        print(result);
        print('Iteration: {0}. Time elapsed so far {1}'.format(i, timedelta(seconds=end_time_mid - start_time)))

    end_time = timer()

    print('Total execution times: {0} Average time is {1} microsec. Total elapsed time is : {2}'
          .format(count_times,
                  int(total_timeCount / count_times) / 1000,
                  timedelta(seconds=end_time - start_time)))


def rx_multi_threads(count_times=100000, clear_or_nice_or_rx=ClearNiceRx.clear):
    start_time = timer()

    # calculate cpu count, using which will create a ThreadPoolScheduler
    thread_count = multiprocessing.cpu_count()
    thread_pool_scheduler = ThreadPoolScheduler(thread_count)
    print("Cpu count is : {0}".format(thread_count))
    range_list = range(count_times)
    chunks = split_list(range_list, int(count_times / thread_count) + 1)
    i: int = 0
    subscriber = [None] * thread_count
    task_complete_counter = 0

    for cpu_c in chunks:
        subscriber[i] = rx.from_(cpu_c) \
            .pipe(
            ops.map(lambda a: calculate_date_faster(day_matrix='45;12;1;29;2;', years_count=200)),
            ops.subscribe_on(thread_pool_scheduler)
        ).subscribe(
            lambda s: final_time(start_time),  # print("Next date is: {0}; Elapsed time: {1}".format(s[0], s[1]))
            lambda error: print(error),
            on_next=final_time(start_time)
        )
        i = i + 1

    end_time = timer()
    print("everything is done {}".format(task_complete_counter))
    print('Total execution times: {0} Average time is {1} microsec. Total elapsed time is : {2}'
          .format(count_times,
                  0,
                  timedelta(seconds=end_time - start_time)))


def multi_threads(count_times=100000, clear_or_nice_or_rx=ClearNiceRx.clear):
    start_time = timer()

    # calculate cpu count, using which will create a ThreadPoolScheduler
    thread_count = multiprocessing.cpu_count()
    print("Cpu count is : {0}".format(thread_count))
    range_list = range(count_times)
    # chunks = split_list(range_list, int(count_times / thread_count) + 1)
    i: int = 0
    subscriber = [None] * thread_count
    task_complete_counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(calculate_date_faster, range_list)

    end_time = timer()
    print("everything is done {}".format(task_complete_counter))
    print('Total execution times: {0} Average time is {1} microsec. Total elapsed time is : {2}'
          .format(count_times,
                  0,
                  timedelta(seconds=end_time - start_time)))
