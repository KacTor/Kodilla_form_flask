'''import os
from flask import Flask, render_template, request

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/images/", methods=["GET", "POST"])
def form_view():
    if request.method == "POST":
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "File is uploaded"
    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)
'''
import requests
import csv
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

response = requests.get(
    'http://api.nbp.pl/api/exchangerates/tables/C?format=json')
data = response.json()
rates = data[0]['rates']

# emergency plan :3, another way, with csvwriter
'''with open('rates.csv', 'w', newline='', encoding='UTF8') as ratesfile:
    writer = csv.writer(ratesfile, delimiter=';')

    writer.writerow(rates[0].keys())
    for dict in rates:        
        writer.writerow(dict.values())
'''

with open('rates.csv', 'w', newline='', encoding='UTF8') as ratesfile:
    fieldname = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(ratesfile, fieldnames=fieldname, delimiter=';')

    writer.writeheader()

    for dict in rates:
        writer.writerow(dict)


@app.route("/exchange", methods=["GET", "POST"])
def exchange():
    currentCurrencies = []
    for dict in rates:
        currentCurrencies.append(dict['code'])

    if request.method == "POST":
        data = request.form
        currency = data.get('currency')
        amountOfCurrency = data.get('amountOfCurrency')

        for dict in rates:
            if currency == dict['code']:
                result = round(float(amountOfCurrency) * dict['bid'], 2)

        return render_template('result.html', result=result)

    return render_template('exchange.html', currentCurrencies=currentCurrencies)


if __name__ == "__main__":
    app.run(debug=True)
