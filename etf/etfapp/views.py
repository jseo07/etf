from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from etfapp.api_func import *
import json
# Create your views here.

def index(request):
    return render(request, 'index.html')

def result(request, symbol):
    symbol = extract_symbol(symbol)
    #monthly_data = request_data("TIME_SERIES_MONTHLY_ADJUSTED", symbol)
    with open('/Users/jangwonseo/Documents/Documents/Courses/etf/etf/etfapp/temp.json') as file:
        monthly_data = json.load(file)
        monthly_data = monthly_data['Monthly Adjusted Time Series']

    context = {'symbol':symbol, 'monthly_data':monthly_data}
    return render(request, 'result.html', context)

def live_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '')  # Get the query string from the request
        print(search_query)
        if search_query:
            #data = search_auto(search_query)
            ###########
            # temporarily put sample data because of api daily limit
            ##########
            #"""
            data = [
                        {'symbol': 'JEPI', 'name': 'JPMorgan Equity Premium Income ETF'},
                        {'symbol': 'JEPQ', 'name': 'JPMorgan Nasdaq Equity Premium Income ETF'},
                        {'symbol': 'JEP.FRK', 'name': 'SalMar ASA'},
                        {'symbol': 'JEPAX', 'name': 'JPMORGAN EQUITY PREMIUM INCOME FUND CLASS A'},
                        {'symbol': 'JEPCX', 'name': 'JPMORGAN EQUITY PREMIUM INCOME FUND CLASS C'},
                        {'symbol': 'JEPIX', 'name': 'JPMORGAN EQUITY PREMIUM INCOME FUND CLASS I'},
                        {'symbol': 'JEPMX', 'name': 'JPMORGAN U.S. RESEARCH EQUITY PLUS FUND CLASS R6'},
                        {'symbol': 'JEPRX', 'name': 'JPMORGAN EQUITY PREMIUM INCOME FUND CLASS R6'},
                        {'symbol': 'JEPSX', 'name': 'JPMORGAN EQUITY PREMIUM INCOME FUND CLASS R5'},
                        {'symbol': 'JEPG.LON', 'name': 'Global Equity Premium Income UCITS ETF'}
                    ]
            #"""
            
            # Filter the mock data based on the query
            filtered_data = [item for item in data if search_query.lower() in item['name'].lower() or search_query.upper() in item['symbol']]
        else:
            filtered_data = []

        # Return a JsonResponse with the filtered data
        print(filtered_data)
        return JsonResponse({'results': filtered_data})

    return JsonResponse({'error': 'Invalid request method'}, status=400)



# {% url 'result' 'JEPI' %}
# Helper functino to extract symbol from url
def extract_symbol(str):
    str = str[17:]
    str = str[:-4]
    return str