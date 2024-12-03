import requests

##############################################
# API FUNCTIONALITY
##############################################
API_KEY = 'CPI98ICU61YJ90Z9'

def request_data(action, symbol):
    url = 'https://www.alphavantage.co/query?function='+ action +'&symbol='+ symbol +'&apikey=' + API_KEY
    r = requests.get(url)
    data = r.json()
    return data

def search_auto(keyword):
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+ keyword +'&apikey=' + API_KEY
    r = requests.get(url)
    data = r.json()
    data = clean_search_data(data)
    return data

# Data: json data of search automation suggestions
# clean and return only the symbols and names
def clean_search_data(data):
    # Initialize an empty list to store the extracted names and symbols
    extracted_data = []

    # Loop through the 'bestMatches' list and extract 'symbol' and 'name' fields
    for item in data.get('bestMatches', []):
        symbol = item.get('1. symbol', 'N/A')  # Get the symbol, or 'N/A' if not present
        name = item.get('2. name', 'N/A')      # Get the name, or 'N/A' if not present
        extracted_data.append({'symbol': symbol, 'name': name})
    
    return extracted_data