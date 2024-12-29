import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from tensorflow.keras.optimizers import Adam
import yfinance as yf
import warnings

warnings.filterwarnings('ignore', category = UserWarning)

scaler = MinMaxScaler()
sequence_length = 12
num_predictions = 5

def request_data(symbol):
    dat = yf.Ticker(symbol)
    dat= dat.history(period="max", interval="1d")
    dat.reset_index(inplace=True)
    dat['Date'] = pd.to_datetime(dat['Date'])
    return dat

def filter_dividend(data):
    filtered_df = data[data['Dividends'] > 0]
    filtered_df = filtered_df[['Date', 'Dividends']]
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
    filtered_df['Date'] = filtered_df['Date'].dt.to_period('M').astype(str)
    filtered_df.set_index('Date', inplace=True)

    return filtered_df

def add_stock_prices(dividend_data, stock_data):
    dividend_data = dividend_data.reset_index()
    stock_data['Date'] = pd.to_datetime(stock_data['Date']).dt.tz_localize(None)
    dividend_data['Date'] = pd.to_datetime(dividend_data['Date']).dt.tz_localize(None)
    
    # Create a list to store results
    average_prices = []
    
    # Loop through each dividend payment date
    for div_date in dividend_data['Date']:
        # Calculate the start and end of the 3-month period
        start_date = (div_date - pd.DateOffset(months=1)).replace(day=1)
        end_date = div_date - pd.Timedelta(days=1)  # Day before the dividend month
    
        # Filter stock data for the 3-month period
        filtered_stock = stock_data[(stock_data['Date'] >= start_date) & (stock_data['Date'] <= end_date)]
    
        # Calculate the average close price
        avg_close_price = filtered_stock['Close'].mean()
        average_prices.append(avg_close_price)
    
    # Add the average prices as a new column to the dividend DataFrame
    dividend_data['Avg_Close_Prev_1_Month'] = average_prices
    return dividend_data

def prepare_train_test_data(train_data):
    train_data[['Dividends', 'Avg_Close_Prev_1_Month']] = scaler.fit_transform(train_data[['Dividends', 'Avg_Close_Prev_1_Month']])
    X, y = [], []

    for i in range(len(train_data) - 12):
        seq_x = train_data.iloc[i:i + 12][['Dividends', 'Avg_Close_Prev_1_Month']].values
        seq_y = train_data.iloc[i + 12]["Dividends"]
        
        X.append(seq_x)
        y.append(seq_y)

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, shuffle = False)

    return X_train, X_test, y_train, y_test

def configure_model(X_train, y_train):
    model = Sequential()
    model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))

    model.add(LSTM(units=50, activation='relu', return_sequences = True))
    model.add(LSTM(units=50, activation='relu'))
    model.add(Dense(units = 1))
    model.compile(optimizer = Adam(learning_rate = 0.001), loss='mean_squared_error')
    model.fit(X_train, y_train, epochs = 50, batch_size = 32)
    return model
    

def prepare_train_data(symbol):
    dividends = request_data(symbol)
    dividends = filter_dividend(dividends)
    stock = request_data(symbol)
    train_data = add_stock_prices(dividends, stock)
    return train_data

def predict_dividends(test_data, sequence_length, num_predictions, model):
    last_sequence = test_data.iloc[-sequence_length:][['Dividends', 'Avg_Close_Prev_1_Month']].values
    last_sequence_scaled = scaler.transform(last_sequence)
    current_input = last_sequence_scaled.reshape(1, sequence_length, 2)
    
    future_dividends = []
    
    for _ in range(num_predictions):
        # Predict the next dividend
        next_dividend_scaled = model.predict(current_input)  # Output: (1, 1)
        next_dividend = scaler.inverse_transform([[next_dividend_scaled[0, 0], 0]])[0, 0]  # Rescale to original scale
    
        # Append the prediction to the results
        future_dividends.append(next_dividend)
    
        # Update the input sequence
        # Remove the oldest timestep and add the predicted dividend with the most recent avg_close
        next_avg_close = test_data.iloc[-1]['Avg_Close_Prev_1_Month']  # Use the most recent avg_close from train_data
        next_timestep = [next_dividend_scaled[0, 0], scaler.transform([[0, next_avg_close]])[0, 1]]  # Scale avg_close
    
        # Append the new timestep and remove the oldest
        current_input = np.append(current_input[:, 1:, :], [[next_timestep]], axis=1)  # Update input
    
    # Print predictions
    print("Predicted Future Dividends:")
    print(future_dividends)
    return future_dividends

symbol = "JEPI"

