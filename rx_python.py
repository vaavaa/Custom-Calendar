import rx
from rx import of, operators as op
from timeit import default_timer as timer
from datetime import timedelta, datetime
from rx.subject import Subject


def calculate_date_rx(date_string='09.07.2010 23:36',
                      day_matrix='0,45;12;1,2,6;3,6,14,18,21,24,28;1,2,3,4,5,6,7,8,9,10,11,12;',
                      years_count=1):
    start_time = timer()

    subject_test = Subject()
    subject_test.subscribe(
        lambda x: print(x.split(';'))
    )
    subject_test.subscribe(
        lambda x: print(x.split(','))
    )

    subject_test.on_next(day_matrix)
    end_time = timer()
    return None, timedelta(seconds=end_time - start_time)
