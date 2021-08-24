""" Works with yclients API.

    Yclients: https://www.yclients.com/
    API description: https://yclients.docs.apiary.io/
    Used version: 2.0
"""


from config import yclients_company_id, yclients_bearer_token, yclients_user_token
from ratelimit import limits, sleep_and_retry
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


@sleep_and_retry
@limits(calls = 5, period = 1)
@limits(calls = 200, period = 60)
def requestVisits(sinceDate, tillDate, count, page):
    """
    Requests financial transactions list from the API.
    Endpoint: https://api.yclients.com/api/v1/transactions/{yclientsCompanyId}
    Runs with throttling because of API developer requirement. Limited to 200 calls per minute
    (60 seconds) or to 5 calls per second.

    Parameters:
    sinceDate (date): start of the period.
    tillDate (date): end of the period.
    count (int): transactions amount on the page. Max 50.
    page (int): page number in result list.

    Return:
    str: phone string without extra characters.
    """
    url = f"https://api.yclients.com/api/v1/records/{yclients_company_id}"
    headers = {
        "Authorization": f"Bearer {yclients_bearer_token}, User {yclients_user_token}",
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
    count = 50
    page = 1
    extracted = []
    while True:
        requested = requestVisits(sinceDate, tillDate, count, page)
        extracted += requested
        if len(requested) < count:
            break
        page += 1
    return extracted


def clearVisit(visit):
    phone = ""
    if "client" in visit and visit["client"] != None and "phone" in visit["client"]:
        phone = clearPhone(visit["client"]["phone"])
    customerName = ""
    if "client" in visit and visit["client"] != None and "name" in visit["client"]:
        customerName = visit["client"]["name"]
    payed = ()
    if "services" in visit and isinstance(visit["services"], list):
        payed = tuple(service["cost"] for service in visit["services"] if "cost" in service)
    return {
        "phone": phone,
        "customerName": customerName,
        "visits": 1,
        "payed": float(sum(payed)),
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

    
def extract_and_transform_visits(sinceDate, tillDate):
    apiSince = getApiDateFormat(sinceDate)
    apiTill = getApiDateFormat(tillDate)
    extracted = extractVisits(apiSince, apiTill)
    return transformVisits(extracted)
