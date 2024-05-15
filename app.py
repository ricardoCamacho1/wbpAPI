import streamlit as st
import pandas as pd 

from wpopulation import WorldBankDataPopulation
from currency import Currency

currency_codes = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNY', 'CNH', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LTL', 'LVL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD', 'STD', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMK', 'ZMW', 'ZWL']

st.title('Ventagium Assignment')

st.header('World Bank Data Population')

st.sidebar.subheader('API KEY')
api_key = st.sidebar.text_input('Enter your API Key:')
st.sidebar.write('If you do not have an API Key, you can get one from [ExchangeRate-API](https://exchangeratesapi.io/).')


ncountries = st.text_input(
                'Number of Countries', 
                value=5,
            )

year = st.text_input(
                'Year', 
                value=2020,
            )

# Pipeline 1 - World Bank Data Population
wb_data = WorldBankDataPopulation()
result = wb_data.top_countries_by_population(num_countries=int(ncountries), year=year)

st.dataframe(result)

st.download_button(
   "Download CSV",
   result.to_csv(index=False),
   f"top{ncountries}countries.csv",
   "text/csv",
   key='download-csv'
)

st.header('Currency Conversion')

# Initialize session state for DataFrame if not already present
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()

def load_example_data():
    reset_data()
    st.session_state.df = pd.read_csv('data/currency_example.csv')

def add_data(country, population, currency):
    new_data = {
        'Country': [country],
        'Population': [population],
        'Currency': [currency]
    }
    new_df = pd.DataFrame(new_data)
    st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)

def reset_data():
    st.session_state.df = pd.DataFrame()

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Example Data"):
        load_example_data()

with col2:
    country = st.text_input("Country", key="country")
    population = st.text_input("Population", key="population")
    currency = st.text_input("Currency", key="currency")
    if st.button("Add Data"):
        add_data(country, int(population), currency)
        st.success("Data added successfully!")

with col3:
    uploaded_file = st.file_uploader("Upload CSV", type="csv", key="file_uploader")
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
    st.write('Delete file after uploading to continue adding data.')


# Button to reset DataFrame
if st.button("Reset Data"):
    reset_data()

st.dataframe(st.session_state.df)

conv_currency = st.selectbox(
    'Currency:', currency_codes,
    index=None,
    placeholder="Select desired Currency...",
)

# Example usage
currency_converter = Currency(api_key=api_key)
result = currency_converter.one_cent_of_every_person(st.session_state.df,conv_currency)
st.write(f"If every person in the population gives you 1 cent in their currency and you convert it to {conv_currency}, you will have:")
st.write(f"TOTAL: {result} {conv_currency}")


