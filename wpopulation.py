import requests
import pandas as pd

class WorldBankDataPopulation:
    def __init__(self):
        self.base_url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"

    def fetch_data(self, year, num_countries):
        per_page=1000 # number of records to fetch per page
        page = 1 # initialize the page number
        data_accumulated = pd.DataFrame() # initialize an empty DataFrame

        while len(data_accumulated) < num_countries: # fetch data until we have enough countries
            url = f"{self.base_url}?date={year}&per_page={per_page}&format=json&page={page}" # construct the URL
            response = requests.get(url) # make the HTTP request
            if response.status_code != 200:
                print(f'Error: {response.status_code}')
                return pd.DataFrame()  # return an empty DataFrame in case of an HTTP error

            data = response.json()
            if not data[1] :  # no more data available
                break

            batch_data = pd.DataFrame(data[1]) # convert the data to a DataFrame
            batch_data = batch_data[['country', 'value']] # extract the relevant columns
            batch_data['Country'] = batch_data['country'].apply(lambda x: x['value']) # extract the country name
            batch_data['ID'] = batch_data['country'].apply(lambda x: x['id']) # extract the country ID
            batch_data['Population'] = batch_data['value'] # extract the population value
            batch_data = batch_data[['Country', 'ID', 'Population']].dropna(subset=['Population']) # drop rows with missing population data
            batch_data['Population'] = batch_data['Population'].astype(int) # convert population to integer
            batch_data['Year'] = str(year) # add the year column
            data_accumulated = pd.concat([data_accumulated, batch_data]) # append the batch data to the accumulated data

            page += 1

        return data_accumulated

    def top_countries_by_population(self, num_countries=10, year=2020):
        data_accumulated = self.fetch_data(year, num_countries) # fetch the data
        if data_accumulated.empty:
            return pd.DataFrame()

        full_data = data_accumulated.sort_values(by='Population', ascending=False) # sort the data by population
        full_data = full_data.head(num_countries) # select the top N countries
        full_data.reset_index(drop=True, inplace=True) # reset the index
        return full_data