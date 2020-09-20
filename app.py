# app.py - a minimal flask api using flask_restful
from flask import Flask, request
from flask import jsonify
import sqlite3 as sql

app = Flask(__name__)

#API for get list and save a Invoice
@app.route('/invoice', methods=['POST', 'GET'])
def invoice():
    print(request)
    if request.method == 'POST':

        with sql.connect("database.db") as con:
            cur = con.cursor()
            data = request.get_json()
            invoice_number = data['invoice_number']
            total = data['total']
            currency = data['currency']
            invoice_date = data['invoice_date']
            due_date = data['due_date']
            vendor_name = data['vendor_name']
            remittance_address = data['remittance_address']
            status = data.get('status','pending')

            cur.execute("INSERT INTO invoice "
                        "(invoice_number,total,currency,invoice_date,due_date,vendor_name,remittance_address,status) "
                        "VALUES(?,?,?,?,?,?,?,?)",
                        (invoice_number, total, currency, invoice_date, due_date, vendor_name, remittance_address, status))

            con.commit()
        return {"message": "invoice submitted successfully"}
    else:
        result = []
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM invoice")
            invoices = cur.fetchall()
            for invoice in invoices:
                invoice_dict = {
                    "id": invoice[0],
                    "invoice_number": invoice[1],
                    "total": invoice[2],
                    "currency": invoice[3],
                    "invoice_date": invoice[4],
                    "due_date": invoice[5],
                    "vendor_name": invoice[6],
                    "remittance_address": invoice[7],
                    "status": invoice[8]
                }
                result.append(invoice_dict)

            app.logger.debug(invoices)

        return jsonify(result)


#API for get edit a Invoice
@app.route('/invoice/<id_invoice>', methods=['POST', 'GET'])
def edit_invoice(id_invoice):
    if request.method == 'POST':
        # app.logger.debug("ENTER TO EDIT")
        with sql.connect("database.db") as con:
            cur = con.cursor()
            data = request.get_json()
            status = data.get('status')
            cur.execute("UPDATE invoice SET status = '%s' WHERE id = %s" % (status, id_invoice))

        return {"message": "invoice edited successfully"}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
