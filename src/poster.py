from config import posterApiKey
import requests


def getApiDateFormat(targetDate):
    return targetDate.strftime("%Y%m%d")


def clearPhone(phone):
    return phone.replace("+", "").replace("-", "").replace(" ", "")


def extractVisits(sinceDate, tillDate):
    url = "https://joinposter.com/api/dash.getAnalytics"
    params = {
        "token": posterApiKey,
        "dateFrom": sinceDate,
        "dateTo": tillDate,
        "type": "clients"
    }
    response = requests.get(url, params=params)
    return tuple(response.json()["response"])


def transformVisit(customerVisit):
    return {
        "phone": clearPhone(customerVisit["phone"]),
        "customerName": customerVisit["firstname"] + " " + customerVisit["lastname"],
        "visits": customerVisit["clients"],
        "payed": float(customerVisit["sum"]) / 100
    }

def getVisits(sinceDate, tillDate):
    return tuple(transformVisit(visit) for visit in extractVisits(sinceDate, tillDate))
