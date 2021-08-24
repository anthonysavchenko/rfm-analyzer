import sqlite3
from config import db_path


def get_db_formated_date(target_date):
    return target_date.strftime("%Y-%m-%d")


def select(command, *params):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(command, params)
        fetch = cursor.fetchone()
        if fetch == None:
            return None
        result, = fetch
        return result


def insert(command, *params):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(command, params)
        connection.commit()
        return cursor.lastrowid


def update(command, *params):
    with sqlite3.connect(db_path) as connection:
        cursor = connection.execute(command, params)
        connection.commit()
        return cursor.rowcount


def delete(command, *params):
    return update(command, *params)


def select_customer(phone):
    return select("SELECT Id FROM Customers WHERE Phone = ?", phone)
    

def insert_customer(name, phone):
    return insert("INSERT INTO Customers VALUES(?, ?, ?)", None, name, phone)


def insert_week(customer_id, since, till, visits, payed):
    return insert(
        "INSERT INTO Weeks VALUES(?, ?, ?, ?, ?, ?)",
        None,
        customer_id,
        since,
        till,
        visits,
        payed)


def delete_weeks(since_db_date):
    return delete("DELETE FROM Weeks WHERE Since = ?", since_db_date)


def delete_customers_without_weeks():
    return delete("DELETE FROM Customers WHERE Id IN "
        + "(SELECT c.Id FROM Customers AS c LEFT JOIN Weeks AS w "
            + "ON c.Id = w.CustomerId WHERE w.Id IS NULL)")
