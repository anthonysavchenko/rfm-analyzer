""" ETL solution to collect data from systems such as CRM and provide result of RFM-analysis """


import dates
import db
import poster
import yclients


def create_new_week(since_db_date, till_db_date, phone, customer_name, visits, payed):
    """
    Saves Week and Customer (if it is not saved yet) to the database.

    Parameters:
    since_db_date (str): start of the week in database string format.
    till_db_date (str): end of the week in database string format.
    phone (str): phone number of the customer (unique among customers).
    customer_name (str): name of the customer.
    visits (int): number of customer visits during the week.
    payed (float): payed amount by customer during the week.

    Return:
    None
    """
    customer_id = db.select_customer(phone)
    if customer_id == None:
        customer_id = db.insert_customer(customer_name, phone)
    db.insert_week(customer_id, since_db_date, till_db_date, visits, payed)


def load_visits(since_date, till_date, visits):
    """
    Loads information about visits (Customers and Weeks) to the database.

    Parameters:
    since_db_date (str): start of the period.
    till_db_date (str): end of the period.
    visits (tuple({
                "phone": str,
                "customerName": str,
                "visits": int,
                "payed": float
        })): Extracted and transformed information about visits.

    Return:
    None
    """
    since_db_date = db.get_db_formated_date(since_date)
    till_db_date = db.get_db_formated_date(till_date)
    db.delete_weeks(since_db_date)
    db.delete_customers_without_weeks()
    tuple(create_new_week(
        since_db_date,
        till_db_date,
        visit["phone"],
        visit["customerName"],
        visit["visits"],
        visit["payed"]
    ) for visit in visits if len(visit["phone"]) > 0 and visit["visits"] > 0)


def update_week_info_poster(since_date, till_date):
    """
    Poster API-related function.
    Runs extract, trasform and load operation sequence for some period.

    Parameters:
    since_date (date): start of the period.
    till_date (date): end of the period.

    Return:
    None
    """
    visits = poster.extract_and_transform_visits(since_date, till_date)
    load_visits(since_date, till_date, visits)


def update_week_info_yclients(since_date, till_date):
    """
    Yclients API-related function.
    Runs extract, trasform and load operation sequence for some period.

    Parameters:
    since_date (date): start of the period.
    till_date (date): end of the period.

    Return:
    None
    """
    visits = yclients.extract_and_transform_visits(since_date, till_date)
    load_visits(since_date, till_date, visits)


def update_weeks_info(api_method, since_date, till_date):
    """
    Runs extract, trasform and load operation sequence for some period.

    Parameters:
    api_method ((date, date) -> None): API-related function to execute operations.
    since_date (date): start of the period.
    till_date (date): end of the period.

    Return:
    None

    Other posible variants:

        def update_current_week_info(api_method):
            week = dates.get_week()
            api_method(*week)

        def update_all_weeks_info(api_method):
            tuple(api_method(*week) for week in dates.get_weeks())

        def update_weeks_info_since(api_method, since_date):
            tuple(api_method(*week) for week in dates.get_weeks(since_date = since_date))
    """
    tuple(api_method(*week) for week in dates.get_weeks(since_date, till_date))


# Main entry point with history of data loads:
#
# 08.07. First load Poster data.
# update_weeks_info(update_week_info_poster, dates.to_date(2021, 1, 4), dates.to_date(2021, 3, 14))
# update_weeks_info(update_week_info_poster, dates.to_date(2021, 3, 15), dates.to_date(2021, 5, 23))
# update_weeks_info(update_week_info_poster, dates.to_date(2021, 5, 24), dates.to_date(2021, 7, 8))
#
# 25.07. Update Poster data. New select report proposal.
# update_weeks_info(update_week_info_poster, dates.to_date(2021, 7, 8), dates.to_date(2021, 7, 25))
#
# 27.07. First load Yclients data. With throttling.
# update_weeks_info(update_week_info_yclients, dates.to_date(2021, 1, 4), dates.to_date(2021, 7, 27))
#
# 24.08. Load Yclients to new database again. Records API used.
# update_weeks_info(update_week_info_yclients, dates.to_date(2021, 1, 4), dates.to_date(2021, 8, 24))
#
# 13.10. Reload Poster data from the begining of the year.
update_weeks_info(
    update_week_info_poster,
    dates.to_date(2021, 1, 4),
    dates.to_date(2021, 10, 13))

print("done")
