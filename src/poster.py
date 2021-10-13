from config import poster_api_key
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
        "token": poster_api_key,
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
        "visits": int(visit["clients"])
            if "clients" in visit
            else 0,
        "payed": float(visit["sum"]) / 100
            if "sum" in visit
            else 0
    }


def transformVisits(visits):
    return tuple(clearVisit(visit) for visit in visits)


def extract_and_transform_visits(since_date, till_date):
    apiSince = getApiDateFormat(since_date)
    apiTill = getApiDateFormat(till_date)
    extracted = extractVisits(apiSince, apiTill)
    return transformVisits(extracted)
