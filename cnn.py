
# Visualize training history
from keras.models import Sequential
from keras.layers import Dense
# import matplotlib.pyplot as plt
# import numpy
# # load pima indians dataset
# # dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# # # split into input (X) and output (Y) variables
# import speechData1
# X, Y = speechData1.loadDataSet()


import numpy as np

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import pandas as pd



def one_hot_from_item(item, items):
    # items=set(items) # assure uniqueness
    x = [0] * 2  # numpy.zeros(len(items))

    x[int(item)] = 1
    return x


df = pd.read_csv(r'C:\Users\Maymol\Downloads\dos\dos\dos detection loan_server\src\static\dataset\train.csv', header=None)
data = np.array(df)
x_train = data[:, :-1]
y_train = data[:, -1:]
print(x_train[0],len(x_train))
print(y_train)
from keras.models import model_from_json



def predict(x):
    model = model_from_json(open("model1.json", "r").read())
    model.load_weights("model1.h5")
    y = model.predict([x])
    print(y[0])
    if y[0][0]>y[0][1]:
        return 0
    return 1
# print(predict([[1,0,4583,1508,128,360,1,0]]))





