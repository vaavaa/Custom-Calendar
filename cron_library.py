# By Nissanov Kairat
from datetime import datetime
import pytz
from croniter import croniter


def get_next_run_date(base, params):
    minutes, hour, weekdays, monthdays, months = params.rstrip(';').split(';')
    weekdays = ','.join([str(int(week_day) - 1) for week_day in weekdays.split(',')])

    schedule = f'{minutes} {hour} {monthdays} {months} {weekdays}'
    return croniter(schedule, base, day_or=False).get_next(datetime)


def main(base, params):
    tz = pytz.timezone('Asia/Almaty')
    date = datetime.strptime(base, '%d.%m.%Y %H:%M')
    user_date = tz.localize(date)
    utc_date = user_date.astimezone(pytz.utc)

    nextdate = get_next_run_date(utc_date, params)
    user_nextdate = tz.localize(nextdate.replace(tzinfo=None))

    return user_nextdate.strftime('%d-%m-%Y %H:%M')
