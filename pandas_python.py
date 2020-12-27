from timeit import default_timer as timer
from datetime import timedelta

def calculate_date_nice():
    start = timer()

    end = timer()
    print(timedelta(seconds=end - start))
