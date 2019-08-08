import xlrd

from flask import Blueprint, render_template, redirect

import db
import moysklad

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    if db.test_connection():
        message = "База даних під'єднана"
    else:
        message = "Не вдалося встановити з'єднання з базою даних"

    orders = db.get_orders()
    counterparties = db.get_counterparties()

    return render_template('index.html', message=message, orders=orders, counterparties=counterparties)


@bp.route('/recreate')
def recreate():
    db.create_tables()

    return redirect("/", code=302)


@bp.route('/xlsx')
def xlsx():
    counterparties = db.get_counterparties_id()
    orders = db.get_orders_id()
    fails = []
    successfully_count = 0

    book = xlrd.open_workbook("AzureTables.xlsx")

    sheet = book.sheet_by_name("counterparty")
    for r in range(1, sheet.nrows):
        id = sheet.cell(r, 0).value
        name = sheet.cell(r, 1).value

        if id in counterparties:
            fails.append("Контрагент {}(id={}) вже існує".format(name, id))
            continue

        counterparties.append(id)
        db.insert_counterparty(id, name)
        successfully_count += 1

    sheet = book.sheet_by_name("orders")
    for r in range(1, sheet.nrows):
        id = sheet.cell(r, 0).value
        name = sheet.cell(r, 1).value
        description = sheet.cell(r, 2).value
        moment = sheet.cell(r, 3).value
        sum = sheet.cell(r, 4).value
        counterparty_uuid = sheet.cell(r, 5).value

        if id in orders:
            fails.append("Замовлення {}(id={}) вже існує".format(name, id))
            continue

        if not counterparty_uuid in counterparties:
            fails.append("Замовлення {}(id={}) містить невідомий контрагент {}".format(name, id, counterparty_uuid))
            continue

        db.insert_order(id, name, description, moment, sum, counterparty_uuid)
        successfully_count += 1

    message = "Успішно додано {} рядків".format(successfully_count)

    return render_template('result.html', message=message, fails=fails)


@bp.route('/moysklad_api')
def moysklad_api():
    new_orders = moysklad.get_orders()

    counterparties = db.get_counterparties_id()
    orders = db.get_orders_id()

    fails = []
    successfully_count = 0
    for o in new_orders:
        if o['id'] in orders:
            fails.append("Замовлення {}(id={}) вже існує".format(o['name'], o['id']))
            continue

        if not o['counterparty_uuid'] in counterparties:
            fails.append("Замовлення {}(id={}) містить невідомий контрагент {}".format(
                o['name'], o['id'], o['counterparty_uuid']))
            continue

        db.insert_order(o['id'], o['name'], o['description'], o['moment'], o['sum'], o['counterparty_uuid'])
        successfully_count += 1

    message = "Успішно додано {} рядків".format(successfully_count)

    return render_template('result.html', message=message, fails=fails)
