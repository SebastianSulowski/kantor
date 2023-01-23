import requests
from flask import Flask, render_template, request

app = Flask(__name__)

url = f'http://api.nbp.pl/api/exchangerates/tables/C?format=json'
response = requests.get(url)
data = response.json()

result = {}

for item in data[0]['rates']:
    result[item["code"]] = item


@app.route('/currency', methods=['GET', 'POST'])
def currency():
    if request.method == 'POST':
        # Pobieranie z formularza

        _result = result
        currency_from = request.form.get('currency_from')
        currency_to = request.form.get('currency_to')
        amount = float(request.form.get('amount'))

        # Pobieranie kursu z NBP

        exchange_rate = data[0]['rates'][currency_to]

        # Obliczanie kosztu wymiany
        cost = exchange_rate * amount

        return render_template('currency_result.html', cost=cost)
    return render_template('currency.html')

if __name__ == "__main__":
    app.run(debug=True)
