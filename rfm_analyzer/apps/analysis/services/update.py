from django.db.models import Count

from rfm_analyzer.apps.analysis.models import Customer, Week
from rfm_analyzer.apps.yclients.services import extract_and_transform_visits \
    as yclients_extract_and_transform_visits

from .dates import get_weeks


def _create_new_week(since, till, phone, customer_name, visits, payed, user_id):
    """
    Saves Week and Customer (if it is not exists) to the database.
    """
    customer, = Customer.objects.get_or_create(
        phone=phone,
        defaults={'customer_name': customer_name, 'user_id': user_id}
    )
    Week.objects.create(
        customer_id=customer.pk,
        since=since,
        till=till,
        visits=visits,
        payed=payed
    )


def _delete_temporary_data(since):
    """
    Deletes previously saved data for the week to request it again.
    """
    Week.objects.filter(since=since).delete()
    Customer.objects \
        .annotate(week_count = Count('week')) \
        .filter(week_count=0) \
        .delete()


def _load_visits(since, till, user_id, visits):
    """
    Saves visits (Customers and Weeks) to the database.
    """
    _delete_temporary_data(since)
    tuple(_create_new_week(
        since,
        till,
        visit['phone'],
        visit['customer_name'],
        visit['visits'],
        visit['payed'],
        user_id
    ) for visit in visits if len(visit['phone']) > 0 and visit['visits'] > 0)


def _update_one_week_data(since, till, config):
    """
    Updates data for one week.
    """
    visits = yclients_extract_and_transform_visits(since, till, config)
    _load_visits(since, till, config.user.id, visits)


def update(config):
    """
    Updates data for the user.
    """
    tuple(_update_one_week_data(*week, config.user.id) \
        for week in get_weeks(since=config.last_update))
