""" Service functions to works with yclients API.

    Yclients: https://www.yclients.com/
    API description: https://yclients.docs.apiary.io/
    Used version: 2.0
"""


from datetime import date, datetime

from ratelimit import limits, sleep_and_retry
from requests import get as send_get_request

from rfm_analyzer.apps.yclients.models import Config


def _get_api_formated_date(target_date: date) -> str:
    """
    Returns date as string in format used by the API.
    """
    return target_date.strftime("%Y-%m-%d")


@sleep_and_retry
@limits(calls=5, period=1)
@limits(calls=200, period=60)
def _request_visits(since: date, till: date, config: Config, count: int, page: int):
    """
    Requests financial transactions list from the API.
    Endpoint: https://api.yclients.com/api/v1/transactions/{yclientsCompanyId}
    Runs with throttling because of API developer requirement. Limited
    to 200 calls per minute (60 seconds) or to 5 calls per second.
    """
    url = f"https://api.yclients.com/api/v1/records/{config.company_id}"
    headers = {
        "Authorization": f"Bearer {config.bearer_token}, User {config.user_token}",
        "Accept": "application/vnd.yclients.v2+json",
        "Content-Type": "application/json"
    }
    params = {
        "start_date": _get_api_formated_date(since),
        "end_date": _get_api_formated_date(till),
        "page": page,
        "count": count
    }
    response = send_get_request(url, headers=headers, params=params)
    return tuple(response.json()["data"])


def _extract_visits(since: date, till: date, config: Config):
    count = 50
    page = 1
    extracted = []
    while True:
        requested = _request_visits(since, till, config, count, page)
        extracted += requested
        if len(requested) < count:
            break
        page += 1
    return extracted


def _clear_phone(phone):
    """
    Removes extra characters from the phone string used by the API.
    """
    return phone.replace("+", "")


def _clear_visit(visit):
    phone = ""
    if "client" in visit and visit["client"] != None and "phone" in visit["client"]:
        phone = _clear_phone(visit["client"]["phone"])
    customer_name = ""
    if "client" in visit and visit["client"] != None and "name" in visit["client"]:
        customer_name = visit["client"]["name"]
    payed = ()
    if "services" in visit and isinstance(visit["services"], list):
        payed = tuple(service["cost"]
                      for service in visit["services"] if "cost" in service)
    return {
        "phone": phone,
        "customer_name": customer_name,
        "visits": 1,
        "payed": float(sum(payed)),
    }


def _group_visits(visits):
    grouped = []
    for visit in visits:
        if next((False for t in grouped if t["phone"] == visit["phone"]), True):
            same_customer_visits = tuple(
                v["payed"] for v in visits if v["phone"] == visit["phone"])
            grouped.append({
                "phone": visit["phone"],
                "customer_name": visit["customer_name"],
                "visits": len(same_customer_visits),
                "payed": sum(same_customer_visits)
            })
    return grouped


def _transform_visits(visits):
    cleared = tuple(_clear_visit(visit) for visit in visits)
    return _group_visits(cleared)


def extract_and_transform_visits(since: date, till: date, config: Config):
    extracted = _extract_visits(since, till, config)
    return _transform_visits(extracted)


def get_last_update(user_id: int) -> datetime | None:
    config = Config.objects.filter(pk=user_id).first()
    return config.last_update if config is not None else None


def set_last_update(user_id: int, now: datetime) -> None:
    Config.objects.update_or_create(pk=user_id, defaults={'last_update': now})
