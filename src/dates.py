from config import firstMonday as configFirstMonday
from datetime import date, timedelta


def toDate(year, month, day):
    return date(year, month, day)


def getFirstMonday():
    year, month, day = configFirstMonday
    return date(year, month, day)


def getWeekNumber(targetDate):
    firstMonday = getFirstMonday()
    if targetDate < firstMonday:
        return 0
    delta = targetDate - firstMonday + timedelta(days = 1)
    weeksCount = delta.days // 7
    return weeksCount + 1 if delta.days % 7 > 0 else weeksCount


def getWeek(targetDate = date.today()):
    firstMondayDate = getFirstMonday()
    if targetDate < firstMondayDate:
        return ()
    weekNumber = getWeekNumber(targetDate)
    if (weekNumber == 0):
        return ()
    sinceDate = firstMondayDate + timedelta(days = (weekNumber - 1) * 7)
    tillDate = sinceDate + timedelta(days = 6)
    return (sinceDate, tillDate)


def getWeeks(sinceDate = getFirstMonday(), tillDate = date.today()):
    sinceWeekNumber = getWeekNumber(sinceDate)
    tillWeekNumber = getWeekNumber(tillDate)
    if sinceWeekNumber == 0 or tillWeekNumber == 0 or tillWeekNumber < sinceWeekNumber:
        return ()
    weeksCount = tillWeekNumber - sinceWeekNumber + 1
    firstWeek = getWeek(sinceDate)
    if firstWeek.count == 0:
        return ()
    firstWeekMonday, *_ = firstWeek
    mondays = (firstWeekMonday + timedelta(days = w * 7) for w in [*range(weeksCount)])
    return tuple((monday, monday + timedelta(days = 6)) for monday in mondays)
