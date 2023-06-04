from keras.utils.np_utils import to_categorical
import numpy

import os

import warnings
from random import shuffle
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import numpy as np


import pandas as pd
train_audio_path = r'E:\myProjectCnn\samplecode\\'

all_wave = []
all_label = []


df = pd.read_csv(r'C:\Users\GOPIKA\Downloads\dos detection loan_server\dos detection loan_server\src\static\dataset\train.csv', header=None)
data = np.array(df)
x_train = data[:, :-1]
y_train = data[:, -1:]

X = np.array(x_train)
Y = y_train
print(X[0])
print(X[1])
print(X[2])
trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.20, random_state=4)


X = trainX
y_int = trainY
Y = to_categorical(y_int,2)
#Y = trainY

# Test Set
XTest = testX
#ytest=testY
ytest_int = testY
yTest = to_categorical(ytest_int)
# create model
model = Sequential()
model.add(Dense(output_dim=4, init='uniform', activation='relu', input_dim=8))
model.add(Dense(output_dim=4, init='uniform', activation='relu', input_dim=4))
model.add(Dense(output_dim=2, init='uniform', activation='softmax', input_dim=4))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()
if not os.path.isfile("model21.h5"):
# Fit the model
    history = model.fit(X, Y, nb_epoch=30, batch_size=20)

    curt = 0
    print("\nSLNO  :  Predict -> Label\n")
    model_json = model.to_json()
    with open("model1.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model1.h5")
    lt = len(XTest)
    y = model.predict(XTest)
    ytest = []
    ans = []
    # print()
    for r in range(0, len(y)):
        p = list(y[r]).index(max(list(y[r])))
        v = list(yTest[r]).index(max(list(yTest[r])))
        ans.append(p)
        ytest.append(v)
        # print(list(y[r]).index(max(list(y[r]))))
        # print(list(Y[r]).index(max(list(Y[r]))))
        # print( "********")

        if p == v:
            curt += 1
            # translate_text = translator.translate(str(outputlabels[int(p)]), lang_src='en', lang_tgt='ml')

        # print(r + 1, "\t:  ", int(p) + 1, outputlabels[int(p)], " --> ", int(v + 1))

    cm = confusion_matrix(ytest, ans)
    print("confusion_matrix")
    print(cm)
    print("\n\t ACCURACY : ", curt / lt)


else:
    model=model_from_json(open("model1.json","r").read())
    model.load_weights("model1.h5")


    print("\n....Model is already trained....\n")
    print("\nSLNO  :  Predict -> Label\n")
    curt = 0
    lt = len(XTest)
    y = model.predict(XTest)
    ytest = []
    ans = []
    # print()
    for r in range(0, len(y)):
        p = list(y[r]).index(max(list(y[r])))
        v = list(yTest[r]).index(max(list(yTest[r])))
        ans.append(p)
        ytest.append(v)
        # print(list(y[r]).index(max(list(y[r]))))
        # print(list(Y[r]).index(max(list(Y[r]))))
        # print( "********")

        if p == v:
            curt += 1
            # translate_text = translator.translate(str(outputlabels[int(p)]), lang_src='en', lang_tgt='ml')

        print(r + 1, "\t:  ", int(p) + 1, outputlabels[int(p)], " --> ", int(v + 1))

    cm = confusion_matrix(ytest, ans)
    print("confusion_matrix")
    print(cm)
    print("\n\t ACCURACY : ", curt / lt)
# ******************************

# translator = google_translator()
# #model.load("model1.h5")
# print("\n....Model is already trained....\n")
# print("\nSLNO  :  Predict -> Label\n")
# curt = 0
# lt = len(XTest)
# ytest=[]
# ans=[]
# for i in range(1, lt + 1):
#     p = np.argmax(model.predict(XTest[i - 1:i]))
#     v = np.argmax(ytest_int[i - 1:i])
#     ans.append(p)
#     ytest.append(v)
#     if p == v:
#         curt += 1
#             #translate_text = translator.translate(str(outputlabels[int(p)]), lang_src='en', lang_tgt='ml')
#
#         print(i, "\t:  ", int(p)+1,outputlabels[int(p)], " --> ", int(v+1))
#
#
# cm=confusion_matrix(ytest,ans)
# print("confusion_matrix")
# print(cm)
# print("\n\t ACCURACY : ", curt / lt)
#


# ****************************
# print("Prediction   Result")
# files = os.listdir("predict/")
# #print(len(files))
# for wav in files:
#     if not wav.endswith(".wav"): continue
#     model.load("model1.h5")
#
#     //T = speechData.mfcc_target1("predict/"+wav)
#     #lt = len(T)
#     pp = np.argmax(model.predict(T))
#     print(outputlabels[int(pp)])

# #Only code needed to save model
# model_json = model.to_json()
# with open("model1.json", "w") as json_file:
#     json_file.write(model_json)
# model.save_weights("model1.h5")
##################################