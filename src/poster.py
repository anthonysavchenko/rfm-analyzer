from config import posterApiKey
from ratelimit import limits, sleep_and_retry
import requests


def getApiDateFormat(targetDate):
    return targetDate.strftime("%Y%m%d")


def clearPhone(phone):
    return phone.replace("+", "").replace("-", "").replace(" ", "")


@sleep_and_retry
@limits(calls = 15, period = 60)
def requestVisits(sinceDate, tillDate):
    url = "https://joinposter.com/api/dash.getAnalytics"
    params = {
        "token": posterApiKey,
        "dateFrom": sinceDate,
        "dateTo": tillDate,
        "type": "clients"
    }
    response = requests.get(url, params = params)
    return tuple(response.json()["response"])


def extractVisits(sinceDate, tillDate):
    return requestVisits(sinceDate, tillDate)


def clearVisit(visit):
    return {
        "phone": clearPhone(visit["phone"])
            if "phone" in visit
            else "",
        "customerName": visit["firstname"] + " " + visit["lastname"]
            if "firstname" in visit and "lastname" in visit
            else "",
        "visits": visit["clients"]
            if "clients" in visit
            else 0,
        "payed": float(visit["sum"]) / 100
            if "sum" in visit
            else 0
    }


def transformVisits(visits):
    return tuple(clearVisit(visit) for visit in visits)


def extractAndTransformVisits(sinceDate, tillDate):
    extracted = extractVisits(sinceDate, tillDate)
    return transformVisits(extracted)
