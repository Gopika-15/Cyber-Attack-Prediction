import numpy as np
import feature_extraction
from sklearn.ensemble import RandomForestClassifier as rfc
#from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression as lr
from flask import jsonify


def getResult(url):
    # url="http://www.facebook.com"

    #Importing dataset
    data = np.loadtxt( r"C:\Users\Maymol\Downloads\dos\dos\dos detection loan_server\src\dataset.csv", delimiter = ",")
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!_____________________________________________________________________")

    # print(data)

    #Seperating features and labels
    X = data[: , :-1]
    y = data[: , -1]

       #Seperating training features, testing features, training labels & testing labels
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    clf = rfc()
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    # print(score*100)
    # print("hello")
    accuracy=str(score*100)

    X_new = []

    X_input = url
    ress=""
    try:
        X_new=feature_extraction.generate_data_set(X_input)
        X_new = np.array(X_new).reshape(1,-1)

        try:
            prediction = clf.predict(X_new)
            print(prediction,"-------------------------")
            if prediction == -1:
                ress="Phishing Url"
                return ress,accuracy
            else:
                ress="Legitimate Url"
                return ress,accuracy
        except Exception as r:
            print(r,"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            ress="Legitimate Url"
            return ress,accuracy
    except Exception as e:
        print(e,"===========")
        ress="Phishing Url"
        return ress,accuracy

print (getResult("xxxx"))