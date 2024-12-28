from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from etfapp.api_func import *
from etfapp.tableau import *


# Create your views here.

def index(request):
    return render(request, 'index.html')

def result(request, symbol):
    symbol = extract_symbol(symbol)

    data = request_data(symbol)
    dataframe_to_hyper(data, 'table', "data.hyper")

    future = predict(symbol)
    future = [float(value) for value in future]

    context = {'symbol':symbol,
               'prediction': future }
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
    
def predict(symbol):
    train_data = prepare_train_data(symbol)
    X_train, X_test, y_train, y_test = prepare_train_test_data(train_data)
    model = configure_model(X_train, y_train)

    to_be_predicted = prepare_train_data(symbol)
    future_dividends = predict_dividends(to_be_predicted, sequence_length, num_predictions, model)

    return future_dividends
