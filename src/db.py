import sqlite3
from config import dbPath


def getDbDateFormat(targetDate):
    return targetDate.strftime("%Y-%m-%d")


def select(command, *params):
    with sqlite3.connect(dbPath) as connection:
        cursor = connection.execute(command, params)
        fetch = cursor.fetchone()
        if fetch == None:
            return None
        result, = fetch
        return result


def insert(command, *params):
    with sqlite3.connect(dbPath) as connection:
        cursor = connection.execute(command, params)
        connection.commit()
        return cursor.lastrowid


def update(command, *params):
    with sqlite3.connect(dbPath) as connection:
        cursor = connection.execute(command, params)
        connection.commit()
        return cursor.rowcount


def selectCustomer(phone):
    return select("SELECT Id FROM Customers WHERE Phone = ?", phone)
    

def insertCustomer(name, phone):
    return insert("INSERT INTO Customers VALUES(?, ?, ?)", None, name, phone)


def selectWeek(customerId, since):
    return select("SELECT Id FROM Weeks WHERE CustomerId = ? AND Since = ?", customerId, since)


def insertWeek(customerId, since, till, visits, payed):
    return insert(
        "INSERT INTO Weeks VALUES(?, ?, ?, ?, ?, ?)",
        None,
        customerId,
        since,
        till,
        visits,
        payed
    )


def updateWeek(weekId, visits, payed):
    return update("UPDATE Weeks SET Visits = ?, Payed = ? WHERE Id = ?", visits, payed, weekId)
