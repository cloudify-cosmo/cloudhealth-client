import json
import calendar

from datetime import date, datetime


def _format_date(date_string, format):
    if format == "day":
        return date_string.strftime('%Y-%m-%d')
    elif format == "month":
        return date_string.strftime('%Y-%m')


def _get_yesterdays_date():
    """Get yesterday's date in the right format

    CloudHealth reports based on dates formatted in a specific way.
    This function is used by CLI to extract specific day from response.
    This function will always get you yesterdays date except if the time is
      before 6 AM (in this case the reports aren't done yet so you'll get
      the day before yesterday)
    When it's first day of the month it will return the last day of last month.
    """
    current = date.today()
    current_time = datetime.utcnow()
    if current.day == 1:
        if current_time.hour <= 6:
            return _format_date(date(current.year,
                                     current.month-1,
                                     (calendar.monthrange(
                                             current.year,
                                             current.month-1)[2])), "day")
        else:
            return _format_date(date(current.year,
                                     current.month-1,
                                     (calendar.monthrange(
                                             current.year,
                                             current.month-1)[1])), "day")
    else:
        if current_time.hour <= 6:
            return _format_date(date(current.year,
                                     current.month,
                                     current.day-2), "day")
        else:
            return _format_date(date(current.year,
                                     current.month,
                                     current.day-1), "day")


def _get_last_month():
    """Get last month's date in the right format

    CloudHealth reports based on dates formatted in a specific way.
    This function is used by CLI to extract specific day from response.
    This function will always get you last month's date.

    When it's first day of the month it will return the last day of last month.
    """
    current = date.today()
    return _format_date(date(
            current.year,
            current.month-1,
            (calendar.monthrange(current.year,
                                 current.month-1)[1])), "month")


def _format_json(dictionary):
    return json.dumps(dictionary, indent=4, sort_keys=True)
