import numpy
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

df = pd.read_csv("combined.csv")
dataset = df.values
dataset = dataset.astype('float32')

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):

		a = dataset[i:(i+look_back), 0]
		b = dataset[i:(i+look_back), 1]
		c = dataset[i:(i+look_back), 2]
		d = dataset[i:(i+look_back), 3]

		dataX.append(numpy.array([a,b,c,d]))
		dataY.append(dataset[i + look_back, 4])
	return numpy.array(dataX), numpy.array(dataY)

# normalize the dataset
#scaler = MinMaxScaler(feature_range=(0, 1))
#dataset = scaler.fit_transform(dataset)

train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

look_back = 1
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)


#trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[2]))
#testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[2]))


# create and fit the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(4, look_back)))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=600, batch_size=1, verbose=2)

testPredict = model.predict(testX)
print(testPredict)
