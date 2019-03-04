import sklearn.neural_network as nn
import pandas as pd
import datetime
import numpy as np
from collect_data import get_volume, maprange, get_date_from_day, get_day_from_date


data_1 = pd.read_csv("sw.csv")
data_2 = pd.read_csv("a-k-flux.csv")
#lbfgs
network = nn.MLPRegressor(hidden_layer_sizes=(10,), solver='lbfgs', verbose=True)

X = pd.concat([data_1["day"], data_2["solar_flux"], data_2["a"], data_2["k"]], axis=1, keys=['day', 'solar_flux', 'a', 'k'])

network.fit(X, data_1["volume"])


d = "21/01/19"
day = get_day_from_date(d)

day_real_volume = round(get_volume(day), 2)
day_data = np.array([day, 72, 3, 3]).reshape(1,-1)
pred = round(network.predict(day_data)[0], 2)

print("Date: {}".format(get_date_from_day(day)) )
print("Real volume on  = {} db".format(day_real_volume))
print("Predicted volume = {} db".format(pred))
print("Error = {} db".format(abs(day_real_volume - pred)))
