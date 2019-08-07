import os
import pyodbc

SERVER = os.environ['server']
DATABASE = os.environ['database']
USERNAME = os.environ['username']
PASSWORD = os.environ['password']
DRIVER = '{ODBC Driver 17 for SQL Server}'

connection_string = 'DRIVER={};SERVER={};PORT=1433;DATABASE={};UID={};PWD={}'.format(
    DRIVER, SERVER, DATABASE, USERNAME, PASSWORD)


def test_connection():
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()

            if str(row[0]) == '1':
                return True

            return False


def create_tables():
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            with open('create_tables.sql', 'r') as f:
                query = f.read()

            cursor.execute(query)
            cursor.commit()


def get_orders():
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Fedor.Orders")

            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            return results


def get_counterparties():
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Fedor.Counterparty")

            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            return results


def insert_counterparty(id, name):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            query = """INSERT INTO Fedor.Counterparty(counterparty_uuid, name)
            VALUES (?, ?)"""

            values = (id, name)
            cursor.execute(query, values)


def insert_order(id, name, description, moment, sum, counterparty_uuid):
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            query = """INSERT INTO Fedor.Orders(id, name, description, moment, sum, counterparty_uuid)
            VALUES (?, ?, ?, ?, ?, ?)"""

            cursor.execute(query, (id, name, description, moment, sum, counterparty_uuid))


def get_counterparties_id():
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT counterparty_uuid FROM Fedor.Counterparty")

            results = []
            for row in cursor.fetchall():
                results.append(row[0])

            return results


def get_orders_id():
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM Fedor.Orders")

            results = []
            for row in cursor.fetchall():
                results.append(row[0])

            return results
