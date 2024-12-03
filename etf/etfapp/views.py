from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from etfapp.api_func import *
import json
from plotly.io import to_html


# Create your views here.

def index(request):
    return render(request, 'index.html')

def result(request, symbol):
    symbol = extract_symbol(symbol)

    #### Uncomment to test with real api
    #monthly_data = request_data("TIME_SERIES_MONTHLY_ADJUSTED", symbol)
    #monthly_data = monthly_data['Monthly Adjusted Time Series']
    #cleaned_monthly_data = clean_monthly_data(monthly_data)

    # Loads Temporary file
    with open('C:/Users/tjwkd/Documents/etf/etf/etfapp/temp.json') as file:
        monthly_data = json.load(file)
        monthly_data = monthly_data['Monthly Adjusted Time Series']
        cleaned_monthly_data = clean_monthly_data(monthly_data)

    df = data_to_df(cleaned_monthly_data)
    fig_price = px.line(df, x="date", y="price", title="Date vs Price", labels={"Date": "Date", "Price": "Price"})
    fig_dividend = px.line(df, x="date", y="dividend", title="Date vs Dividend", labels={"Date": "Date", "Dividend": "Dividend"})
    fig_dividend_rate = px.line(df, x="date", y="dividend_rate", title="Date vs Dividend Rate", labels={"Date": "Date", "Dividend Rate": "Dividend Rate"})

    fig_price_html = to_html(fig_price, full_html=False)
    fig_dividend_html = to_html(fig_dividend, full_html=False)
    fig_dividend_rate_html = to_html(fig_dividend_rate, full_html=False)

    context = {'symbol':symbol, 
               'price_plot':fig_price_html, 
               'dividend_plot':fig_dividend_html,
               'dividend_rate_plot':fig_dividend_rate_html}
    return render(request, 'result.html', context)

def live_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '')  # Get the query string from the request
        if search_query:
            #data = search_auto(search_query)
            ###########
            # temporarily put sample data because of api daily limit
            ##########
            #"""
            
            data = [
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'},
                        {'symbol': 'IBM', 'name': 'International Business Machines Corporation'}
                    ]
            #"""

            
            # Filter the mock data based on the query
            filtered_data = [item for item in data if search_query.lower() in item['name'].lower() or search_query.upper() in item['symbol']]
        else:
            filtered_data = []

        # Return a JsonResponse with the filtered data
        return JsonResponse({'results': filtered_data})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



# {% url 'result' 'JEPI' %}
# Helper functino to extract symbol from url
def extract_symbol(str):
    str = str[17:]
    str = str[:-4]
    return str
    