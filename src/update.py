import dates
import db
import poster


def loadVisit(sinceDate, tillDate, phone, customerName, visits, payed):
    if len(phone) > 0:
        customerId = db.selectCustomer(phone)
        if customerId == None:
            customerId = db.insertCustomer(customerName, phone)
        weekId = db.selectWeek(customerId, sinceDate)
        if weekId == None:
            db.insertWeek(customerId, sinceDate, tillDate, visits, payed)
        else:
            db.updateWeek(weekId, visits, payed)


def updateWeekInfo(sinceDate, tillDate):
    apiSince = poster.getApiDateFormat(sinceDate)
    apiTill = poster.getApiDateFormat(tillDate)
    dbSince = db.getDbDateFormat(sinceDate)
    dbTill = db.getDbDateFormat(tillDate)
    visits = poster.getVisits(apiSince, apiTill)
    tuple(loadVisit(
        dbSince,
        dbTill,
        phone = visit["phone"],
        customerName = visit["customerName"],
        visits = visit["visits"],
        payed = visit["payed"]
    ) for visit in visits)


def updateCurrentWeekInfo():
    week = dates.getWeek()
    updateWeekInfo(*week)


def updateWeeksInfoAll():
    tuple(updateWeekInfo(*week) for week in dates.getWeeks())


def updateWeeksInfoSince(sinceDate):
    tuple(updateWeekInfo(*week) for week in dates.getWeeks(sinceDate = sinceDate))


def updateWeeksInfoSinceTill(sinceDate, tillDate):
    tuple(updateWeekInfo(*week) for week in dates.getWeeks(sinceDate, tillDate))

#updateWeeksInfoSinceTill(dates.toDate(2021, 1, 4), dates.toDate(2021, 3, 14))
#updateWeeksInfoSinceTill(dates.toDate(2021, 3, 15), dates.toDate(2021, 5, 23))
#updateWeeksInfoSinceTill(dates.toDate(2021, 5, 24), dates.toDate(2021, 7, 8))

updateWeeksInfoSinceTill(dates.toDate(2021, 7, 8), dates.toDate(2021, 7, 25))
print("done")
