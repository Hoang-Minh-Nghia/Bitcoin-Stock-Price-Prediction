import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os.path
import numpy as np
import sys


# Nhận tham số từ command line
if len(sys.argv) > 1:
    name = sys.argv[1]
    print(f"Đã nhận tham số: {name}")
else:
    print("Không có tham số nào được truyền.")

# Read csv file
data = pd.read_csv("result.csv")

# Backup data origin
data_bk = data

# Remove NaN data
data = data.dropna()

# Remove name stock to train data
data = data[data['name'] != name]

name_out = data['name']
price_out = data['price']
data = data.drop('name', axis=1)
data = data.drop('price', axis=1)

x = data.values
y = price_out.values

param_to_predict = data_bk[data_bk['name'] == name].drop('name', axis=1)
real_value = param_to_predict['price'].values
param_to_predict = param_to_predict.drop('price', axis=1)

model = LinearRegression()
model.fit(x,y)

y_pred = model.predict(param_to_predict)
print("Prediction :", y_pred[0])
print("Real value :", real_value[0])


