import dates
import db
import poster
import yclients


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


def updateWeekInfoPoster(sinceDate, tillDate):
    apiSince = poster.getApiDateFormat(sinceDate)
    apiTill = poster.getApiDateFormat(tillDate)
    dbSince = db.getDbDateFormat(sinceDate)
    dbTill = db.getDbDateFormat(tillDate)
    visits = poster.extractAndTransformVisits(apiSince, apiTill)
    tuple(loadVisit(
        dbSince,
        dbTill,
        phone = visit["phone"],
        customerName = visit["customerName"],
        visits = visit["visits"],
        payed = visit["payed"]
    ) for visit in visits)


def updateWeekInfoYclients(sinceDate, tillDate):
    apiSince = yclients.getApiDateFormat(sinceDate)
    apiTill = yclients.getApiDateFormat(tillDate)
    dbSince = db.getDbDateFormat(sinceDate)
    dbTill = db.getDbDateFormat(tillDate)
    visits = yclients.extractAndTransformVisits(apiSince, apiTill)
    tuple(loadVisit(
        dbSince,
        dbTill,
        phone = visit["phone"],
        customerName = visit["customerName"],
        visits = visit["visits"],
        payed = visit["payed"]
    ) for visit in visits)


def updateCurrentWeekInfo(updateMethod):
    week = dates.getWeek()
    updateMethod(*week)


def updateWeeksInfoAll(updateMethod):
    tuple(updateMethod(*week) for week in dates.getWeeks())


def updateWeeksInfoSince(updateMethod, sinceDate):
    tuple(updateMethod(*week) for week in dates.getWeeks(sinceDate = sinceDate))


def updateWeeksInfoSinceTill(updateMethod, sinceDate, tillDate):
    tuple(updateMethod(*week) for week in dates.getWeeks(sinceDate, tillDate))

#updateWeeksInfoSinceTill(updateWeekInfoPoster, dates.toDate(2021, 1, 4), dates.toDate(2021, 3, 14))
#updateWeeksInfoSinceTill(updateWeekInfoPoster, dates.toDate(2021, 3, 15), dates.toDate(2021, 5, 23))
#updateWeeksInfoSinceTill(updateWeekInfoPoster, dates.toDate(2021, 5, 24), dates.toDate(2021, 7, 8))

#updateWeeksInfoSinceTill(updateWeekInfoPoster, dates.toDate(2021, 7, 8), dates.toDate(2021, 7, 25))

updateWeeksInfoSinceTill(updateWeekInfoYclients, dates.toDate(2021, 1, 4), dates.toDate(2021, 7, 27))
print("done")
