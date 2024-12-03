import requests
import json
import plotly.express as px
import pandas as pd

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

def clean_monthly_data(data_dict):
    keys = data_dict.keys()
    result={"date":"", "dividend":0, "adjusted_close":0, "dividend_rate":0}
    results = []
    for key in keys:
        data = data_dict[key]
        if float(data["7. dividend amount"]) != 0:
            temp = result.copy()
            temp["date"] = key
            temp["dividend"] = float(data["7. dividend amount"])
            temp["adjusted_close"] = float(data["5. adjusted close"])
            temp["dividend_rate"] = float(data["7. dividend amount"])/float(data["5. adjusted close"])
            results.append(temp)
    return results

with open('C:/Users/tjwkd/Documents/etf/etf/etfapp/temp.json') as file:
        monthly_data = json.load(file)
        monthly_data = monthly_data['Monthly Adjusted Time Series']
        cleaned_monthly_data = clean_monthly_data(monthly_data)

def data_to_df(data_dict):
    df_dict = {
        "date": [],
        "price": [],
        "dividend": [],
        "dividend_rate": []
        }
    dates = []
    dividends = []
    price = []
    dividend_rates = []
    for data in cleaned_monthly_data:
        df_dict["date"].append(pd.to_datetime((data["date"])))
        df_dict["price"].append(data["adjusted_close"])
        df_dict["dividend"].append(data["dividend"])
        df_dict["dividend_rate"].append(data["dividend_rate"])

    df = pd.DataFrame(df_dict)
    return df

