from os import getenv
from datetime import date, datetime, timedelta


def get_first_monday():
    """
    Gets beginning of the first supported week
    """
    first_monday_str = getenv('FIRST_MONDAY')
    first_monday_datetime = datetime.strptime(first_monday_str, "%Y-%m-%d")
    return first_monday_datetime.date()


def get_week_number(target_date):
    """
    Returns number of week the target_date.

    Return:
    int: Non-zero week number. Or 0 in case of target_date is earler
        than first monday.
    """
    first_monday = get_first_monday()
    if target_date < first_monday:
        return 0
    delta = target_date - first_monday + timedelta(days=1)
    week_number = delta.days // 7
    return week_number + 1 if delta.days % 7 > 0 else week_number


def get_weeks(since=get_first_monday(), till=date.today()):
    """
    Returns sequence of weeks which includes since_date and till_date.
    Each week is returned in form of monday date and sunday date, exept
    for current week - today is not included, so current week is
    returned in form of monday date and yesterday date.

    Return:
    tuple((date, date)): weeks tuple. Empty tuple in case of dates are
    earler than first monday or in case of other incorrect values.
    """
    today = date.today()
    yesterday = today - timedelta(days=1)
    till = yesterday if (till >= today) else till
    since_week_number = get_week_number(since)
    till_week_number = get_week_number(till)
    if since_week_number == 0 or till_week_number == 0 or \
            till_week_number < since_week_number:
        return ()
    weeks_count = till_week_number - since_week_number + 1
    since_week_monday = get_first_monday() + \
        timedelta(days=(since_week_number - 1) * 7)
    mondays = (since_week_monday + timedelta(days=w * 7)
               for w in [*range(weeks_count)])
    return tuple((
        monday,
        yesterday
        if monday + timedelta(days=6) >= today
        else monday + timedelta(days=6)
    ) for monday in mondays)
