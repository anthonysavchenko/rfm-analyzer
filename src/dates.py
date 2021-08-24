from config import first_monday as config_first_monday
from datetime import date, timedelta


def to_date(year, month, day):
    return date(year, month, day)


def get_first_monday():
    year, month, day = config_first_monday
    return date(year, month, day)


def get_week_number(target_date):
    """
    Returns number of week (starting from first monday week) which includes target_date.

    Parameters:
    targer_date (date): target date.

    Return:
    int: Non-zero week number. Or 0 in case of target_date is earler than first monday.
    """
    first_monday_date = get_first_monday()
    if target_date < first_monday_date:
        return 0
    delta = target_date - first_monday_date + timedelta(days = 1)
    week_number = delta.days // 7
    return week_number + 1 if delta.days % 7 > 0 else week_number


def get_weeks(since_date = get_first_monday(), till_date = date.today()):
    """
    Returns sequence of weeks whick include since_date and till_date. Each week is
    returned in form of monday date and sunday date, exept for current week - today is not
    included, so current week is returned in form of monday date and yesterday date.

    Parameters:
    since_date (date): start of the period.
    till_date (date): end of the period.

    Return:
    tuple((date, date)): weeks tuple. Empty tuple in case of dates are earler than first monday or
    in case of other incorrect values.
    """
    today_date = date.today()
    yesterday_date = today_date - timedelta(days = 1)
    till_date = yesterday_date if (till_date >= today_date) else till_date
    since_week_number = get_week_number(since_date)
    till_week_number = get_week_number(till_date)
    if since_week_number == 0 or till_week_number == 0 or till_week_number < since_week_number:
        return ()
    weeks_count = till_week_number - since_week_number + 1
    since_week_monday = get_first_monday() + timedelta(days = (since_week_number - 1) * 7)
    mondays = (since_week_monday + timedelta(days = w * 7) for w in [*range(weeks_count)])
    return tuple((
        monday,
        yesterday_date if monday + timedelta(days = 6) >= today_date else monday + timedelta(days = 6)
    ) for monday in mondays)
