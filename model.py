import sklearn.neural_network as nn
import pandas as pd
import datetime
import numpy as np


data_1 = pd.read_csv("sw.csv")
data_2 = pd.read_csv("a and k indexes.csv")
#lbfgs
network = nn.MLPRegressor(hidden_layer_sizes=(10,), solver='adam', verbose=True, learning_rate='adaptive')

X = pd.concat([data_1["date"], data_1["flux"], data_1["num_spots"], data_2["a"], data_2["k"]], axis=1, keys=['date','flux', 'num_spots', 'a', 'k'])

network.fit(X, data_1["volume"])

today = np.array([17915.0, 67.8, 5.3, 4, 0.87]).reshape(1,-1)
print(network.predict(today))


