from io import StringIO
from timeit import default_timer as timer
from datetime import timedelta
import pandas as pd


def calculate_date_nice(date_string='09.07.2010 23:36',
                        day_matrix='0,45;12;1,2,6;3,6,14,18,21,24,28;1,2,3,4,5,6,7,8,9,10,11,12;',
                        # '0,45;0,4,8,12,17,22;2,6;1,2,3,4,5,11,18,24;1,2,3,9,11;',
                        years_count=0):
    start = timer()
    df = pd.read_csv(StringIO(day_matrix),
                     header=None,
                     usecols=[0, 1, 2, 3, 4], names=['minutes', 'hours', 'weekdays', 'days', 'month'],
                     sep=';',
                     converters={i: str for i in range(5)}).transpose()
    minutes = pd.concat([df.iloc[0].str.split(',', expand=True)], axis=0)
    hours = pd.concat([df.iloc[1].str.split(',', expand=True)], axis=1)
    weekdays = pd.concat([df.iloc[2].str.split(',', expand=True)], axis=1)
    days = pd.concat([df.iloc[3].str.split(',', expand=True)], axis=1)
    month = pd.concat([df.iloc[4].str.split(',', expand=True)], axis=1)

    end = timer()
    print(timedelta(seconds=end - start))
