import numpy as np
import yfinance as yf
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta

class Stockmarket:
  def __init__(self, stockName, days_future):
    self.stockName = stockName
    self.days_future = days_future
  def predict(self):
    today = datetime.now() 
    n_days_ago = today - timedelta(days=60)
    tomorrow = today + timedelta(days = 1)
    data = yf.download(self.stockName, start = n_days_ago, end=tomorrow)
    data = data[['Close']]
    data['Predictions'] = data[['Close']].shift(-self.days_future)
    X = np.array(data.drop(['Predictions'], 1))[:-self.days_future]
    y = np.array(data['Predictions'])[:-self.days_future]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    lr = linear_model.LinearRegression().fit(x_train, y_train)
    future_prices = data.drop(['Predictions'], 1)[:-self.days_future]
    future_prices = future_prices.tail(self.days_future)
    future_prices = np.array(future_prices)
    predicted_values = lr.predict(future_prices)
    predicted_values = predicted_values.tolist()
    cleared_values = []
    for i in predicted_values:
      cleared_values.append(round(i, 2))
    return cleared_values
