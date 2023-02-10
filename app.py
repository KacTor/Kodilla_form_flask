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

from pprint import pprint
import requests
import csv


response = requests.get(
    'http://api.nbp.pl/api/exchangerates/tables/C?format=json')
data = response.json()
rates = data[0]['rates']

# porownanie 2 dict
print(rates[0])
print(rates[1])
print(rates[3])
print(rates[4])


with open('rates.csv', 'w', newline='') as ratesfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(ratesfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()
    writer.writerow(rates[3])
    writer.writerow(rates[4])
