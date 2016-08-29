import json
import calendar

from datetime import date, timedelta, datetime


def _get_yesterdays_date():
    current = date.today()
    current_time = datetime.utcnow()
    if current.day == 1:
        if current_time.hour <= 5:
            return date(current.year, current.month-1, (calendar.monthrange(current.year, current.month-1)[2])).strftime('%Y-%m-%d')
        else:
            return date(current.year, current.month-1, (calendar.monthrange(current.year, current.month-1)[1])).strftime('%Y-%m-%d')
    else:
        if current_time.hour <= 5:
            return date(current.year, current.month, current.day-2).strftime('%Y-%m-%d')
        else:
            return date(current.year, current.month, current.day-1).strftime('%Y-%m-%d')

def _get_last_month():
    current = date.today()
    if current.day == 31:
        return date(current.year, current.month-1, (calendar.monthrange(current.year, current.month-1)[1])).strftime('%Y-%m')
    else:
        return date(current.year, current.month-1, current.day).strftime('%Y-%m')

def _format_json(dictionary):
    return json.dumps(dictionary, indent=4, sort_keys=True)