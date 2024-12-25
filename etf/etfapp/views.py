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

    
    data = request_data(symbol)
    dataframe_to_hyper(data, 'table', "data.hyper")

    context = {'symbol':symbol }
    return render(request, 'result.html', context)

def live_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('query', '')  # Get the query string from the request
        if search_query:
            
            data = search_auto(search_query)

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
    