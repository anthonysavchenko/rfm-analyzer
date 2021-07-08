from config import posterApiKey
import requests


def getApiDateFormat(targetDate):
    return targetDate.strftime("%Y%m%d")


def getCustomerVisits(sinceDate, tillDate):
    url = "https://joinposter.com/api/dash.getAnalytics"
    params = {
        "token": posterApiKey,
        "dateFrom": sinceDate,
        "dateTo": tillDate,
        "type": "clients"
    }
    response = requests.get(url, params=params)
    return tuple(response.json()["response"])
