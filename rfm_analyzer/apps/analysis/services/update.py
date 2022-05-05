from django.db.models import Count
from django.utils import timezone

from rfm_analyzer.apps.analysis.models import Customer, Week
from rfm_analyzer.apps.yclients.services import \
    extract_and_transform_visits, set_last_update
from rfm_analyzer.apps.analysis.services.dates import get_weeks


def _create_new_week(since, till, phone, customer_name, visits, payed, user_id):
    """
    Saves Week and Customer (if it is not exists) to the database.
    """
    customer = Customer.objects.get_or_create(
        phone=phone,
        user_id=user_id,
        defaults={'customer_name': customer_name}
    )[0]
    Week.objects.create(
        customer_id=customer.pk,
        since=since,
        till=till,
        visits=visits,
        payed=payed
    )


def _delete_temporary_data(since, user_id):
    """
    Deletes previously saved data for the week to request it again.
    """
    Week.objects.filter(since=since, customer__user_id=user_id).delete()
    Customer.objects \
        .filter(user_id=user_id) \
        .annotate(week_count=Count('week')) \
        .filter(week_count=0) \
        .delete()


def _load_visits(since, till, user_id, visits):
    """
    Saves visits (Customers and Weeks) to the database.
    """
    _delete_temporary_data(since, user_id)
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
    visits = extract_and_transform_visits(since, till, config)
    _load_visits(since, till, config.user.id, visits)


def update(config):
    """
    Updates data for the user.
    """
    now = timezone.now()
    weeks = get_weeks() if config.last_update is None \
        else get_weeks(since=timezone.localdate(config.last_update))
    tuple(_update_one_week_data(*week, config) for week in weeks)
    set_last_update(config.user.id, now)
