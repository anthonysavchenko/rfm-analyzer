from config import posterApiKey
import requests


def getApiDateFormat(targetDate):
    return targetDate.strftime("%Y%m%d")


def clearPhone(phone):
    return phone.replace("+", "").replace("-", "").replace(" ", "")


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
        "phone": clearPhone(visit["phone"]),
        "customerName": visit["firstname"] + " " + visit["lastname"],
        "visits": visit["clients"],
        "payed": float(visit["sum"]) / 100
    }


def transformVisits(visits):
    return tuple(clearVisit(visit) for visit in visits)


def extractAndTransformVisits(sinceDate, tillDate):
    extracted = extractVisits(sinceDate, tillDate)
    return transformVisits(extracted)
