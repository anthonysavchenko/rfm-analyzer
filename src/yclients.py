""" Works with yclients API.

    Yclients: https://www.yclients.com/
    API description: https://yclients.docs.apiary.io/
    Used version: 2.0
"""


from config import yclientsCompanyId, yclientsBearerToken, yclientsUserToken
import requests


def getApiDateFormat(targetDate):
    """
    Returns date as string in format used by the API.

    Parameters:
    targetDate (date): target date.

    Return:
    str: date formatted as string.
    """
    return targetDate.strftime("%Y-%m-%d")


def clearPhone(phone):
    """
    Removes extra characters from the phone string used by the API.

    Parameters:
    phone (str): target phone string.

    Return:
    str: phone string without extra characters.
    """
    return phone.replace("+", "")


def requestVisits(sinceDate, tillDate, count, page):
    """
    Requests financial transactions list from the API.
    Endpoint: https://api.yclients.com/api/v1/transactions/{yclientsCompanyId}

    Parameters:
    sinceDate (date): start of the period.
    tillDate (date): end of the period.
    count (int): transactions amount on the page. Max 50.
    page (int): page number in result list.

    Return:
    str: phone string without extra characters.
    """
    url = f"https://api.yclients.com/api/v1/transactions/{yclientsCompanyId}"
    headers = {
        "Authorization": f"Bearer {yclientsBearerToken}, User {yclientsUserToken}",
        "Accept": "application/vnd.yclients.v2+json",
        "Content-Type": "application/json"
    }
    params = {
        "start_date": sinceDate,
        "end_date": tillDate,
        "page": page,
        "count": count
    }
    response = requests.get(url, headers = headers, params = params)
    return tuple(response.json()["data"])


def extractVisits(sinceDate, tillDate):
    count = 2
    page = 1
    extracted = []
    while len(extracted) == 0 or len(requested) == count:
        requested = requestVisits(sinceDate, tillDate, count, page)
        extracted += requested
        page += 1
    return extracted


def clearVisit(visit):
    return {
        "phone": clearPhone(visit["client"]["phone"]),
        "customerName": visit["client"]["name"],
        "visits": 1,
        "payed": float(visit["amount"])
    }


def groupVisits(visits):
    grouped = []
    for visit in visits:
        if next((False for t in grouped if t["phone"] == visit["phone"]), True):
            sameCustomerVisits = tuple(v["payed"] for v in visits if v["phone"] == visit["phone"])
            grouped.append({
                "phone": visit["phone"],
                "customerName": visit["customerName"],
                "visits": len(sameCustomerVisits),
                "payed": sum(sameCustomerVisits)
            })
    return grouped


def transformVisits(visits):
    cleared = tuple(clearVisit(visit) for visit in visits)
    return groupVisits(cleared)

    
def extractAndTransformVisits(sinceDate, tillDate):
    extracted = extractVisits(sinceDate, tillDate)
    return transformVisits(extracted)
