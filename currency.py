import requests
import pandas as pd


import requests

class Currency:
    def __init__(self, api_key=None):
        # Assuming your API key is stored in 'api.key'
        self.api_key = api_key
        self.url = f'http://api.exchangeratesapi.io/v1/latest?access_key={self.api_key}'

    def fetch_rates(self):
        '''
        Fetches the latest currency exchange rates from the API.

        Returns:
        - A dictionary containing the currency exchange rates.
        '''
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error: {response.status_code}')
            return None

    def convert_to_currency(self, currency_code):
        '''
        Converts all currencies to the specified currency.

        Args:
        - currency_code: The currency code to convert to (e.g., 'USD', 'EUR', 'MXN', etc.)

        Returns:
        - A dictionary containing the converted currency exchange rates.
        '''
        data = self.fetch_rates()
        if data:
            rates = data['rates']
            target_rate = rates.get(currency_code, None)  # Get the rate for the target currency

            if target_rate is None:
                print(f"Rate for {currency_code} not found.")
                return None

            # Convert all currencies to the specified currency
            converted_rates = {currency: rate / target_rate for currency, rate in rates.items()}
            # format the output similar to the original API structure
            data['rates'] = converted_rates
            data['base'] = currency_code  # update the base currency to the specified currency
            return data
        else:
            print("Failed to fetch rates.")
            return None
        
    def one_cent_of_every_person(self, dataframe, currency_code):
        '''
        Calculates how much money you will have if every person in the population gives you 1 cent in their currency and you convert it to Mexican Pesos (MXN).

        Args:
        - dataframe: A pandas DataFrame containing the population data and currency information.

        Returns:
        - The total population in Mexican Pesos (MXN).
        '''
        rates_data = self.convert_to_currency(currency_code)
        if rates_data is None:
            return f"Failed to convert currencies to {currency_code}. Check that you entered a valid API key."
        
        total_base_currency = 0
        rates = rates_data['rates']
        for index, row in dataframe.iterrows():
            currency = row['Currency']
            population = row['Population']
            rate_to_base_currency = rates.get(currency, 0)
            total_currency = 0.01 * population
            total_base_currency += total_currency / rate_to_base_currency

        return round(total_base_currency, 2)
