import requests

API_KEY = '6fce5ca7f3e13df5983d2d05'
URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'

def get_rates():
    response = requests.get(URL)
    data = response.json()


    if response.status_code != 200:
        print('Error al obtener las tasas de cambio')
        return None
    return data['conversion_rates']

def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency != 'USD':
        amount = amount / rates[from_currency]
    return amount * rates[to_currency]

def main():
    rates = get_rates()
    if rates:
        amount = float(input('Introduce la cantidad que quieres convertir: '))
        from_currency = input('Introduce la divisa desde la cual conviertes: ')
        to_currency = input('Introduce la divisa a la cual conviertes: ')

        result = convert_currency(amount, from_currency, to_currency, rates)
        print(f'{amount} {from_currency} es igual a {result:.2f} {to_currency}')
        print(rates[from_currency])

if __name__ == '__main__':
    main()