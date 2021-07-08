import dates
import db
import poster


def clearPhone(phone):
    return phone.replace("+", "").replace("-", "").replace(" ", "")


def updateWeekInfo(since, till):
    apiSince = poster.getApiDateFormat(since)
    apiTill = poster.getApiDateFormat(till)
    dbSince = db.getDbDateFormat(since)
    dbTill = db.getDbDateFormat(till)
    customerVisits = poster.getCustomerVisits(apiSince, apiTill)
    for customerVisit in customerVisits:
        phone = clearPhone(customerVisit["phone"])
        if len(phone) == 0:
            continue
        customerId = db.selectCustomer(phone)
        if customerId == None:
            customerName = customerVisit["firstname"] + " " + customerVisit["lastname"]
            customerId = db.insertCustomer(customerName, phone)
        weekId = db.selectWeek(customerId, dbSince)
        visits, = customerVisit["clients"],
        payed = float(customerVisit["sum"]) / 100
        if weekId == None:
            db.insertWeek(customerId, dbSince, dbTill, visits, payed)
        else:
            db.updateWeek(weekId, visits, payed)


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
updateWeeksInfoSinceTill(dates.toDate(2021, 5, 24), dates.toDate(2021, 7, 8))
print("done")
