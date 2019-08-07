import os
import requests
from datetime import date

USERNAME = os.environ['m_username']
PASSWORD = os.environ['m_password']

COLUMNS = ['id', 'name', 'description', 'moment', 'sum', 'counterparty_uuid']


def get_orders():
    today = date.today()
    cur_date = '{}-{}-{} 00:00:00'.format(today.year, today.month, today.day)
    url = 'https://online.moysklad.ru/api/remap/1.1/entity/customerorder?filter=moment>' + cur_date

    r = requests.get(url, auth=(USERNAME, PASSWORD))
    rows = r.json()['rows']

    res = []
    for row in rows:
        id = row['id']
        name = row['name']
        description = ''
        moment = row['moment']
        sum = row['sum']
        counterparty_uuid = row['agent']['meta']['href'].split('/')[-1]

        values = [id, name, description, moment, sum, counterparty_uuid]

        res.append(dict(zip(COLUMNS, values)))

    return res